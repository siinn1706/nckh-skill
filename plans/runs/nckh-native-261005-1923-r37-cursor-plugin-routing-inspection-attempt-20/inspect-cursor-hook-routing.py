"""Read bounded vendor source excerpts; never execute or modify that source."""

import hashlib
import json
import re
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
INDEX = Path(r"C:/Users/USER\AppData\Local\cursor-agent\versions\2026.09.15-d2fe57e\index.js")
data = INDEX.read_bytes()
source = data.decode("utf8")
sha = lambda value: hashlib.sha256(value).hexdigest()
terms = ["beforeSubmitPrompt", "preToolUse", "sessionStart", "pluginHooks", "getPluginHooks", "getHooksForEvent", "getHooksByEvent", "plugin-dir"]
rows = []
for term in terms:
    matches = list(re.finditer(re.escape(term), source))
    excerpts = []
    for match in matches[:5]:
        start = max(0, match.start() - 220)
        end = min(len(source), match.end() + 380)
        excerpts.append({"character_start": start, "character_end": end, "match_start": match.start(),
            "text": source[start:end], "sha256_utf8": sha(source[start:end].encode("utf8"))})
    rows.append({"term": term, "match_count": len(matches), "excerpts": excerpts})
record = {"status": "bounded-read-only-vendor-source-observation", "source": str(INDEX), "source_sha256": sha(data),
    "source_bytes": len(data), "version_directory": INDEX.parent.name, "rows": rows,
    "vendor_source_modified": False, "vendor_code_evaluated": False, "model_prompts": 0,
    "interpretation": "Evidence only; observations do not alone qualify native callbacks or declare platform-wide support"}
with (RUN / "cursor-hook-source-excerpts.json").open("x", encoding="utf8") as stream:
    stream.write(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
baseline = WORK / "plans/runs/nckh-native-261005-1900-r37-cursor-project-plugin-duplicate-attempt-19/audit-before-native.ps1"
audit = baseline.read_text(encoding="utf8")
needle = "    'nckh-native-261005-1842-r37-cursor-private-create-attempt-18',"
assert audit.count(needle) == 1 and audit.count("$taskEarlierRuns[0..2]") == 1
audit = audit.replace(needle, needle + "\n    'nckh-native-261005-1900-r37-cursor-project-plugin-duplicate-attempt-19',")
audit = audit.replace("$taskEarlierRuns[0..2]", "$taskEarlierRuns[0..3]")
with (RUN / "audit-before-native.ps1").open("x", encoding="utf8") as stream:
    stream.write(audit)
print(json.dumps({"status": record["status"], "source_sha256": record["source_sha256"],
    "terms": [{"term": row["term"], "count": row["match_count"]} for row in rows]}))
for row in rows:
    if row["term"] in {"beforeSubmitPrompt", "pluginHooks", "getPluginHooks", "getHooksForEvent", "getHooksByEvent"}:
        print(json.dumps(row, ensure_ascii=False))
