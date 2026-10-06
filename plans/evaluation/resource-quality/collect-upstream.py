"""Fetch only the pinned shortlist files; never execute upstream code."""

import csv
import hashlib
import io
import json
import urllib.request
from pathlib import Path

STAGING = Path(__file__).resolve().parent / "staging"
SOURCES = [
    ("S1", "K-Dense-AI/scientific-agent-skills", "154988403bb5a18e9d3c0ce4e6d5e2e4b184a298", [
        "LICENSE.md", "skills/scientific-writing/assets/reporting_guidelines.json",
        "skills/scientific-visualization/assets/publisher_profiles.json"]),
    ("S2", "Yuan1z0825/nature-skills", "84880815fb37317b3766bff2c2abba395b8993c3", [
        "LICENSE", "skills/nature-writing/manifest.yaml", "skills/nature-writing/static/fragments/language/en.md"]),
    ("S3", "nextlevelbuilder/ui-ux-pro-max-skill", "09170eec67eefd46a7ae85de61b40c194020f997", [
        "LICENSE", "src/ui-ux-pro-max/data/ux-guidelines.csv"]),
]
EXPECTED = {
    "reporting_guidelines.json": "215f8c55bd40bda0569f2e81556030ff575319e25276b1e1ae70e2cc7475ddcd",
    "publisher_profiles.json": "1e1b1b5a4e0e3dfc57877f2abf1e96888fe6b65617234b078f193b8f76e0ebe9",
    "ux-guidelines.csv": "ff81ec613f70ba9fc3fcce52dbe4ae35d44b2079dbe6dc066d2d6e38c28facd5",
}


def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "NCKH-selective-resource-review"}), timeout=30) as response:
        data = response.read(2_000_001)
        if len(data) > 2_000_000:
            raise ValueError("shortlist response exceeds review bound")
        return data


records = []
for identity, repo, commit, files in SOURCES:
    tree_url = f"https://api.github.com/repos/{repo}/git/trees/{commit}?recursive=1"
    tree_bytes = fetch(tree_url)
    tree = json.loads(tree_bytes)
    if tree.get("truncated") or tree.get("sha") != commit:
        raise ValueError("incomplete or mismatched pinned repository tree")
    notices = [row["path"] for row in tree["tree"] if row["type"] == "blob" and
               any(word in Path(row["path"]).name.upper() for word in ["LICENSE", "LICENCE", "NOTICE", "COPYING"])]
    destination = STAGING / identity
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "tree-evidence.json").write_bytes(tree_bytes)
    members = []
    for relative in files:
        url = f"https://raw.githubusercontent.com/{repo}/{commit}/{relative}"
        data = fetch(url)
        digest = hashlib.sha256(data).hexdigest()
        if Path(relative).name in EXPECTED and digest != EXPECTED[Path(relative).name]:
            raise ValueError("selected resource differs from reviewed shortlist")
        path = destination / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        members.append({"path": relative, "sha256": digest, "bytes": len(data), "url": url})
    records.append({"source_id": identity, "repository": repo, "commit": commit,
                    "as_of": "2026-10-02", "tree_sha256": hashlib.sha256(tree_bytes).hexdigest(),
                    "license_notice_paths": notices, "files": members,
                    "status": "staged-for-file-review", "upstream_code_executed": False})
(STAGING / "source-inspection.json").write_text(json.dumps({"schema_version": 1, "sources": records}, indent=2) + "\n", encoding="utf-8")
print(json.dumps(records, indent=2))
