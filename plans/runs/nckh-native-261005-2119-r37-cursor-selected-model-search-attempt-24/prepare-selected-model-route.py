"""Reuse the frozen search oracle with observed existing CLI model selection."""

import json
import subprocess
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
BASE = WORK / "plans/runs/nckh-native-261005-2004-r37-cursor-uncovered-search-attempt-23"
read = lambda p: json.loads(p.read_text(encoding="utf8"))
assert read(BASE / "native-admission-summary.json")["status"] == "verified-model-admission-rejected-no-prompt-native-search-unqualified"
assert read(BASE / "cleanup.json")["status"] == "pass" and read(BASE / "final-process-audit.json")["matching_count"] == 0
for name in ("audit-before-native.ps1", "record-uncovered-search.py"):
    with (RUN / name).open("xb") as stream:
        stream.write((BASE / name).read_bytes())
source = (BASE / "prepare-uncovered-search.py").read_text(encoding="utf8")
source = source.replace("uncovered-search-23", "selected-model-search-24")
source = source.replace("SEARCH_MARKER_23", "SEARCH_MARKER_24").replace("SEARCH_FINISHED_23", "SEARCH_FINISHED_24")
old = 'source = original.replace(".nckh-native-r37-cursor-plugin-alias-21", ".nckh-native-r37-cursor-selected-model-search-24")'
assert source.count(old) == 1
source = source.replace(old, old + '\nsource = source.replace(\'"command_model": MODEL,\', \'"requested_model": MODEL, "model_selection_source": "existing CLI selectedModel; --model omitted",\')')
needle = 'probe.prepare()\nstage = read(RUN / "stage.json")'
replacement = ('probe.prepare()\n'
    'metadata = read(RUN / "native-metadata.json")\n'
    'parameters = {p["id"]:p["value"] for p in metadata["selected_model"]["parameters"]}\n'
    'assert metadata["selected_model"]["modelId"] == "grok-4.7"\n'
    'assert parameters == {"context":"500k", "reasoning_effort":"xhigh", "fast":"false"}\n'
    'capture_path = RUN / "capture-native-processes.ps1"\n'
    'capture_text = capture_path.read_text(encoding="utf8")\n'
    'old_command = "Cursor interactive: --force --trust --sandbox disabled --workspace owned project --model granted Grok 4.7 500k xhigh"\n'
    'assert capture_text.count(old_command) == 1\n'
    'capture_path.write_text(capture_text.replace(old_command, "Cursor interactive: --force --trust --sandbox disabled --workspace owned project; granted model through existing selectedModel"), encoding="utf8")\n'
    'stage = read(RUN / "stage.json")')
assert source.count(needle) == 1
source = source.replace(needle, replacement)
source = source.replace('"global_direct_write": False, "installed_update": "not-performed",',
    '"global_direct_write": False, "installed_update": "not-performed",\n    "model_selection_source": "existing CLI selectedModel; --model omitted", "UI_model_check_required_before_prompt": True,\n    "previous_admission_failure": probe.bind(WORK / "plans/runs/nckh-native-261005-2004-r37-cursor-uncovered-search-attempt-23/native-admission-summary.json"),')
target = RUN / "prepare-uncovered-search.py"
compile(source, str(target), "exec")
with target.open("x", encoding="utf8") as stream:
    stream.write(source)
audit = subprocess.run(["pwsh", "-NoProfile", "-File", str(RUN / "audit-before-native.ps1"), "-Stage", "prepare"], capture_output=True, text=True, encoding="utf8")
with (RUN / "prepare-preflight-command.json").open("x", encoding="utf8") as stream:
    json.dump({"exit_code":audit.returncode,"stdout":audit.stdout,"stderr":audit.stderr},stream,indent=2)
assert audit.returncode == 0, audit.stderr
result = subprocess.run([sys.executable, "-B", str(target)], cwd=WORK, capture_output=True, text=True, encoding="utf8")
with (RUN / "prepare-command.json").open("x", encoding="utf8") as stream:
    json.dump({"exit_code":result.returncode,"stdout":result.stdout,"stderr":result.stderr},stream,indent=2)
print(result.stdout, end="")
if result.stderr:
    print(result.stderr, file=sys.stderr, end="")
sys.exit(result.returncode)
