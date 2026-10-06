"""Actual isolated reads and installer previews from owned external extractions."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import uuid
import zipfile

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
KIT = WORK / "nckh-kit"
sys.path.insert(0, str(KIT))
from core.build import verify_bundle
from core.install import SURFACE_HOST
from core.paths import digest_file, no_links

def save(name, value):
    with (RUN / name).open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(value, indent=2) + "\n")

def snapshot(root):
    return {path.relative_to(root).as_posix(): digest_file(no_links(path)) for path in root.rglob("*") if path.is_file()}

spec = importlib.util.spec_from_file_location("resource_smoke", KIT / "scripts/resource-smoke.py")
smoke = importlib.util.module_from_spec(spec)
spec.loader.exec_module(smoke)
outside = no_links(Path(tempfile.gettempdir()) / ("nckh-upgrade-" + uuid.uuid4().hex)).resolve()
assert not outside.is_relative_to(WORK.resolve())
outside.mkdir(mode=0o777 if os.name == "nt" else 0o700)
cwd = outside / "cwd"
cwd.mkdir()
save("p7-temp-ownership.json", {"root": str(outside), "cwd": str(cwd), "owner": str(RUN), "outside_workspace": True,
    "purpose": "Archive/extraction, isolated readers/checker and disposable installer previews", "cleanup": "pending"})
environment = dict(os.environ)
environment.pop("PYTHONPATH", None)
environment.pop("NCKH_RESOURCE_TEST_ROOT", None)
records = []
try:
    for mode in ("on-standalone", "on-plugin", "off-standalone-internal", "off-plugin-internal"):
        for host in ("claude", "codex", "cursor", "agy"):
            source = RUN / "bundles" / mode / host
            before = snapshot(source)
            manifest = verify_bundle(source)
            archive = outside / (mode + "-" + host + ".zip")
            with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED) as stream:
                for name in sorted(before): stream.write(source / name, name)
            target = outside / "extracted" / mode / host
            with zipfile.ZipFile(archive) as stream:
                assert all(not Path(name).is_absolute() and ".." not in Path(name).parts for name in stream.namelist())
                stream.extractall(target)
            assert snapshot(target) == before and snapshot(source) == before
            verified = verify_bundle(target)
            assert verified == manifest
            row = {"mode": mode, "host": host, "source": str(source), "extracted": str(target), "manifest_sha256": digest_file(target / "manifest.json"),
                "archive_sha256": digest_file(archive), "files": len(before), "resource_bindings": len(manifest.get("resources", [])),
                "closure_hash": manifest["closure_hash"], "source_lock_hash": manifest["source_lock_hash"], "verdict": "pass"}
            if mode.startswith("on-"):
                observation = smoke.smoke(target, cwd)
                save("p7-smoke-" + mode + "-" + host + ".json", observation)
                row["actual_resource_reads"] = len(observation["observations"])
                if mode == "on-plugin":
                    plugin_observations = []
                    for resource in manifest["resources"]:
                        context = smoke.CONTEXTS.get(resource["resource_id"])
                        if context is None:
                            registry_path = next(path for path in resource["requires"] if path.endswith("core/registry/catalog/resources.json"))
                            resource_row = next(item for item in json.loads((target / registry_path).read_text(encoding="utf-8"))["resources"] if item["resource_id"] == resource["resource_id"])
                            context = ["--domain", resource_row["domain"], "--genre", resource_row["genre"], "--locale", resource_row["locale"]]
                        else: context = [*context, "--locale", "en"]
                        command = [sys.executable, "-I", str(target / "plugin" / resource["reader"]), "--resource-id", resource["resource_id"],
                            "--consumer", resource["consumer"], *context, "--json"]
                        process = subprocess.run(command, cwd=cwd, env=environment, capture_output=True)
                        result = json.loads(process.stdout)
                        assert process.returncode == 0 and result["resource_read"] and result["resource_sha256"] == resource["source_sha256"]
                        plugin_observations.append({"resource_id": resource["resource_id"], "consumer": resource["consumer"], "reader_sha256": digest_file(target / "plugin" / resource["reader"]),
                            "resource_sha256": result["resource_sha256"], "exit_status": process.returncode})
                    save("p7-plugin-reads-" + host + ".json", {"python_isolated": True, "cwd": str(cwd), "observations": plugin_observations})
                    row["actual_plugin_resource_reads"] = len(plugin_observations)
                checker = next(item["path"] for item in manifest["files"] if item["source_path"] == "scripts/check-research-artifacts.py" and item["path"].startswith("skills/nckh-method/"))
                output = "p7-extracted-check-" + mode + "-" + host + ".json"
                command = [sys.executable, "-I", str(target / checker), "--project", str(RUN), "--task", "vnm-population-chronological-forecast",
                    "--manifest", "experiment-readout.json", "--output", output]
                process = subprocess.run(command, cwd=cwd, env=environment, capture_output=True)
                save("p7-checker-observation-" + mode + "-" + host + ".json", {"argv": command, "exit_status": process.returncode,
                    "stdout": process.stdout.decode("utf-8"), "stderr": process.stderr.decode("utf-8"), "cwd": str(cwd)})
                assert process.returncode == 0, process.stderr.decode("utf-8")
                row["isolated_checker"] = "pass"
            else:
                reader = next(item["path"] for item in manifest["files"] if item["source_path"] == "scripts/search-resource.py" and item["path"].startswith("skills/nckh-statistics/"))
                command = [sys.executable, "-I", str(target / reader), "--resource-id", "R-statistical-recipes", "--consumer", "nckh-statistics",
                    "--domain", "scientific-statistics", "--genre", "statistical-recipe", "--resource-access", "off", "--json"]
                process = subprocess.run(command, cwd=cwd, env=environment, capture_output=True)
                result = json.loads(process.stdout)
                assert process.returncode == 0 and not result["resource_read"] and result["status"] == "resource-disabled"
                save("p7-off-read-" + mode + "-" + host + ".json", {"result": result, "cwd": str(cwd), "exit_status": process.returncode})
                row["off_missing_resources_no_read"] = True
            assert snapshot(target) == before and snapshot(source) == before
            records.append(row)
            save("p7-package-" + mode + "-" + host + ".json", row)
            print(json.dumps({"mode": mode, "host": host, "verdict": "pass"}), flush=True)
    previews = []
    for surface, host in SURFACE_HOST.items():
        project = outside / "disposable" / surface
        project.mkdir(parents=True)
        (project / "user.txt").write_text("Existing user bytes must survive read-only preview.\n", encoding="utf-8")
        package = outside / "extracted/on-standalone" / host
        source_before, target_before = snapshot(package), snapshot(project)
        command = [sys.executable, "-B", str(KIT / "installer/nckh-installer.py"), "install", "--package", str(package), "--runtime", surface,
            "--scope", "project", "--project", str(project), "--home", str(outside / "disposable-home"),
            "--kits", "core", "engineer", "marketing", "--mode", "copy", "--models", "balanced", "--dry-run"]
        process = subprocess.run(command, cwd=cwd, env=environment, capture_output=True)
        result = json.loads(process.stdout)
        save("p7-installer-preview-" + surface + ".json", {"argv": command, "exit_status": process.returncode, "preview": result,
            "source_pre": source_before, "source_post": snapshot(package), "target_pre": target_before, "target_post": snapshot(project)})
        assert process.returncode == 0 and result["status"] == "preview", process.stderr.decode("utf-8")
        assert source_before == snapshot(package) and target_before == snapshot(project)
        previews.append({"surface": surface, "host": host, "exit_status": 0, "preserved_source_and_target": True})
        print(json.dumps({"installer_preview": surface, "verdict": "pass"}), flush=True)
    legacy = []
    roots = [KIT / "dist/codex", WORK / "plans/runs/nckh-native-261004-2112-r33-attempt-01/build/on-standalone/codex",
        WORK / "plans/runs/nckh-writing-hooks-261004-1037-attempt-03/build/on-standalone/codex"]
    for root in roots:
        before = snapshot(root)
        manifest = verify_bundle(root)
        assert snapshot(root) == before
        legacy.append({"root": str(root), "format": manifest["schema_version"], "source_lock_hash": manifest["source_lock_hash"], "manifest_sha256": digest_file(root / "manifest.json"), "verdict": "pass", "unchanged": True})
    assert {row["format"] for row in legacy} == {1, 2}
    save("p7-extracted-qualification.json", {"packages": records, "installer_previews": previews, "legacy": legacy,
        "temp_root": str(outside), "native_qualification": "unverified", "scientific_acceptance": "pending", "stable_public_release": "not-authorized"})
    owned_before = snapshot(outside)
    save("p7-temp-before-cleanup.json", {"root": str(outside), "files": owned_before})
    assert outside.is_relative_to(Path(tempfile.gettempdir()).resolve()) and outside.name.startswith("nckh-upgrade-")
    assert snapshot(outside) == owned_before
    no_links(outside)
    shutil.rmtree(outside)
    save("p7-temp-cleanup.json", {"root": str(outside), "removed": not outside.exists(), "verified_owned_unchanged_files": len(owned_before), "owned_live": 0})
except BaseException as error:
    save("p7-extraction-failure.json", {"type": type(error).__name__, "error": str(error), "completed_packages": records,
        "temp_root": str(outside), "cleanup": "retained for inspection; no broad deletion"})
    raise
