"""Correct project versus hook trust claims without changing native evidence."""

import hashlib
import json
import shutil
import sys
import tomllib
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PLAN = WORK / "plans/261004-0047-nckh-research-data-hooks-writing"
FILE = RUN.parent / "nckh-native-261005-0658-r34-codex-file-attempt-01"
REPORT = WORK / "plans/reports/delivery-261005-0052-r34-codex-events"
CONFIG = Path(r"C:/Users/USER\.codex\config.toml")
PREIMAGES = RUN / "preimages/trust-report-correction"
RECEIPT = RUN / "trust-report-correction.json"
sys.path.insert(0, str(WORK / "nckh-kit"))
sys.dont_write_bytecode = True
from core.build import verify_source_lock
from core.paths import atomic_json, digest_file, digest_record

read = lambda path: json.loads(path.read_text(encoding="utf8"))
bind = lambda path: {"path": path.relative_to(WORK).as_posix(), "sha256": digest_file(path)}
if RECEIPT.exists() or PREIMAGES.exists():
    raise RuntimeError("Preserve the existing trust correction")
source_hash = digest_record(verify_source_lock(WORK / "nckh-kit"))
assert source_hash == "4482bbba7f4537025b523d887abe34774a4427d397549730f1ba8cf9fd50a255"
cleanup_path = RUN / "project/cleanup.json"
cleanup_hash = digest_file(cleanup_path)
cleanup = read(cleanup_path)
own_trust = cleanup["native_owned_project_trust"]
assert len(own_trust) == 1 and cleanup["global_direct_write"] is False
assert cleanup["persisted_hook_trust_mutation"] is False and cleanup["unrelated_global_config_unchanged"] is True
config_bytes = CONFIG.read_bytes()
native = tomllib.loads(config_bytes.decode("utf8"))
current_owned = {}
for project in (RUN / "project", FILE / "project-02"):
    matches = {key: value for key, value in native.get("projects", {}).items()
               if str(Path(key).resolve()).casefold() == str(project.resolve()).casefold()}
    assert len(matches) == 1 and next(iter(matches.values()))["trust_level"] == "trusted"
    current_owned.update(matches)
observation_path = RUN / "trust-observation-current.json"
atomic_json(observation_path, {"recorded_at": datetime.now(timezone.utc).isoformat(),
    "status": "observed-existing-native-owned-project-trust", "config_sha256": hashlib.sha256(config_bytes).hexdigest(),
    "native_owned_project_trust": current_owned, "global_direct_write": False,
    "historical_cleanup": bind(cleanup_path), "cleanup_receipt_unchanged": True,
    "meaning": "workspace/project trust persisted by native CLI; invocation-only hook bypass is separate"})

targets = [REPORT.with_suffix(".md"), REPORT.with_suffix(".json"), RUN / "write-codex-native-addendum.py",
    PLAN / "plan.md", PLAN / "phase-03-portable-hooks.md",
    WORK / "plans/journals/2026-10-05-nckh-r34-native-delivery-checkpoint.md",
    WORK / "plans/reports/delivery-261005-0658-r34-codex-file-failure.md"]
contents = {path: path.read_text(encoding="utf8") for path in targets}
PREIMAGES.mkdir(parents=True)
before = []
for index, path in enumerate(targets):
    image = PREIMAGES / (f"{index:02d}-" + path.name)
    shutil.copyfile(path, image)
    before.append({"original": bind(path), "preimage": bind(image)})

replacements = [
    ("global file không được edit.", "controller không edit trực tiếp global file; native CLI tự persist own workspace trust như cleanup receipt ghi."),
    ("Action chưa chạy, global trust không đổi. New specific approval request đã được gửi cho owner; không suy elapsed time là approval.",
     "Normal UI action này không chạy. CLI route sau đó tự persist exact own workspace/project trust key; cleanup receipt chứng minh thay đổi này. Report trước đã diễn giải nhầm workspace trust thành hook-definition trust. Không có approval mới được suy từ elapsed time."),
    ("Safer route dùng inline **sessionFlags** definitions cùng `--dangerously-bypass-hook-trust`, không lưu project trust.",
     "CLI route dùng inline **sessionFlags** definitions cùng `--dangerously-bypass-hook-trust`. Flag bypass hook-definition review cho invocation; native CLI vẫn tự lưu own workspace/project trust."),
    ("chưa attest persisted trust hoặc plugin support.", "Cleanup receipt ghi own workspace trust persisted; plugin support vẫn chưa observed."),
    ("Không thêm persisted native project trust; unrelated global config hash unchanged.",
     "Native CLI đã thêm exact own project trust key. Controller không direct-write global; hook-definition trust không persist. Unrelated parsed global state unchanged sau khi bỏ own key chỉ trong memory."),
    ("persisted project-trust route đang chờ explicit owner approval sau auto-review rejection; project/plugin duplicate và protected-path/other tools chưa qualified.",
     "normal UI trust rejection giữ trong history; native CLI đã persist own workspace trust. Project/plugin duplicate và protected-path/other tools chưa qualified."),
]
for path in (REPORT.with_suffix(".md"), RUN / "write-codex-native-addendum.py"):
    text = contents[path]
    for old, new in replacements:
        assert old in text, (path, old)
        text = text.replace(old, new)
    if path.suffix == ".py":
        text = text.replace('"persisted project-trust path needs approval after automatic reviewer rejection"',
            '"normal UI trust rejection retained; native workspace trust persisted separately from hook trust"')
        text = text.replace('"native_project_trust_change": "not-performed"',
            '"native_project_trust_change": "persisted-by-native-cli", "native_owned_project_trust": cleanup["native_owned_project_trust"], "global_direct_write": False, "persisted_hook_trust_mutation": False')
    else:
        text += "\n## Trust reporting correction\n\n[Correction receipt](../runs/nckh-native-261005-0052-r34-codex-attempt-01/trust-report-correction.json) preserves the original report/helper/document preimages and binds the unchanged native cleanup receipt plus current read-only observation. The prior report incorrectly stated that no project trust was persisted. Both this exec run and the later file run have native-owned workspace trust; hook-definition trust and controller direct writes remain distinct. Native callbacks/oracles and r34 source bindings are unchanged.\n"
    path.write_text(text, encoding="utf8", newline="\n")

