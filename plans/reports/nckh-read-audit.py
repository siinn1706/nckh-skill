"""One-shot read audit for the NCKH kit source and installed .agents skills."""

import ast
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import traceback
from pathlib import Path

REPO = Path(r"C:/Users/USER\Downloads\test-skill")
KIT = REPO / "nckh-kit"
INSTALLED = REPO / ".agents" / "skills"
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
SKIP_PARTS = {
    "dist-resource-quality-r22",
    "__pycache__",
    ".git",
    "plans",
    "github-publication",
    "publication-r41",
    "resources",
}

errors = []
notes = []
counts = {
    "source_skill_links": 0,
    "installed_skill_links": 0,
    "doc_links": 0,
    "resource_files": 0,
    "resource_lookups": 0,
    "installed_resource_files": 0,
    "installed_lookups": 0,
    "json_files": 0,
    "python_files": 0,
    "hook_invocations": 0,
}


def add(kind, location, detail):
    errors.append({"kind": kind, "location": str(location), "detail": detail})


def note(kind, location, detail):
    notes.append({"kind": kind, "location": str(location), "detail": detail})


def should_skip(path):
    return any(part in SKIP_PARTS for part in path.parts)


def normalize_target(raw):
    target = raw.strip().strip("<>")
    if not target or target.startswith(("#", "http://", "https://", "mailto:")):
        return None
    if any(token in target for token in ("<", ">", "*", "EXTRACTED", "PROJECT", "{", "}")):
        return None
    return target.split("#", 1)[0]


def check_link(source, raw, kind):
    target = normalize_target(raw)
    if target is None:
        return
    counts[kind] += 1
    path = (source.parent / target).resolve()
    try:
        data = path.read_bytes()
    except OSError as error:
        add(kind, f"{source.relative_to(REPO)} -> {raw}", f"{type(error).__name__}: {error}")
        return
    if path.suffix == ".json":
        try:
            json.loads(data.decode("utf-8-sig"))
        except (UnicodeError, json.JSONDecodeError) as error:
            add("json-parse", path, f"{type(error).__name__}: {error}")
    elif path.suffix == ".py":
        try:
            ast.parse(data.decode("utf-8-sig"))
        except (UnicodeError, SyntaxError) as error:
            add("python-parse", path, f"{type(error).__name__}: {error}")


def scan_markdown(root, kind):
    if not root.exists():
        add(kind, root, "root missing")
        return
    for path in root.rglob("*.md"):
        if should_skip(path):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            add("markdown-read", path.relative_to(REPO), f"{type(error).__name__}: {error}")
            continue
        for match in LINK_RE.finditer(text):
            check_link(path, match.group(1), kind)


