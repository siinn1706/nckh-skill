"""Preview/apply/remove explicit project-owned hooks; no native trust mutation."""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
if (ROOT / "hooks/_shared").is_dir():
    sys.path.insert(0, str(ROOT / "hooks/_shared"))

from core.hook_config import TARGETS, apply_config, payload_from_bundle, preview_config, recover_config
from core.guards import _visual_file
from core.paths import atomic_json, contained, digest_record
from core.schema import ContractError
from hooks.runner import strict_json

FAILURE_CASES = {"allow", "policy-deny", "malformed-input", "malformed-output", "timeout", "crash", "unsupported", "duplicate"}


def native_evidence(project, reference, preview):
    path = contained(project, reference)
    if path.stat().st_size > 131072:
        raise ContractError("native evidence oversized")
    record = strict_json(path.read_bytes())
    if (record.get("schema_version") != 1 or record.get("host") != preview["host"]
            or record.get("version") != preview["host_version"] or record.get("version") == "unverified"
            or record.get("surface") != preview["surface"] or record.get("surface") == "unverified"
            or record.get("closure_hash") != preview["payload"]["closure_hash"]):
        raise ContractError("native evidence does not bind the selected hook host/version/payload")
    for definition in preview["definitions"]:
        rows = [row for row in record.get("cases", []) if row.get("event") == definition["event"]]
        if len(rows) != 8 or {row.get("case") for row in rows} != FAILURE_CASES:
            raise ContractError("native failure-path matrix incomplete")
        for row in rows:
            if row.get("status") != "observed" or row.get("surface") != preview["surface"] or not row.get("cleanup"):
                raise ContractError("native observation/cleanup missing")
            _visual_file(project, row["receipt"])
            if row["case"] in {"policy-deny", "malformed-input", "malformed-output", "timeout", "crash"} and row.get("side_effects_absent") is not True:
                raise ContractError("native route has no preventive failure evidence")
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=["preview", "apply", "remove", "recover"])
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--host", choices=sorted(TARGETS), required=True)
    parser.add_argument("--package", type=Path)
    parser.add_argument("--action", choices=["apply", "remove"], default="apply", help="Action proposed by preview.")
    parser.add_argument("--events", nargs="+")
    parser.add_argument("--mode", choices=["advisory", "enforce"], default="enforce",
                        help="Advisory reports checks without denying tools; enforcement requires native evidence.")
    parser.add_argument("--context", default=".nckh-state/hooks/context/current.json")
    parser.add_argument("--host-version", default="unverified")
    parser.add_argument("--surface", default="unverified", help="Exact native surface to qualify; host alone does not cover every surface.")
    parser.add_argument("--preview-file", type=Path)
    parser.add_argument("--approved-hash")
    parser.add_argument("--transaction", help="Project-relative interrupted journal; recover requires its current canonical record hash.")
    parser.add_argument("--grant-reference", help="Separate human activation grant; preview/evidence files do not grant authority.")
    parser.add_argument("--native-evidence", help="Project-relative actual failure-path observations; hashes alone cannot authenticate host behavior.")
    parser.add_argument("--output", type=Path, help="Save a private preview; preview never writes config/runtime.")
    args = parser.parse_args()
    try:
        if args.operation == "recover":
            if not args.transaction or not args.approved_hash:
                raise ContractError("recovery requires its reviewed journal and current hash")
            journal = strict_json(contained(args.project, args.transaction).read_bytes())
            if journal.get("host") != args.host:
                raise ContractError("recovery host differs")
            result = recover_config(args.project, args.transaction, approved_hash=args.approved_hash)
        elif not args.package:
            raise ContractError("explicit verified package required")
        elif args.operation == "preview":
            payload = payload_from_bundle(args.package)
            result = preview_config(args.project, args.host, payload, action=args.action, events=args.events,
                context_reference=args.context, host_version=args.host_version, surface=args.surface, mode=args.mode)
            result = {"preview": result, "preview_hash": digest_record(result)}
            if args.output:
                atomic_json(args.output, result)
            result = {"preview_hash": result["preview_hash"], "preview": {key: result["preview"][key] for key in
                ("action", "host", "host_version", "surface", "mode", "target", "runtime_relative", "registered", "enabled", "trusted", "native_qualification")},
                "private_preview_saved": bool(args.output)}
        else:
            payload = payload_from_bundle(args.package)
            if not args.preview_file or not args.approved_hash:
                raise ContractError("apply/remove requires the exact reviewed preview file/hash")
            envelope = strict_json(args.preview_file.read_bytes())
            preview = envelope["preview"]
            if (str(args.project.resolve()) != preview["project"] or args.host != preview["host"]
                    or preview["payload"] != payload or preview["action"] != args.operation):
                raise ContractError("preview project/host/package/action differs")
            qualified = bool(args.native_evidence and native_evidence(args.project, args.native_evidence, preview))
            result = apply_config(preview, approved_hash=args.approved_hash,
                                  grant_reference=args.grant_reference, native_verified=qualified)
        print(json.dumps(result, ensure_ascii=True, indent=2))
        return 0
    except (ContractError, OSError, ValueError, KeyError, TypeError, RecursionError):
        print(json.dumps({"status": "conflict-no-write-or-rolled-back", "native_qualification": "unverified",
                          "instruction": "Review the private transaction journal and create a fresh preview."}))
        return 3


if __name__ == "__main__":
    sys.exit(main())
