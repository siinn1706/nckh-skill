"""Adapt owned probes with an isolated evidence namespace and safe cleanup."""

import json
import shutil
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
OLD = RUN.parent / "nckh-native-261005-0658-r34-codex-file-attempt-01"
NEW = RUN / "native-codex-file"
if NEW.exists():
    raise RuntimeError("Preserve the earlier native retest")
NEW.mkdir()
source = (OLD / "codex-native-files.py").read_text(encoding="utf8")
source = source.split('if len(sys.argv) == 2 and sys.argv[1] == "cleanup-only":', 1)[0]
source = source.replace('WORK = RUN.parents[2]', 'WORK = Path(r"C:/Users/USER\\Downloads\\test-skill")')
source = source.replace('PROJECT = RUN / "project-02"', 'PROJECT = Path(r"C:/Users/USER\\Downloads\\test-skill\\plans\\runs\\nckh-native-261005-0658-r34-codex-file-attempt-01\\project-02")\nEVIDENCE = PROJECT / ".nckh-native-r35-file"')
source = source.replace('OLD = RUN.parent / "nckh-native-261004-1707-attempt-01"', 'OLD = WORK / "plans/runs/nckh-native-261004-1707-attempt-01"')
source = source.replace('DELIVERY = RUN.parent / "nckh-native-261005-0005-r34-attempt-01"', 'DELIVERY = RUN.parent')
source = source.replace('8ca3304f3c906b0a3421c38fbb32c939ec23839537e9b9c5fc23421da0a21b34', '4482bbba7f4537025b523d887abe34774a4427d397549730f1ba8cf9fd50a255')
source = source.replace('relative_to(RUN).as_posix()', 'relative_to(WORK).as_posix()')
source = source.replace('PROJECT / "definition.json"', 'RUN / "definition.json"')
source = source.replace('PROJECT / "control.json"', 'EVIDENCE / "control.json"')
source = source.replace('PROJECT / "attempts"', 'RUN / "attempts"')
source = source.replace('PROJECT / "observations"', 'EVIDENCE / "observations"')
source = source.replace('PROJECT / "policy-receipts"', 'EVIDENCE / "policy-receipts"')
source = source.replace('PROJECT / ("context-"', 'EVIDENCE / ("context-"')
source = source.replace('PROJECT.glob("context-*.json")', 'EVIDENCE.glob("context-*.json")')
source = source.replace('digest_file(PROJECT / name)', 'digest_file(EVIDENCE / name)')
source = source.replace('PROJECT.mkdir(parents=True, exist_ok=False)', '''assert PROJECT.is_dir()
    assert not (PROJECT / ".codex/hooks.json").exists()
    native_before = tomllib.loads(CONFIG.read_text(encoding="utf8"))
    trusted = {key: value for key, value in native_before.get("projects", {}).items()
        if str(Path(key).resolve()).casefold() == str(PROJECT.resolve()).casefold()}
    assert len(trusted) == 1 and next(iter(trusted.values()))["trust_level"] == "trusted"
    EVIDENCE.mkdir(parents=True, exist_ok=False)
    pipeline = read(DELIVERY / "revalidation-summary.json")
    assert pipeline["status"] == "completed-local-checks-native-retest-pending"
    assert pipeline["source_lock_hash"] == EXPECTED''')
source = source.replace('context_reference="context-allow.json"', 'context_reference=".nckh-native-r35-file/context-allow.json"')
source = source.replace('native-codex-file-r34', 'native-codex-file-r35')
source = source.replace('"source_revision": 34', '"source_revision": 35')
source = source.replace('"config_route": "invocation-only inline sessionFlags; no persisted project trust"',
    '"config_route": "inline sessionFlags; existing native-persisted workspace trust reused, no new key"')
