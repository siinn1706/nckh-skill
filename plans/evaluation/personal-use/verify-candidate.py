"""Retain actual frozen-source checks and bind their stated scope to a candidate."""

import argparse
import json
import re
import sys
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    project = Path(__file__).resolve().parents[3]
    kit = project / "nckh-kit"
    output = args.output.resolve()
    if not output.is_relative_to(project.resolve()) or output == project.resolve():
        parser.error("output must be a fresh directory inside test-skill")
    if output.exists() and any(output.iterdir()):
        parser.error("preserve previous attempts; select a fresh output directory")
    effective_temp = Path(tempfile.gettempdir()).resolve()
    if effective_temp.is_relative_to(project.resolve()):
        parser.error("effective temporary directory is inside test-skill; use the normal external system temp directory before running checks")
    output.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(kit))
    from core.build import load_json, verify_bundle, verify_source_lock
    from core.paths import digest_bytes, digest_file, digest_record, temporary_tree
    from core.processes import run_owned_command

    source = verify_source_lock(kit)
    source_hash = digest_record(source)
    attempts = []

    def run(name, arguments, cwd=kit, *, require_success=True):
        command = [sys.executable, "-B", *map(str, arguments)]
        started = datetime.now(timezone.utc).isoformat()
        print("Running " + name, flush=True)
        stdout = output / (name + ".stdout.txt")
        stderr = output / (name + ".stderr.txt")
        record = {"name": name, "command": command, "cwd": str(cwd),
                  "started_at": started, "status": "starting", "pid": None,
                  "exit_status": None, "process_cleanup": "not-started",
                  "timeout_seconds": None, "stdout": str(stdout), "stderr": str(stderr)}
        attempts.append(record)
        write_json(output / "attempts.json", attempts)

        def on_started(pid):
            record.update(pid=pid, status="running", process_cleanup="pending",
                          process_started_at=datetime.now(timezone.utc).isoformat())
            write_json(output / "attempts.json", attempts)

        try:
            result = run_owned_command(command, cwd, b"", stdout, stderr,
                                       timeout=None, on_started=on_started)
            record.update(result)
        except (Exception, KeyboardInterrupt) as error:
            record.update(status="interrupted" if isinstance(error, KeyboardInterrupt) else "fail",
                          error=str(error), process_cleanup="unverified-after-lifecycle-error")
            raise
        finally:
            record["finished_at"] = datetime.now(timezone.utc).isoformat()
            for stream, path in (("stdout", stdout), ("stderr", stderr)):
                if path.is_file():
                    record[stream + "_sha256"] = digest_file(path)
            write_json(output / "attempts.json", attempts)
        if require_success and record["exit_status"] != 0:
            print(stderr.read_text(encoding="utf-8", errors="replace")[-6000:], flush=True)
            raise RuntimeError(name + " failed; retained actual output")
        if digest_record(verify_source_lock(kit)) != source_hash:
            raise RuntimeError("source changed during checks")
        return record

    def suite_receipt(record):
        stdout = Path(record["stdout"]).read_bytes()
        stderr = Path(record["stderr"]).read_bytes()
        combined = stdout + stderr
        text = combined.decode("utf-8", errors="replace")
        counts = re.findall(r"(?m)^Ran (\d+) tests? in ([0-9.]+)s\s*$", text)
        verdicts = re.findall(r"(?m)^(OK|FAILED)(?: \(([^\r\n]*)\))?\s*$", text)
        tests = int(counts[-1][0]) if counts else None
        verdict, details = verdicts[-1] if verdicts else (None, "")
        counters = {key: int(value) for key, value in re.findall(
            r"(failures|errors|skipped|expected failures|unexpected successes)=(\d+)", details)}
        status = "pass" if (record["exit_status"] == 0 and tests and verdict == "OK") else "fail"
        deterministic = {"status": status, "command": record["command"],
                         "exit_status": record["exit_status"], "tests": tests,
                         "failures": counters.get("failures", 0) if verdict else None,
                         "errors": counters.get("errors", 0) if verdict else None,
                         "skipped": counters.get("skipped", 0) if verdict else None,
                         "expected_failures": counters.get("expected failures", 0) if verdict else None,
                         "unexpected_successes": counters.get("unexpected successes", 0) if verdict else None,
                         "unittest_verdict": verdict,
                         "reported_seconds": float(counts[-1][1]) if counts else None,
                         "stdout": record["stdout"], "stderr": record["stderr"],
                         "stdout_sha256": digest_bytes(stdout), "stderr_sha256": digest_bytes(stderr),
                         "output_sha256": digest_bytes(combined), "pid": record["pid"],
                         "process_cleanup": record["process_cleanup"], "timeout_seconds": None,
                         "started_at": record["started_at"], "finished_at": record["finished_at"]}
        structure = load_json(output / "structure-validation.json")
        receipt = {**structure, "evidence_class": "deterministic", "status": status,
                   "scope": "frozen source structure validation and direct full unittest discovery without a suite timeout",
                   "source_lock_hash": source_hash, "recorded_at": datetime.now(timezone.utc).isoformat(),
                   "environment": {"python": sys.version.split()[0], "platform": sys.platform,
                                   "effective_temp": str(effective_temp)}, "deterministic": deterministic}
        write_json(output / "full-suite.json", receipt)
        return receipt

    try:
        run("structure-validation", ["evals/run-evals.py", "--validate-only", "--output", output / "structure-validation.json"])
        if load_json(output / "structure-validation.json").get("status") != "pass":
            raise RuntimeError("structure validation did not pass")
        full_suite = run("full-suite", ["-m", "unittest", "discover", "-s", "tests",
                                        "-p", "test_*.py", "-v"], require_success=False)
        if suite_receipt(full_suite)["status"] != "pass":
            raise RuntimeError("full suite failed or did not report completed test discovery; retained actual output")
        for access in ("on", "off"):
            run("reproducible-" + access, ["scripts/build-artifacts.py", "--all", "--check", "--resource-access", access])
            run("build-" + access, ["scripts/build-artifacts.py", "--all", "--resource-access", access,
                                     "--output", output / "bundles" / access])
        manifests = {}
        for host in ("claude", "codex", "cursor", "agy"):
            manifests[host] = verify_bundle(output / "bundles" / "on" / host)
            off = verify_bundle(output / "bundles" / "off" / host)
            if off["source_lock_hash"] != manifests[host]["source_lock_hash"]:
                raise RuntimeError("resource on/off source mismatch")
        archive = output / ("nckh-personal-use-r" + source["revision"] + ".zip")
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as packed:
            for path in sorted((output / "bundles" / "on").rglob("*")):
                if path.is_file():
                    packed.write(path, path.relative_to(output / "bundles" / "on").as_posix())
        with temporary_tree() as isolated:
            extracted = isolated / "extracted"
            with zipfile.ZipFile(archive) as packed:
                packed.extractall(extracted)
            outside_cwd = isolated / "cwd"
            outside_cwd.mkdir()
            for host in manifests:
                run("extracted-smoke-" + host, ["scripts/resource-smoke.py", "--bundle", extracted / host,
                    "--cwd", outside_cwd, "--unset-pythonpath", "--output", output / ("extracted-smoke-" + host + ".json")])
        affected = sorted({skill["id"] for manifest in manifests.values() for skill in manifest["skills"]}
                          | {agent["id"] for manifest in manifests.values() for agent in manifest["agents"]})
        closures = {host: manifest["closure_hash"] for host, manifest in manifests.items()}
        locks = {host: manifest["source_lock_hash"] for host, manifest in manifests.items()}
        limitations = ["Source/package checks only; no model, native host or owner acceptance.",
                       "Deterministic suites include fixtures; they are not human gold or scientific evidence.",
                       "On/off reproducibility and extracted reads do not prove resource benefit."]
        receipt = {"schema_version": 1, "evidence_class": "deterministic", "input_class": "owned-source",
                   "scope": "frozen source structure validation, direct full unittest suite without timeout, four-host on/off builds and extracted resource reads",
                   "status": "pass", "command": [sys.executable, "-B", str(Path(__file__).resolve()),
                       "--output", str(output)], "exit_status": 0, "closure_hashes": closures,
                   "source_lock_hashes": locks, "affected_skills": affected, "limitations": limitations}
        check_path = output / "candidate-check-receipt.json"
        write_json(check_path, receipt)
        evidence = {"schema_version": 1, "evidence_class": "deterministic", "qualification": "accepted-for-scope",
                    "closure_hashes": closures, "source_lock_hashes": locks, "affected_skills": affected,
                    "checks": [{"id": "frozen-source-package-checks", "result": "pass", "receipt": str(check_path),
                                "receipt_sha256": digest_file(check_path)}]}
        write_json(output / "candidate-evidence.json", evidence)
        summary = {"status": "pass", "revision": source["revision"], "source_lock_hash": source_hash,
                   "archive": str(archive), "archive_sha256": digest_file(archive), "host_count": len(manifests),
                   "skills": len(manifests["codex"]["skills"]), "checks": len(attempts),
                   "owner_review": "pending-user-use", "native_qualification": "not-established-by-these-checks"}
        write_json(output / "summary.json", summary)
        print(json.dumps(summary, indent=2), flush=True)
        return 0
    except (Exception, KeyboardInterrupt) as error:
        suite_attempt = next((record for record in reversed(attempts) if record["name"] == "full-suite"), None)
        if (suite_attempt and not (output / "full-suite.json").exists()
                and Path(suite_attempt["stdout"]).is_file()
                and Path(suite_attempt["stderr"]).is_file()):
            try:
                suite_receipt(suite_attempt)
            except Exception as receipt_error:
                suite_attempt["receipt_error"] = str(receipt_error)
                write_json(output / "attempts.json", attempts)
        write_json(output / "failure.json", {"status": "interrupted" if isinstance(error, KeyboardInterrupt) else "fail",
                                           "error": str(error), "source_lock_hash": source_hash,
                                           "revision": source["revision"], "attempt_count": len(attempts)})
        print(str(error), file=sys.stderr, flush=True)
        return 3


if __name__ == "__main__":
    sys.exit(main())
