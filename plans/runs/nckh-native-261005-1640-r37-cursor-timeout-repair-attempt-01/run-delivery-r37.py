import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
PROJECT = RUN.parents[2]
ROOT = PROJECT / "nckh-kit"
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True
os.environ.pop("PYTHONPATH", None)
os.environ["PYTHONUTF8"] = "1"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

from core.build import load_json, verify_bundle, verify_source_lock
from core.install import SURFACE_HOST
from core.paths import atomic_json, contained, digest_bytes, digest_file, digest_record, no_links
from core.processes import run_owned_command
from tests.hooks.test_runner import payload

VARIANTS = ("on-standalone", "off-standalone", "on-plugin", "off-plugin")
HOSTS = ("claude", "codex", "cursor", "agy")
WRITERS = ("nckh-humanwrite", "nckh-paperwrite")
VIZ = Path(r"C:/Users/USER\.codex\visualizations\2026\10\04\01a104fc-f969-7f43-b1e0-1a6774f0e0c8")
OUTSIDE = VIZ / "nckh-hooks-r37-1640-attempt-01"


def now():
    return datetime.now(timezone.utc).isoformat()


def fresh(path):
    path = no_links(path)
    if path.exists():
        raise RuntimeError("preserve existing attempt path: " + str(path))
    path.mkdir(parents=True)
    return path


def snapshot(root):
    return {p.relative_to(root).as_posix(): digest_file(p) for p in root.rglob("*") if p.is_file()}


def command(name, argv, *, cwd=ROOT, stdin=b"", json_output=True):
    directory = RUN / "commands"
    directory.mkdir(exist_ok=True)
    stdout, stderr, receipt_path = (directory / (name + suffix) for suffix in (".stdout", ".stderr", ".json"))
    if receipt_path.exists():
        raise RuntimeError("command attempt exists: " + name)
    receipt = {"schema_version": 1, "name": name, "argv": [str(arg) for arg in argv], "cwd": str(cwd),
               "started_at": now(), "status": "starting", "port": None, "work_context": str(PROJECT)}
    def started(pid):
        receipt.update(pid=pid, status="running")
        atomic_json(receipt_path, receipt)
    outcome = run_owned_command(receipt["argv"], cwd, stdin, stdout, stderr, timeout=None, on_started=started)
    receipt.update(outcome, ended_at=now(), stdout_sha256=digest_file(stdout), stderr_sha256=digest_file(stderr))
    atomic_json(receipt_path, receipt)
    print(name + ": exit " + str(outcome["exit_status"]), flush=True)
    if outcome["exit_status"] != 0:
        raise RuntimeError("delivery command failed: " + name)
    return load_json(stdout) if json_output else stdout.read_bytes()


def build():
    lock = verify_source_lock(ROOT)
    if lock["revision"] != "37":
        raise RuntimeError("fresh attempt must explicitly select its source revision")
    fresh(OUTSIDE)
    for subdir in ("cwd", "extracted", "project", "home"):
        fresh(OUTSIDE / subdir)
    context = {"schema_version": 1, "recorded_at": now(), "status": "building", "owner": "/root",
               "source_revision": lock["revision"], "source_lock_hash": digest_record(lock),
               "source_lock_file_sha256": digest_file(ROOT / "core/registry/source-lock/source-lock.json"),
               "run": str(RUN), "source": str(ROOT), "outside": str(OUTSIDE), "outside_cwd": str(OUTSIDE / "cwd"),
               "variants": list(VARIANTS), "hosts": list(HOSTS), "native": "unverified", "human": "accepted-exact-r29-writer-samples"}
    atomic_json(RUN / "delivery-context.json", context)
    atomic_json(OUTSIDE / "owned-attempt.json", context)
    artifacts = []
    for variant in VARIANTS:
        args = ["--all", "--resource-access", variant.split("-", 1)[0]]
        if variant.endswith("plugin"):
            args.append("--plugin")
        check = command("reproducibility-" + variant,
                        [sys.executable, "-X", "utf8", "-B", ROOT / "scripts/build-artifacts.py", *args, "--check"])
        assert check["status"] == "pass" and len(check["artifacts"]) == 4
        destination = RUN / "build" / variant
        result = command("build-" + variant, [sys.executable, "-X", "utf8", "-B", ROOT / "scripts/build-artifacts.py",
                                             *args, "--output", destination])
        assert result["status"] == "pass"
        for host in HOSTS:
            manifest = verify_bundle(destination / host)
            assert len(manifest["skills"]) == 39 and manifest["source_lock_hash"] == context["source_lock_hash"]
            artifacts.append({"variant": variant, "host": host, "bundle": str(destination / host),
                              "closure_hash": manifest["closure_hash"], "files": len(manifest["files"]),
                              "hook_members": len(manifest["hooks"]["members"]), "native": "unverified"})
    context.update(status="built", artifacts=artifacts, ended_at=now())
    atomic_json(RUN / "delivery-context.json", context)