source = source.replace('"global_parsed_hash": digest_record(native)', '"global_parsed_hash": digest_record(native), "global_hook_sha256": digest_file(Path(r"C:/Users/USER\\.codex\\hooks.json"))')
source = source.replace('"--project", str(PROJECT), "--runner", str(runner)', '"--project", str(PROJECT), "--evidence", str(EVIDENCE), "--runner", str(runner)')
source = source.replace('"private/file-protected-01.txt"', '"private/r35-file-protected-01.txt"')
source = source.replace('PROJECT / "cli-state/sqlite"', 'EVIDENCE / "cli-state/sqlite"')
source = source.replace('PROJECT / "cli-state/logs"', 'EVIDENCE / "cli-state/logs"')
source = source.split('\ndef cleanup():', 1)[0]
source += '''
def cleanup():
    receipt_path = RUN / "cleanup.json"
    if receipt_path.exists():
        raise RuntimeError("Preserve cleanup receipt")
    assert receipt_path.resolve().is_relative_to(RUN.resolve())
    definition = read(RUN / "definition.json")
    assert digest_file(CONFIG) == definition["global_config_sha256"]
    assert digest_file(Path(r"C:/Users/USER\\.codex\\hooks.json")) == definition["global_hook_sha256"]
    assert digest_record(tomllib.loads(CONFIG.read_text(encoding="utf8"))) == definition["global_parsed_hash"]
    for global_path in (CONFIG, Path(r"C:/Users/USER\\.codex\\hooks.json")):
        if global_path.is_file():
            text = global_path.read_text(encoding="utf8").casefold().replace("\\\\\\\\", "\\\\")
            if definition["runner"].casefold() in text or str(OBSERVER).casefold() in text:
                raise RuntimeError("Global hook references owned runtime; preserve payload")
    for member in definition["staged_members"]:
        assert digest_file(contained(PROJECT, member["path"])) == member["sha256"]
    for member in definition["staged_members"]:
        contained(PROJECT, member["path"]).unlink()
    atomic_json(receipt_path, {"status": "pass", "removed_members": definition["staged_members"],
        "config_callable": (PROJECT / ".codex/hooks.json").exists(), "global_config_unchanged": True,
        "global_hook_unchanged": True, "global_direct_write": False, "workspace_trust": "existing native key retained",
        "new_project_trust_keys": 0, "native_observer_receipts_retained": True})
    print(json.dumps({"status": "cleaned", "members": len(definition["staged_members"])}), flush=True)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "cleanup-only":
        cleanup()
        sys.exit(0)
    if (RUN / "native-file-summary.json").exists():
        raise RuntimeError("Preserve earlier batch")
    prepare()
    results = []
    try:
        for mode, relative, attempt in (("allow", "oracles/r35-file-allow-01.txt", "r35-file-allow-01"),
            ("policy-deny", "oracles/r35-file-policy-deny-01.txt", "r35-file-policy-deny-01"),
            ("allow", "private/r35-file-protected-01.txt", "r35-file-protected-01"),
            ("uncovered-tool", "oracles/r35-file-uncovered-01.txt", "r35-file-uncovered-01")):
            row = observe(mode, relative, attempt)
            selected = [item for item in row["native_callbacks"] if item["event"] == "PreToolUse"]
            results.append({"attempt": attempt, "mode": mode, "marker": row["marker_exists"],
                "pretool_callbacks": len(selected), "receipt": bind(RUN / "attempts" / (attempt + ".json"))})
            atomic_json(RUN / "native-file-summary.json", {"status": "running", "results": results,
                "source_revision": 35, "source_lock_hash": EXPECTED})
            if not selected:
                raise RuntimeError("Native pretool unobserved; do not claim prevention")
        atomic_json(RUN / "native-file-summary.json", {"status": "recorded-native-file-attempts",
            "results": results, "source_revision": 35, "source_lock_hash": EXPECTED})
    finally:
        cleanup()
'''
compile(source, str(NEW / "codex-native-files.py"), "exec")
(NEW / "codex-native-files.py").write_text(source, encoding="utf8", newline="\n")
observer = (OLD / "codex-file-observer.py").read_text(encoding="utf8")
observer = observer.replace('parser.add_argument("--runner",', 'parser.add_argument("--evidence", type=Path, required=True)\nparser.add_argument("--runner",')
observer = observer.replace('args.project / "control.json"', 'args.evidence / "control.json"')
observer = observer.replace('args.project / "observations"', 'args.evidence / "observations"')
observer = observer.replace('"--context", context, "--receipt-dir", "policy-receipts/"',
    '"--context", (args.evidence.relative_to(args.project) / context).as_posix(), "--receipt-dir", args.evidence.relative_to(args.project).as_posix() + "/policy-receipts/"')
compile(observer, str(NEW / "codex-file-observer.py"), "exec")
(NEW / "codex-file-observer.py").write_text(observer, encoding="utf8", newline="\n")
print(json.dumps({"status": "prepared-helpers-only", "reused_project": str(OLD / "project-02"),
    "native_models": "gpt-5.6-luna medium", "staging_and_inference": "not-performed"}))
