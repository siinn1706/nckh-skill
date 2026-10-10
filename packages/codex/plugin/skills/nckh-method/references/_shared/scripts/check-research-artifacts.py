"""Check contained scientific artifact graphs; never execute recorded commands."""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
from core.experiments import validate_experiment_manifest
from core.paths import contained
from core.research_io import ArtifactReader
from core.schema import ContractError

def main():
    # The receipt bytes are UTF-8; emit them unchanged even when the console default is a legacy code page.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--task", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        if not args.project.is_absolute() or not args.project.is_dir():
            raise ContractError("project must be an existing absolute authorized root")
        reader = ArtifactReader(args.project)
        record = reader.json(args.manifest)
        if record["task_id"] != args.task:
            raise ContractError("checker task differs from manifest")
        result = validate_experiment_manifest(record, project=args.project, reader=reader)
        destination = contained(args.project, args.output)
        if destination.exists():
            raise ContractError("preserve prior artifact; output must be a fresh receipt path")
        report = {"schema_version": 1, "task_id": args.task, "manifest": args.manifest, "checks": result,
                  "read_only": True, "commands_executed": False, "scientific_acceptance": "pending"}
        data = reader.output(report, newline=True)
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("xb") as stream:
            stream.write(data)
        sys.stdout.write(data.decode("utf-8"))
        return 0
    except (ContractError, OSError, KeyError, TypeError) as error:
        sys.stderr.write(str(error) + "\n")
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
