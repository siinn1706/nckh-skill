"""Read bounded installed-vendor snippets without evaluating or changing vendor code."""

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PREVIOUS = WORK / "plans/runs/nckh-native-261005-1923-r37-cursor-plugin-routing-inspection-attempt-20/cursor-hook-source-excerpts.json"
previous = json.loads(PREVIOUS.read_text(encoding="utf8"))
source_path = Path(previous["source"])
raw = source_path.read_bytes()
digest = hashlib.sha256(raw).hexdigest()
assert digest == previous["source_sha256"], "Installed vendor source changed; revise scope before inspection"
source = raw.decode("utf8")
rows = []
for term in ("workspaceOpen", "pluginPaths", "runWorkspaceOpen", "setWorkspacePlugin", "setExtensionPlugins"):
    matches = list(re.finditer(re.escape(term), source))
    snippets = []
    for match in matches[:6]:
        start = max(0, match.start() - 300)
        end = min(len(source), match.end() + 650)
        snippet = source[start:end]
        snippets.append({"start": start, "end": end, "match_start": match.start(), "text": snippet,
            "sha256_utf8": hashlib.sha256(snippet.encode()).hexdigest()})
    rows.append({"term": term, "match_count": len(matches), "snippets": snippets})
record = {
    "status": "bounded-readonly-workspace-plugin-route-inspection",
    "timestamp_utc": datetime.now(timezone.utc).isoformat(), "source": str(source_path),
    "source_sha256": digest, "source_bytes": len(raw), "rows": rows,
    "official_reference": "https://cursor.com/docs/hooks#workspaceopen",
    "vendor_source_modified": False, "vendor_code_evaluated": False,
    "model_prompts": 0, "native_workspace_callback": "not-observed-by-this-inspection",
    "qualification": "Source presence or absence alone does not establish supported callback delivery",
}
with (RUN / "workspace-hook-source-excerpts.json").open("x", encoding="utf8") as stream:
    stream.write(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": record["status"], "source_sha256": digest,
    "terms": [{"term": row["term"], "matches": row["match_count"]} for row in rows]}))
for row in rows:
    if row["term"] == "pluginPaths":
        for snippet in row["snippets"]:
            print(json.dumps(snippet, ensure_ascii=False))
