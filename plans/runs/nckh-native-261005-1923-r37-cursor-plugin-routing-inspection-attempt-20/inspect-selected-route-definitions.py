"""Read only specific definitions selected from the first vendor observation."""

import hashlib
import json
import re
from pathlib import Path

RUN = Path(__file__).resolve().parent
first = json.loads((RUN / "cursor-hook-source-excerpts.json").read_text(encoding="utf8"))
data = Path(first["source"]).read_bytes()
assert hashlib.sha256(data).hexdigest() == first["source_sha256"]
source = data.decode("utf8")
selected = []
patterns = [("executeHookForStep definition", r"executeHookForStep\([^)]*\)\{", 7200),
    ("getPluginHooks definition", r"async getPluginHooks\([^)]*\)\{", 2800),
    ("hook name normalization", r"s=\{PreToolUse:n\.preToolUse", 2800)]
for label, pattern, limit in patterns:
    matches = list(re.finditer(pattern, source))
    for match in matches[:2]:
        start = max(0, match.start() - 100)
        end = min(len(source), match.end() + limit)
        selected.append({"label": label, "match_count": len(matches), "character_start": start, "character_end": end,
            "text": source[start:end], "sha256_utf8": hashlib.sha256(source[start:end].encode("utf8")).hexdigest()})
counts = {term: source.count(term) for term in ["getPluginHooks", "pluginHook", "pluginHookConfigs", "hookConfigs",
    "loadHooks", "reloadHooks", "UserPromptSubmit", "forceReload", "getHookConfigurations", "loadHookConfigs"]}
record = {"status": "bounded-selected-route-definitions", "source": first["source"], "source_sha256": first["source_sha256"],
    "definitions": selected, "term_counts": counts, "vendor_code_evaluated": False, "vendor_source_modified": False}
with (RUN / "cursor-selected-route-definitions.json").open("x", encoding="utf8") as stream:
    stream.write(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(record, ensure_ascii=False))