record = json.loads(contents[REPORT.with_suffix(".json")])
assert record["native_project_trust_change"] == "not-performed"
record.update(native_project_trust_change="persisted-by-native-cli", native_owned_project_trust=own_trust,
    global_direct_write=False, persisted_hook_trust_mutation=False, unrelated_global_config_unchanged=True,
    trust_observation=bind(observation_path), trust_correction={"path": RECEIPT.relative_to(WORK).as_posix(),
        "classification": "reporting-correction; native observations unchanged"})
record["open_gates"] = ["normal UI trust rejection retained; native workspace trust persisted separately from hook trust"
    if gate == "persisted project-trust path needs approval after automatic reviewer rejection" else gate
    for gate in record["open_gates"]]
atomic_json(REPORT.with_suffix(".json"), record)

path = PLAN / "plan.md"
old = "Codex persisted project-trust route đang chờ specific approval sau automatic approval review rejection."
assert old in contents[path]
path.write_text(contents[path].replace(old,
    "Normal UI Codex trust step bị auto-review từ chối và không chạy; native dangerous CLI sau đó tự persist exact own workspace trust trong cả event/file projects. [Trust correction](../runs/nckh-native-261005-0052-r34-codex-attempt-01/trust-report-correction.json) giữ preimages và native receipts; hook-definition trust không persist, controller không ghi trực tiếp global. Existing trusted scratch projects có thể được reuse trong native grant; thêm trust keys mới vẫn cần specific authority."), encoding="utf8", newline="\n")

path = PLAN / "phase-03-portable-hooks.md"
text = contents[path]
old = "Inline `sessionFlags` definitions và native dangerous flags không ghi global trust."
assert old in text
text = text.replace(old, "Inline `sessionFlags` definitions bypass hook-definition trust cho invocation; native CLI tự persist exact own workspace/project trust key, controller không direct-write global.")
old = "Cleanup gỡ 26 matching payload members; config đã park vào evidence, unrelated global config hash unchanged;"
assert old in text
text = text.replace(old, "Cleanup gỡ 26 matching payload members; config đã park vào evidence, unrelated parsed global state unchanged sau khi bỏ own native trust key chỉ trong memory;")
old = "Claude model/effort và exact new persisted Codex project trust đang chờ human replies; trust action đã bị automatic approval review từ chối và chưa chạy."
assert old in text
text = text.replace(old, "Claude model/effort chưa có reply. Normal UI trust action bị automatic approval review từ chối và không chạy; native CLI route sau đó tự persist own workspace trust. [Trust correction](../runs/nckh-native-261005-0052-r34-codex-attempt-01/trust-report-correction.json) giữ report/helper preimages và unchanged native cleanup receipt; existing trusted scratch project được reuse theo native grant, thêm trust keys mới chưa authorized.")
path.write_text(text, encoding="utf8", newline="\n")

path = WORK / "plans/reports/delivery-261005-0658-r34-codex-file-failure.md"
old = "earlier r34 Codex addendum vẫn giữ exact earlier run của nó."
assert old in contents[path]
path.write_text(contents[path].replace(old, "[Earlier Codex addendum correction](./delivery-261005-0052-r34-codex-events.md) ghi rằng event run trước cũng đã native-persist own workspace trust; original report/helper preimages được giữ."), encoding="utf8", newline="\n")

path = WORK / "plans/journals/2026-10-05-nckh-r34-native-delivery-checkpoint.md"
path.write_text(contents[path] + "\n## Correction — workspace trust in the earlier Codex event run\n\nThe unchanged event-run cleanup receipt already recorded its own native project trust key. The event report/helper had incorrectly described invocation-only hook trust as absence of persisted workspace trust. Report, structured status and plan claims are now corrected with preimages retained. A current read-only check found both the event project and file project trusted. The normal UI trust action was rejected and did not run; the later native CLI route did persist workspace trust. The controller did not directly edit global state, and native callbacks/oracles are unchanged. Existing trusted scratch projects can be reused within the native grant; further trust additions need specific authority. AgentWiki publish skipped.\n", encoding="utf8", newline="\n")

assert digest_file(cleanup_path) == cleanup_hash
assert digest_file(CONFIG) == hashlib.sha256(config_bytes).hexdigest()
assert digest_record(verify_source_lock(WORK / "nckh-kit")) == source_hash
atomic_json(RECEIPT, {"recorded_at": datetime.now(timezone.utc).isoformat(), "status": "corrected-reporting-claims",
    "cause": "workspace/project trust was conflated with hook-definition trust",
    "source_revision": 35, "source_lock_hash": source_hash, "source_unchanged": True,
    "historical_native_revision": 34, "native_receipts_mutated": False, "global_direct_write": False,
    "native_owned_project_trust": own_trust, "evidence": [bind(cleanup_path), bind(observation_path)],
    "before": before, "after": [bind(path) for path in targets],
    "normal_ui_trust_step": "rejected-and-not-run", "native_cli_workspace_trust": "persisted",
    "hook_definition_trust_mutation": False, "native_checkbox": "unchecked", "plan_progress": "44/45"})
print(json.dumps({"status": "corrected-reporting-claims", "native_owned_trust_keys_observed": len(current_owned),
    "source_unchanged": True, "native_receipts_unchanged": True}))
