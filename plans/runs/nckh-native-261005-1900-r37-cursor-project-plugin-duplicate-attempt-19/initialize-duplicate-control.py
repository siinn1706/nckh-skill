"""Reuse reviewed native helpers without changing their historical artifacts."""

from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
BASE = WORK / "plans/runs/nckh-native-261005-1842-r37-cursor-private-create-attempt-18"
audit = (BASE / "audit-before-native.ps1").read_text(encoding="utf8")
needle = "    'nckh-native-261005-1755-r37-cursor-preflight-faults-attempt-17',"
assert audit.count(needle) == 1 and audit.count("$taskEarlierRuns[0..1]") == 1
audit = audit.replace(needle, needle + "\n    'nckh-native-261005-1842-r37-cursor-private-create-attempt-18',")
audit = audit.replace("$taskEarlierRuns[0..1]", "$taskEarlierRuns[0..2]")
with (RUN / "audit-before-native.ps1").open("x", encoding="utf8") as stream:
    stream.write(audit)
for name in ("capture-native-processes.ps1", "reconcile-native-processes.ps1", "cursor-agy-model-dangerous-grant.json"):
    with (RUN / name).open("xb") as stream:
        stream.write((BASE / name).read_bytes())
observer = WORK / "plans/runs/nckh-native-261005-1755-r37-cursor-preflight-faults-attempt-17/cursor-file-observer.py"
with (RUN / "cursor-file-observer.py").open("xb") as stream:
    stream.write(observer.read_bytes())
print("Reviewed helper copies prepared; native control not yet staged")
