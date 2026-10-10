"""Bounded stdin hook runner; no payload command execution, transcript reads or egress."""

import argparse
import importlib
import json
import math
import os
import re
import sys
import time
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
if (ROOT / "hooks/_shared").is_dir():
    sys.path.insert(0, str(ROOT / "hooks/_shared"))

from core.hook_policy import MAX_CONTEXT_BYTES, MAX_EVENT_BYTES, evaluate
from core.paths import atomic_json, contained, digest_bytes, digest_record, exclusive_file_lock, no_links
from core.schema import ContractError, validate_record

HOSTS = {"claude", "codex", "cursor", "agy"}
# Failed receipts keep a per-attempt identity so every failure stays visible.
PER_ATTEMPT_STATUSES = {"degraded-failed"}
# Missing-context receipts fire on every event of an unconfigured install; they are
# deduplicated per session and capped so the receipt namespace cannot grow unbounded.
# Only these receipts carry the prefix and count toward the cap; once it is hit, one
# marker records that later ones were dropped. Every other receipt is never capped.
CAPPED_STATUSES = {"degraded-no-context"}
CAPPED_PREFIX = "no-context-"
CAPPED_NAME = re.compile(re.escape(CAPPED_PREFIX) + r"[a-f0-9]{64}\.json")
CAP_MARKER = "cap-reached-no-context.json"
RECEIPT_CAP = 1000
ROUTE_BOUNDARIES = "registry/catalog/route-boundaries.json"


class ContextUnavailable(ContractError):
    """Controller context is absent or oversized; distinct from malformed hook input."""


def strict_json(data):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ContractError("duplicate hook JSON key")
            result[key] = value
        return result
    def reject(value):
        raise ContractError("nonfinite hook JSON")
    def finite_float(value):
        number = float(value)
        if not math.isfinite(number):
            raise ContractError("nonfinite hook JSON number")
        return number
    try:
        value = json.loads(data, object_pairs_hook=unique, parse_constant=reject, parse_float=finite_float)
    except (json.JSONDecodeError, UnicodeError) as exc:
        raise ContractError("invalid hook JSON encoding or syntax") from exc
    if not isinstance(value, dict):
        raise ContractError("hook JSON must be an object")
    return value


def load_context(project, reference):
    path = contained(project, reference)
    if not path.is_file() or path.stat().st_size > MAX_CONTEXT_BYTES:
        raise ContextUnavailable("bounded controller context unavailable")
    data = path.read_bytes()
    return strict_json(data), digest_bytes(data)


def _installed_skills(project, roots, skills):
    return {skill for skill in skills
            if any((project / root / skill / "SKILL.md").is_file() for root in roots)}


def _nudge(codec, host, decoded, project, paths):
    """Return `{kind, text, ...}` for a routing or EOL/BOM nudge, or None.

    Runs before the controller context is loaded so hints survive a missing
    context. Any failure yields None: a nudge never changes the hook decision.
    """
    try:
        phase, tool = decoded["phase"], decoded["tool"]
        if phase == "advisory" and isinstance(decoded.get("prompt"), str):
            if not getattr(codec, "SKILL_INVOCATION", None):
                return None
            from core import route_hint
            boundaries = route_hint.load_boundaries(Path(route_hint.__file__).parent / ROUTE_BOUNDARIES)
            skills = {skill for boundary in boundaries for skill in boundary["vi_cues"]}
            matches = route_hint.match(decoded["prompt"], boundaries,
                                       installed=_installed_skills(project, codec.SKILL_ROOTS, skills))
            text = route_hint.hint_text(matches, codec.SKILL_INVOCATION)
            return {"kind": "route-hint", "text": text, "skills": [hint["skill"] for hint in matches]} if text else None
        if tool not in getattr(codec, "WRITE_TOOLS", ()) or not paths:
            return None
        from core import edit_guard
        if phase == "preflight":
            # Only existing files can lose their EOL/BOM; new files leave no runtime state,
            # but a snapshot left by an unfinished earlier edit of the same path is dropped.
            existing = [path for path in paths if (project / path).is_file()]
            absent = [path for path in paths if path not in existing]
            if absent:
                edit_guard.discard(project, host, decoded["session_key"], absent)
            if existing:
                edit_guard.snapshot(project, host, decoded["session_key"], existing)
            return None
        if phase == "pre-delivery":
            findings = edit_guard.compare(project, host, decoded["session_key"], paths)
            text = edit_guard.advice_text(findings)
            # Receipts never carry raw project paths; record their digests instead.
            return {"kind": "eol-bom", "text": text,
                    "path_hashes": [digest_record(finding["path"]) for finding in findings]} if text else None
    except Exception:  # noqa: BLE001 - an advisory nudge must never alter the decision path
        return None
    return None


