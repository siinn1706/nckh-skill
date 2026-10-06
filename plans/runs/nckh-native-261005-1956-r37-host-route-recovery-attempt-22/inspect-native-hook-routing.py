"""Retain bounded installed-source contexts; do not evaluate vendor code."""

import hashlib
import json
import re
from pathlib import Path

RUN = Path(__file__).resolve().parent
SOURCE = Path(r"C:/Users/USER\AppData\Local\cursor-agent\versions\2026.09.15-d2fe57e\index.js")
raw = SOURCE.read_bytes()
digest = hashlib.sha256(raw).hexdigest()
assert digest == "9f51ecf275d932372bf367914708b0dd21bf9c9e807b5e20e789ec9e247d9f86"
text = raw.decode("utf8")
patterns = [r"\.getPluginHooks\(", r"getPluginHooks\(", r"executeHookForStep", r"async [\w$]*[Hh]ook[\w$]*\("]
results = []
for pattern in patterns:
    matches = list(re.finditer(pattern, text))
    contexts = []
    for match in matches[:8]:
        start, end = max(0, match.start() - 420), min(len(text), match.end() + 1680)
        snippet = text[start:end]
        contexts.append({"start": start, "end": end, "match_start": match.start(), "text": snippet,
            "sha256_utf8": hashlib.sha256(snippet.encode("utf8")).hexdigest()})
    results.append({"pattern": pattern, "total_matches": len(matches), "retained_matches": len(contexts), "contexts": contexts})
record = {"status": "bounded-native-routing-source-observation", "source": str(SOURCE), "source_sha256": digest,
    "vendor_version": "2026.09.15-d2fe57e", "patterns": results, "vendor_code_evaluated": False,
    "vendor_source_modified": False, "native_callbacks_triggered": False,
    "scope_limit": "Text occurrence or missing regex match is not execution evidence or proof of method absence"}
with (RUN / "cursor-native-routing-contexts.json").open("x", encoding="utf8") as stream:
    json.dump(record, stream, ensure_ascii=False, indent=2)
    stream.write("\n")
print(json.dumps({"source_sha256": digest, "patterns": [{k:v for k,v in row.items() if k != "contexts"} for row in results]}))