def smoke():
    context = load_json(RUN / "delivery-context.json")
    assert context["status"] == "built" and context["source_lock_hash"] == digest_record(verify_source_lock(ROOT))
    results = []
    for variant in VARIANTS:
        for host in HOSTS:
            key = variant + "-" + host
            bundle = OUTSIDE / "extracted" / variant / host
            manifest = verify_bundle(bundle)
            archive = RUN / "archives" / (key + ".zip")
            receipt_dir = RUN / "receipts" / key
            fresh(receipt_dir)
            project = fresh(OUTSIDE / "project" / variant / host)
            atomic_json(project / "context.json", {"schema_version": 1, "task_id": "isolated-portability-observation",
                "tool_operations": {"Write": "write"}, "allowed_operations": ["write"], "brief": {"mode": "auto"}})
            before = snapshot(project)
            chain = {"schema_version": 1, "archive": str(archive), "archive_sha256": digest_file(archive),
                "bundle": str(bundle), "outside_cwd": str(OUTSIDE / "cwd"), "project": str(project),
                "source_lock_hash": manifest["source_lock_hash"], "closure_hash": manifest["closure_hash"],
                "bundle_manifest_hash": digest_record(manifest), "status": "verified-extracted", "native": "unverified"}
            atomic_json(receipt_dir / "archive-chain.json", chain)
            observed = command("resources-" + key, [sys.executable, "-I", ROOT / "scripts/resource-smoke.py",
                "--bundle", bundle, "--cwd", OUTSIDE / "cwd", "--unset-pythonpath", "--output", receipt_dir / "resource-smoke.json"])
            assert observed["status"] == "pass"
            readers = {row["path"].split("/")[1]: row["path"] for row in manifest["files"]
                       if row["path"].startswith("skills/") and row["source_path"] == "scripts/search-resource.py"}
            disabled = []
            if manifest["resource_access"] == "off":
                registry = load_json(ROOT / "core/registry/catalog/resources.json")["resources"]
                for writer in WRITERS:
                    for resource in registry:
                        if writer not in resource["consumers"] or resource["dependency"] != "required":
                            continue
                        item = command("disabled-" + key + "-" + writer + "-" + resource["resource_id"],
                            [sys.executable, "-I", bundle / readers[writer], "--resource-access", "off",
                             "--resource-id", resource["resource_id"], "--consumer", writer, "--domain", resource["domain"],
                             "--genre", resource["genre"], "--locale", resource["locale"], "--json"], cwd=OUTSIDE / "cwd")
                        assert item["status"] == "resource-disabled" and item["resource_read"] is False and item["records"] == []
                        disabled.append(item)
                assert len(disabled) == 6
            else:
                bindings = {(row["resource_id"], row["consumer"]) for row in observed["observations"]}
                assert all(sum(consumer == writer for _, consumer in bindings) == 3 for writer in WRITERS)
                assert ("R-worldbank-vietnam-population", "nckh-visuals") in bindings
            atomic_json(receipt_dir / "writer-disabled.json", {"status": "pass" if disabled else "not-applicable-on-bundle", "observations": disabled})
            hook = manifest["hooks"]
            event_name = "preToolUse" if host == "cursor" else "PreToolUse"
            packet = json.dumps(payload(project, host=host)).encode()
            neutral = {"schema_version": 1, "phase": "preflight", "host": host, "tool": "Write", "paths": ["private/input.md"],
                "session_key": digest_record("isolated"), "task_key": digest_record("isolated"),
                "artifact_sha256": digest_record(None), "stop_active": False}
            prefixes = [""] + ([hook["projection_root"] + "/"] if hook["projection_root"] != "not-projected" else [])
            for number, prefix in enumerate(prefixes):
                runner = command("runner-" + key + "-" + str(number), [sys.executable, "-I", bundle / (prefix + hook["entrypoint"]),
                    "--host", host, "--event", event_name, "--project", project, "--context", "context.json"],
                    cwd=OUTSIDE / "cwd", stdin=packet)
                assert runner == ({"decision": "ask"} if host == "agy" else {})
                # Manual block is an expected nonzero outcome; retain its actual process receipt.
                name = "manual-" + key + "-" + str(number)
                command_dir = RUN / "commands"
                argv = [sys.executable, "-I", str(bundle / (prefix + hook["manual_entrypoint"])),
                        "--project", str(project), "--context", "context.json"]
                outcome = run_owned_command(argv, OUTSIDE / "cwd", json.dumps(neutral).encode(),
                    command_dir / (name + ".stdout"), command_dir / (name + ".stderr"), timeout=None,
                    on_started=lambda pid: atomic_json(command_dir / (name + ".json"), {"argv": argv, "pid": pid, "status": "running"}))
                manual = load_json(command_dir / (name + ".stdout"))
                assert outcome["exit_status"] == 3 and manual["decision"] == "block"
                atomic_json(command_dir / (name + ".json"), {"argv": argv, **outcome, "expected_exit_status": 3, "oracle": "manual-block-no-generation"})
                preview_path = receipt_dir / ("hook-preview-" + str(number) + ".json")
                config = command("config-preview-" + key + "-" + str(number), [sys.executable, "-I",
                    bundle / (prefix + hook["config_entrypoint"]), "preview", "--host", host, "--package", bundle,
                    "--project", project, "--context", "context.json", "--output", preview_path], cwd=OUTSIDE / "cwd")
                envelope = load_json(preview_path)
                assert config["preview_hash"] == digest_record(envelope["preview"])
                assert not any(envelope["preview"][field] for field in ("registered", "enabled", "trusted"))
            assert before == snapshot(project), "smoke mutated project"
            verify_bundle(bundle)
            item = {"variant": variant, "host": host, "resource_reads": len(observed["observations"]),
                    "writer_disabled_observations": len(disabled), "hook_projections_exercised": len(prefixes),
                    "project_unchanged": True, "status": "pass", "evidence_class": "local-portability-observation"}
            atomic_json(receipt_dir / "summary.json", item)
            results.append(item)
            print("smoke " + key + ": pass", flush=True)
    atomic_json(RUN / "smoke-summary.json", {"schema_version": 1, "status": "pass", "bundles": results,
        "source_lock_hash": context["source_lock_hash"], "native": "unverified", "human": "accepted-exact-r29-writer-samples", "scientific": "pending"})


