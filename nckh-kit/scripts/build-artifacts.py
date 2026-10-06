import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from core.build import build_host
from core.paths import temporary_tree
from core.schema import ContractError


def main():
    parser = argparse.ArgumentParser(description="Build pinned self-contained artifacts; never install or invoke models.")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--host", choices=["claude", "codex", "cursor", "agy"])
    parser.add_argument("--kits", nargs="+", choices=["core", "engineer", "marketing"], default=["core", "engineer", "marketing"])
    parser.add_argument("--check", action="store_true", help="Build twice in temporary staging and check reproducibility.")
    parser.add_argument("--plugin", action="store_true", help="Also export an optional plugin projection; never register, enable or trust it.")
    parser.add_argument("--resource-access", choices=["on", "off"], default="on", help="Freeze resource availability for a same-base comparison.")
    parser.add_argument("--output", type=Path, help="Empty owned output directory (required without --check).")
    args = parser.parse_args()
    if args.all == bool(args.host):
        parser.error("select exactly one of --all or --host")
    if not args.check and args.output is None:
        parser.error("--output is required without --check")
    root = Path(__file__).resolve().parents[1]
    hosts = ["claude", "codex", "cursor", "agy"] if args.all else [args.host]
    summaries = []
    try:
        for host in hosts:
            if args.check:
                with temporary_tree() as first, temporary_tree() as second:
                    a = build_host(root, host, args.kits, first, include_plugin=args.plugin, include_resources=args.resource_access == "on")
                    b = build_host(root, host, args.kits, second, include_plugin=args.plugin, include_resources=args.resource_access == "on")
                    if a != b:
                        raise ContractError(f"non-reproducible artifact: {host}")
            else:
                a = build_host(root, host, args.kits, args.output / host, include_plugin=args.plugin, include_resources=args.resource_access == "on")
            summaries.append({"host": host, "skills": len(a["skills"]), "files": len(a["files"]),
                              "closure_hash": a["closure_hash"], "reproducible": args.check,
                              "native_qualification": "unverified"})
        print(json.dumps({"status": "pass", "evidence_class": "static", "artifacts": summaries}, indent=2))
        return 0
    except (ContractError, OSError, ValueError) as error:
        print(json.dumps({"status": "fail", "error": str(error)}), file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