def _carries(value, text):
    """True when an encoded wire value contains the nudge text."""
    if isinstance(value, str):
        return text in value
    if isinstance(value, dict):
        return any(_carries(item, text) for item in value.values())
    if isinstance(value, list):
        return any(_carries(item, text) for item in value)
    return False


def _nudge_record(nudge, delivered):
    """Receipt form of a nudge: kind plus skills or path digests, never prompt text.

    A nudge the host wire did not carry (no context channel for the event, or a
    block that replaces it) is marked `delivered: false`, so receipts never count
    it as shown to the model.
    """
    record = {key: value for key, value in nudge.items() if key != "text"}
    if not delivered:
        record["delivered"] = False
    return record


def invoke(host, event_name, payload_bytes, *, project, context_reference, mode="enforce"):
    if host not in HOSTS:
        raise ContractError("unknown hook host")
    if mode not in {"advisory", "enforce"}:
        raise ContractError("unknown hook mode")
    codec = importlib.import_module("hooks.codecs." + host)
    nudge = None
    decoded = None
    def encode(decision):
        """Return (wire, exit code, whether the wire carries the nudge text)."""
        wire_decision = dict(decision)
        if nudge is not None:
            wire_decision["nudge_text"] = nudge["text"]
        if mode == "advisory":
            wire_decision["decision"] = "advisory"
        wire, code = codec.encode(event_name, wire_decision)
        carried = nudge is not None and _carries(wire, nudge["text"])
        return wire, 0 if mode == "advisory" else code, carried
    failure = {"schema_version": 1, "decision": "block", "reason_codes": ["hook-input-or-context-invalid"],
               "evidence_class": "deterministic", "native_enforcement": "unverified", "semantic_fidelity": "unverified", "side_effects": "none"}
    def degrade(reason_code, status):
        # Advisory never denies. Enforce hands the codec a block decision; codecs turn it
        # into a native deny/block only on gating events (PreToolUse/preToolUse and
        # UserPromptSubmit/beforeSubmitPrompt). Other known events return advisory
        # context with exit 0; an unknown event exits 3.
        record = {**failure, "reason_codes": [reason_code]}
        wire, code, carried = encode(record)
        receipt = {**record, "schema_version": 1, "host": host, "status": status,
                   "event_hash": digest_bytes(payload_bytes), "native_host_response": "unobserved", "hook_mode": mode}
        if decoded is not None:
            receipt.update(phase=decoded["phase"], session_key=decoded["session_key"])
        if nudge is not None:
            receipt["nudge"] = _nudge_record(nudge, carried)
        return (wire, code if mode == "advisory" or event_name in codec.EVENTS else 3), receipt
    try:
        project = no_links(project).resolve()
        if len(payload_bytes) > MAX_EVENT_BYTES:
            raise ContractError("hook event byte limit exceeded")
        payload = strict_json(payload_bytes)
        decoded = codec.decode(payload, event_name)
        if str(project).casefold() not in {str(no_links(root).resolve()).casefold() for root in decoded["reported_roots"]}:
            raise ContractError("hook project identity mismatch")
        paths = []
        for path in decoded["raw_paths"]:
            candidate = Path(path)
            if candidate.is_absolute():
                candidate = no_links(candidate).resolve()
                if not candidate.is_relative_to(project):
                    raise ContractError("hook path escapes selected project")
                path = candidate.relative_to(project).as_posix()
            contained(project, path)
            paths.append(path)
        nudge = _nudge(codec, host, decoded, project, paths)
        context, context_hash = load_context(project, context_reference)
        event = validate_record("hook-event", {"schema_version": 1, "phase": decoded["phase"], "host": host,
            "tool": decoded["tool"], "paths": paths, "session_key": decoded["session_key"],
            "task_key": digest_record(context.get("task_id", "unverified")),
            "artifact_sha256": context.get("artifact_sha256", digest_record(None)), "stop_active": decoded["stop_active"]})
        decision = evaluate(event, context, project=project)
        wire, code, carried = encode(decision)
        receipt = {"schema_version": 1, "host": host, "phase": event["phase"],
            "event_hash": digest_record(event), "context_hash": context_hash, "artifact_sha256": event["artifact_sha256"],
            "session_key": event["session_key"], "task_key": event["task_key"], **decision,
            "status": "checked-unreviewed", "native_host_response": "unobserved"}
        receipt["hook_mode"] = mode
        if nudge is not None:
            receipt["nudge"] = _nudge_record(nudge, carried)
        return (wire, code), receipt
    except ContextUnavailable:
        return degrade("hook-context-unavailable", "degraded-no-context")
    except (ContractError, OSError, ValueError, KeyError, TypeError, RecursionError, OverflowError):
        return degrade("hook-input-or-context-invalid", "degraded-failed")


