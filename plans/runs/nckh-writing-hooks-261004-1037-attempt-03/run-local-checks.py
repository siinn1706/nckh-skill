import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[2] / "nckh-kit"
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True
os.environ["PYTHONUTF8"] = "1"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

from core.build import verify_source_lock
from core.paths import atomic_json, digest_file, digest_record
from core.processes import run_owned_command

parser = argparse.ArgumentParser()
parser.add_argument("stage", choices=("installer", "deterministic"))
args = parser.parse_args()
lock = verify_source_lock(ROOT)
assert lock["revision"] == "29"
source_hash = digest_record(lock)
name = args.stage + "-frozen"
receipt_path = RUN / (name + ".process.json")
if receipt_path.exists():
    raise RuntimeError("Preserve existing process receipt")
prefix = [sys.executable, "-X", "utf8", "-B"]
if args.stage == "installer":
    argv = prefix + ["-m", "unittest",
        "tests.installer.test_transactions.TransactionTests.test_shared_consumers_need_qualification_and_survive_other_uninstall",
        "tests.installer.test_transactions.TransactionTests.test_native_model_config_is_owned_transaction_and_uninstall_preserves_user_edit",
        "-v"]
else:
    if (RUN / "deterministic.json").exists():
        raise RuntimeError("Preserve existing deterministic result")
    argv = prefix + [str(ROOT / "evals/run-evals.py"), "--run-deterministic", "--output", str(RUN / "deterministic.json")]
receipt = {"schema_version": 1, "status": "starting", "stage": args.stage,
    "argv": argv, "cwd": str(ROOT), "port": None, "source_revision": "29",
    "source_lock_hash": source_hash, "started_at": datetime.now(timezone.utc).isoformat()}
def started(pid):
    receipt.update(pid=pid, status="running")
    atomic_json(receipt_path, receipt)
stdout, stderr = RUN / (name + ".stdout"), RUN / (name + ".stderr")
outcome = run_owned_command(argv, ROOT, b"", stdout, stderr, timeout=None, on_started=started)
receipt.update(outcome, ended_at=datetime.now(timezone.utc).isoformat(),
    stdout_sha256=digest_file(stdout), stderr_sha256=digest_file(stderr),
    source_unchanged=digest_record(verify_source_lock(ROOT)) == source_hash)
atomic_json(receipt_path, receipt)
print(name + ": exit " + str(outcome["exit_status"]))
sys.exit(outcome["exit_status"] if outcome["exit_status"] is not None else 3)