def load_reader(script):
    spec = importlib.util.spec_from_file_location(f"reader_{hash(script)}", script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def lookup_args(row, root):
    args = {
        "domain": row["domain"],
        "locale": row["locale"],
        "genre": row["genre"],
        "root": root,
        "query": "",
    }
    identity = row["resource_id"]
    if identity == "R-reporting-lookup":
        args["study_design"] = "randomized_trial"
    elif identity == "R-publisher-profile":
        args.update(venue="science", stage="revised", year="2026", track="journal", article_type="research")
    elif identity == "R-ui-lookup":
        args["query"] = "keyboard navigation"
    return args


def check_catalog(catalog_path, root, reader, consumer_filter, file_kind, lookup_kind):
    try:
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        add("catalog-read", catalog_path.relative_to(REPO), f"{type(error).__name__}: {error}")
        return
    for row in catalog.get("resources", []):
        paths = [row.get("path"), *(row.get("requires") or [])]
        source = row.get("source") or {}
        paths.extend([source.get("license_path"), source.get("notice_path"), source.get("review_reference")])
        seen = set()
        for relative in paths:
            if not relative or relative in seen:
                continue
            seen.add(relative)
            counts[file_kind] += 1
            target = root / relative
            try:
                data = target.read_bytes()
            except OSError as error:
                add(file_kind, f"{catalog_path.relative_to(REPO)} :: {row['resource_id']} :: {relative}", f"{type(error).__name__}: {error}")
                continue
            if relative == row.get("path"):
                digest = hashlib.sha256(data).hexdigest()
                expected = source.get("sha256")
                if expected and digest != expected:
                    add("resource-hash", f"{row['resource_id']} :: {relative}", f"sha256 {digest} != catalog {expected}")
        consumers = row.get("consumers") or []
        if consumer_filter is not None and consumer_filter not in consumers:
            continue
        counts[lookup_kind] += 1
        consumer = consumers[0] if consumer_filter is None else consumer_filter
        if reader is None:
            result, detail = subprocess_lookup(catalog_path, row, consumer)
            if result is None:
                add(lookup_kind, f"{catalog_path.relative_to(REPO)} :: {row['resource_id']}", detail)
                continue
        else:
            try:
                result = reader.lookup(row["resource_id"], consumer, **lookup_args(row, root))
            except Exception as error:
                add(lookup_kind, f"{catalog_path.relative_to(REPO)} :: {row['resource_id']}", f"{type(error).__name__}: {error}")
                continue
        if not result.get("resource_read"):
            add(lookup_kind, f"{catalog_path.relative_to(REPO)} :: {row['resource_id']}", f"resource_read false; status={result.get('status')} warnings={result.get('warnings')}")
        elif not result.get("records"):
            note(lookup_kind, f"{catalog_path.relative_to(REPO)} :: {row['resource_id']}", "read succeeded with zero records")


def subprocess_lookup(catalog_path, row, consumer):
    script = catalog_path.parents[3] / "scripts" / "search-resource.py"
    if not script.exists():
        return None, f"reader missing: {script}"
    args = lookup_args(row, script.resolve().parents[1])
    command = [sys.executable, "-I", str(script), "--resource-id", row["resource_id"], "--consumer", consumer,
               "--domain", args["domain"], "--locale", args["locale"], "--genre", args["genre"], "--query", args["query"], "--json"]
    if row["resource_id"] == "R-reporting-lookup":
        command.extend(["--study-design", args["study_design"]])
    elif row["resource_id"] == "R-publisher-profile":
        command.extend(["--venue", args["venue"], "--stage", args["stage"], "--year", args["year"],
                        "--track", args["track"], "--article-type", args["article_type"]])
    try:
        process = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", timeout=60)
    except (OSError, subprocess.TimeoutExpired) as error:
        return None, f"{type(error).__name__}: {error}"
    if process.returncode:
        detail = (process.stderr or process.stdout or "").strip()
        return None, f"exit {process.returncode}: {detail[:2000]}"
    try:
        return json.loads(process.stdout), ""
    except json.JSONDecodeError as error:
        return None, f"stdout is not JSON: {error}; stdout={process.stdout[:500]!r}"


def check_python(root):
    for path in root.rglob("*.py"):
        if should_skip(path):
            continue
        counts["python_files"] += 1
        try:
            source = path.read_text(encoding="utf-8")
            ast.parse(source)
        except (OSError, UnicodeError, SyntaxError) as error:
            add("python-parse", path.relative_to(REPO), f"{type(error).__name__}: {error}")


def check_json(root):
    for path in root.rglob("*.json"):
        if should_skip(path):
            continue
        if path.stat().st_size > 20_000_000:
            note("json-skip", path.relative_to(REPO), "larger than 20MB")
            continue
        counts["json_files"] += 1
        try:
            json.loads(path.read_text(encoding="utf-8-sig"))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            add("json-parse", path.relative_to(REPO), f"{type(error).__name__}: {error}")


def check_hooks():
    sys.path.insert(0, str(KIT))
    try:
        from core.paths import atomic_json, temporary_tree
        from hooks.runner import invoke
    except Exception as error:
        add("hook-import", "nckh-kit/hooks", f"{type(error).__name__}: {error}\n{traceback.format_exc()}")
        return
    with temporary_tree() as project:
        atomic_json(project / "context.json", {
            "schema_version": 1,
            "task_id": "read-audit",
            "tool_operations": {"Write": "write"},
            "allowed_operations": ["write"],
            "brief": {"mode": "auto"},
        })
        payloads = {
            "cursor": {"hook_event_name": "preToolUse", "conversation_id": "audit", "workspace_roots": [str(project)],
                       "tool_name": "Write", "tool_input": {"file_path": "draft.md"}, "loop_count": 0},
            "agy": {"conversationId": "audit", "workspacePaths": [str(project)],
                    "toolCall": {"name": "Write", "args": {"path": "draft.md"}}, "executionNum": 1},
            "claude": {"hook_event_name": "PreToolUse", "session_id": "audit", "cwd": str(project), "model": "unverified",
                       "turn_id": "audit-turn", "tool_name": "Write", "tool_input": {"file_path": "draft.md"}, "stop_hook_active": False},
            "codex": {"hook_event_name": "PreToolUse", "session_id": "audit", "cwd": str(project), "model": "unverified",
                      "turn_id": "audit-turn", "tool_name": "Write", "tool_input": {"file_path": "draft.md"}, "stop_hook_active": False},
        }
        names = {"cursor": "preToolUse", "agy": "PreToolUse", "claude": "PreToolUse", "codex": "PreToolUse"}
        for host, payload in payloads.items():
            counts["hook_invocations"] += 1
            try:
                (wire, code), receipt = invoke(host, names[host], json.dumps(payload).encode(), project=project, context_reference="context.json")
            except Exception as error:
                add("hook-invoke", host, f"{type(error).__name__}: {error}")
                continue
            if code not in (0, 3) or not isinstance(receipt, dict):
                add("hook-invoke", host, f"unexpected result code={code} receipt={receipt}")
            else:
                note("hook-invoke", host, f"code={code} status={receipt.get('status')} decision={receipt.get('decision')} mode={receipt.get('hook_mode')}")
        for relative in (".cursor/hooks.json", ".agents/hooks.json", ".codex/hooks.json", ".claude/settings.local.json"):
            target = REPO / relative
            if target.exists():
                try:
                    json.loads(target.read_text(encoding="utf-8-sig"))
                    note("installed-hook-config", relative, "present and JSON-parsed")
                except (OSError, UnicodeError, json.JSONDecodeError) as error:
                    add("installed-hook-config", relative, f"{type(error).__name__}: {error}")
            else:
                note("installed-hook-config", relative, "not installed in this workspace")


def main():
    scan_markdown(KIT / "skills", "source_skill_links")
    scan_markdown(KIT / "docs", "doc_links")
    scan_markdown(INSTALLED, "installed_skill_links")
    for root in (KIT / "core", KIT / "hooks", KIT / "scripts", KIT / "skills", KIT / "docs", KIT / "tests", KIT / "adapters", KIT / "installer", KIT / "evals"):
        if root.exists():
            check_python(root)
            check_json(root)
    check_python(INSTALLED)
    check_json(INSTALLED)
    reader = load_reader(KIT / "scripts" / "search-resource.py")
    check_catalog(KIT / "core" / "registry" / "catalog" / "resources.json", KIT, reader, None, "resource_files", "resource_lookups")
    if INSTALLED.exists():
        for skill_dir in sorted(path for path in INSTALLED.iterdir() if path.is_dir() and path.name.startswith("nckh-")):
            script = skill_dir / "references" / "_shared" / "scripts" / "search-resource.py"
            catalog = skill_dir / "references" / "_shared" / "core" / "registry" / "catalog" / "resources.json"
            if not script.exists() or not catalog.exists():
                note("installed-resource-pack", skill_dir.name, f"reader={script.exists()} catalog={catalog.exists()}")
                continue
            check_catalog(catalog, script.resolve().parents[1], None, skill_dir.name, "installed_resource_files", "installed_lookups")
    check_hooks()
    report = {"counts": counts, "error_count": len(errors), "note_count": len(notes), "errors": errors, "notes": notes}
    destination = Path(__file__).with_suffix(".json")
    destination.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"error_count": len(errors), "note_count": len(notes), "counts": counts, "report": str(destination)}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        traceback.print_exc()
        sys.exit(2)
