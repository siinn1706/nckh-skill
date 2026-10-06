"""Retain exact installer preview/transaction output for the project candidate."""
import argparse
import json
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


def parse_observation(text):
    decoder = json.JSONDecoder()
    documents = []
    remaining = text.lstrip()
    while remaining:
        document, end = decoder.raw_decode(remaining)
        documents.append(document)
        remaining = remaining[end:].lstrip()
    for document in reversed(documents):
        if isinstance(document, dict) and "status" in document:
            return document
    raise ValueError("installer output has no status object")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--commit", action="store_true")
    args = parser.parse_args()
    project = Path(__file__).resolve().parents[3]
    output = args.output.resolve()
    if not output.is_relative_to(project) or output.exists() and any(output.iterdir()):
        parser.error("select a fresh receipt directory inside test-skill")
    output.mkdir(parents=True, exist_ok=True)
    command = [sys.executable, "-B", str(project / "nckh-kit/installer/nckh-installer.py"),
        "update", "--package", str(args.package.resolve()), "--runtime", "codex-desktop",
        "--scope", "project", "--project", str(project), "--state-dir", str(project / ".nckh-state"),
        "--kits", "core", "engineer", "marketing", "--mode", "copy", "--models", "balanced",
        "--candidate-evidence", str(args.evidence.resolve()), "--yes" if args.commit else "--dry-run"]
    started = datetime.now(timezone.utc).isoformat()
    result = subprocess.run(command, cwd=project / "nckh-kit", capture_output=True)
    (output / "stdout.json").write_bytes(result.stdout)
    (output / "stderr.txt").write_bytes(result.stderr)
    receipt = {"command": command, "cwd": str(project / "nckh-kit"), "started_at": started,
        "finished_at": datetime.now(timezone.utc).isoformat(), "exit_status": result.returncode}
    (output / "command-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    try:
        observed = parse_observation((result.stdout or result.stderr).decode("utf-8-sig"))
        plan = observed.get("transaction", {})
        print(json.dumps({"status": observed.get("status"), "exit_status": result.returncode,
            "install_id": plan.get("install_id", observed.get("install_id")),
            "actions": dict(Counter(item["action"] for item in plan.get("entries", []))),
            "conflicts": plan.get("conflicts", []), "transaction_id": observed.get("transaction_id"),
            "error": observed.get("error"),
            "receipt_directory": str(output)}, indent=2))
    except ValueError:
        print("Installer returned unparsed output; inspect retained files.")
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
