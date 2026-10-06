import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from core.build import freeze_sources
from core.paths import digest_file


def main():
    parser = argparse.ArgumentParser(description="Freeze owner-reviewed original source; no third-party copying or release authorization.")
    parser.add_argument("--write", action="store_true", required=True)
    parser.add_argument("--inspiration", type=Path, action="append", default=[])
    args = parser.parse_args()
    inspirations = [{"id": p.parent.name, "source_sha256": digest_file(p),
                     "inspection": "selected installed instructions", "reuse": "design inspiration only",
                     "redistribution": "not-cleared/not-copied"} for p in args.inspiration] if args.inspiration else None
    result = freeze_sources(Path(__file__).resolve().parents[1], inspirations)
    print(json.dumps({"frozen_files": len(result["files"]), "release_rights": result["release_rights"]}))


if __name__ == "__main__":
    main()