def _receipt_count_reached(directory, limit):
    count = 0
    with os.scandir(directory) as entries:
        for entry in entries:
            if CAPPED_NAME.fullmatch(entry.name):
                count += 1
                if count >= limit:
                    return True
    return False


def record_once(project, relative, receipt):
    directory = contained(project, relative)
    directory.mkdir(parents=True, exist_ok=True)
    status = receipt.get("status")
    if status in CAPPED_STATUSES:
        identity = {name: receipt.get(name) for name in
            ("host", "phase", "session_key", "hook_mode", "reason_codes")}
        identity["nudge"] = digest_record(receipt.get("nudge"))
    else:
        identity = {name: receipt.get(name) for name in
            ("host", "phase", "session_key", "task_key", "artifact_sha256", "reason_codes", "hook_mode")}
        if status in PER_ATTEMPT_STATUSES:
            identity.update(event_hash=receipt.get("event_hash"), failed_attempt=uuid.uuid4().hex)
        elif receipt.get("phase") != "stop":
            identity.update(context_hash=receipt.get("context_hash"), event_hash=receipt.get("event_hash"))
        if receipt.get("nudge") is not None:
            identity["nudge"] = digest_record(receipt["nudge"])
    key = (CAPPED_PREFIX if status in CAPPED_STATUSES else "") + digest_record(identity)
    path = contained(directory, key + ".json")
    for attempt in range(6):
        try:
            with exclusive_file_lock(contained(directory, key + ".lock")):
                if path.exists():
                    return "duplicate-suppressed"
                if status in CAPPED_STATUSES and _receipt_count_reached(directory, RECEIPT_CAP):
                    marker = contained(directory, CAP_MARKER)
                    if not marker.exists():
                        atomic_json(marker, {"schema_version": 1, "host": receipt.get("host"),
                                             "status": "cap-reached", "hook_mode": receipt.get("hook_mode"),
                                             "reason_codes": ["hook-receipt-cap-reached"], "cap": RECEIPT_CAP})
                    return "cap-reached"
                atomic_json(path, receipt)
                return "recorded"
        except ContractError:
            if attempt == 5:
                raise
            time.sleep(0.01)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", choices=sorted(HOSTS), required=True)
    parser.add_argument("--event", required=True)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--context", required=True, help="Controller-selected project-relative context, never supplied by event payload.")
    parser.add_argument("--mode", choices=["advisory", "enforce"], default="enforce")
    parser.add_argument("--receipt-dir", help="Explicit owned project-relative receipt namespace.")
    args = parser.parse_args()
    payload = sys.stdin.buffer.read(MAX_EVENT_BYTES + 1)
    (wire, code), receipt = invoke(args.host, args.event, payload, project=args.project, context_reference=args.context, mode=args.mode)
    if args.receipt_dir:
        try:
            record_once(args.project, args.receipt_dir, receipt)
        except (ContractError, OSError):
            receipt["status"] = "degraded-failed"
            codec = importlib.import_module("hooks.codecs." + args.host)
            wire, code = codec.encode(args.event, {"decision": "advisory" if args.mode == "advisory" else "block",
                                                "reason_codes": ["hook-receipt-conflict"]})
            if args.mode == "advisory":
                code = 0
    print(json.dumps(wire, ensure_ascii=True))
    return code


if __name__ == "__main__":
    sys.exit(main())