def preview():
    context = load_json(RUN / "delivery-context.json")
    results = []
    for surface, host in sorted(SURFACE_HOST.items()):
        project = fresh(OUTSIDE / "install-preview" / surface)
        package = OUTSIDE / "extracted/on-standalone" / host
        before = snapshot(project)
        record = command("installer-preview-" + surface, [sys.executable, "-X", "utf8", "-B", ROOT / "installer/nckh-installer.py",
            "install", "--package", package, "--runtime", surface, "--scope", "project", "--project", project,
            "--home", OUTSIDE / "home", "--kits", "core", "engineer", "marketing", "--mode", "copy", "--models", "balanced",
            "--with-agents", "--dry-run"])
        assert record["status"] == "preview" and record["transaction"]["conflicts"] == []
        assert len([row for row in record["transaction"]["entries"] if row["kind"] == "skill"]) == 39
        assert before == snapshot(project), "installer preview wrote project"
        results.append({"surface": surface, "host": host, "entries": len(record["transaction"]["entries"]),
                        "package": str(package), "project_unchanged": True, "status": "preview", "native": "not-run"})
    atomic_json(RUN / "installer-previews.json", {"status": "pass", "source_lock_hash": context["source_lock_hash"], "surfaces": results})


def final():
    context = load_json(RUN / "delivery-context.json")
    baseline = load_json(PROJECT / "plans/reports/checks-261004-1037-starting-baseline.json")
    checked = {relative: digest_file(PROJECT / relative) for relative in baseline["protected_hashes"]}
    assert checked == baseline["protected_hashes"]
    assert context["source_lock_hash"] == digest_record(verify_source_lock(ROOT))
    legacy = []
    for host in HOSTS:
        package = ROOT / "dist" / host
        record = verify_bundle(package)
        legacy.append({"host": host, "schema_version": record["schema_version"], "hooks": "absent" if "hooks" not in record else "present",
                       "source_lock_hash": record["source_lock_hash"], "status": "legacy-verifier-pass"})
    atomic_json(RUN / "final-preservation.json", {"status": "pass", "recorded_at": now(), "protected_hashes_checked": len(checked),
        "source_lock_hash": context["source_lock_hash"], "source_revision": context["source_revision"],
        "installed_revision": "25", "installed_update": "not-performed", "legacy_bundles": legacy,
        "historical_matrix_cells": 224, "owner_review": "accepted-exact-r29-writer-samples", "native": "unverified", "scientific": "pending"})


parser = argparse.ArgumentParser()
parser.add_argument("stage", choices=("build", "smoke", "preview", "final"))
args = parser.parse_args()
try:
    {"build": build, "smoke": smoke, "preview": preview, "final": final}[args.stage]()
except BaseException as error:
    atomic_json(RUN / (args.stage + "-failure.json"), {"status": "failed", "stage": args.stage, "recorded_at": now(),
                "error_type": type(error).__name__, "error": str(error), "native": "unverified"})
    raise
