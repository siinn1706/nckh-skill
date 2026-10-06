"""Remove only owned matching project configs and staged payload members."""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
sys.path.insert(0, str(WORK / "nckh-kit"))
sys.dont_write_bytecode = True

from core.paths import atomic_json, contained, digest_file, no_links

receipt = RUN / "native-cleanup.json"
if receipt.exists():
    raise RuntimeError("Preserve previous cleanup receipt")
projects = []
for host in ("claude", "codex", "cursor", "agy"):
    project = RUN / "projects" / host
    plan = json.loads((project / "registration-plan.json").read_text(encoding="utf8"))
    definitions = [json.loads(path.read_text(encoding="utf8")) for path in project.glob("registered-*.json")]
    target = contained(project, plan["target"])
    expected = {record["config_sha256"] for record in definitions}
    projects.append({"project": project, "configs": {plan["target"]: expected}, "payload": plan["payload"]})
for base in (RUN / "projects-r30" / "claude", RUN / "projects-r30-attempt-02" / "claude"):
    for project in base.iterdir():
        if not project.is_dir():
            continue
        record = json.loads((project / "registered-definition.json").read_text(encoding="utf8"))
        preview = json.loads((project / "registration-preview.json").read_text(encoding="utf8"))
        configs = {".claude/settings.local.json": {record["config_sha256"]}}
        plugin_config = record["config"]
        for relative in ("duplicate-test-plugin/hooks/hooks.json", "duplicate-test-plugin/.claude-plugin/plugin.json"):
            if contained(project, relative).exists():
                raise RuntimeError("Plugin cleanup did not finish; preserve its config for review")
        projects.append({"project": project, "configs": configs, "payload": preview["payload"]})

record = {"schema_version": 1, "started_at": datetime.now(timezone.utc).isoformat(), "owner": "/root",
          "status": "preflight", "projects": [], "global_configuration": "no-direct-write",
          "native_definition_trust": "two-test-hashes-remain-disabled-in-host-store",
          "project_trust": "test-project-trust-may-remain-in-host-store"}
for item in projects:
    project = no_links(item["project"])
    if not project.resolve().is_relative_to(RUN.resolve()):
        raise RuntimeError("Cleanup escaped its owned run")
    payload = item["payload"]
    runtime = contained(project, f".nckh-state/hooks/{payload['host']}/{payload['closure_hash']}")
    row = {"project": str(project), "runtime": str(runtime), "config_expected_hashes":
           {name: sorted(values) for name, values in item["configs"].items()},
           "removed_configs": [], "configs_already_absent": [], "removed_payload_members": [],
           "conflicts": [], "payload_expected_members": payload["members"]}
    record["projects"].append(row)
atomic_json(receipt, record)
for item, row in zip(projects, record["projects"]):
    project = item["project"]
    for relative, expected in item["configs"].items():
        target = contained(project, relative)
        if not target.exists():
            row["configs_already_absent"].append(relative)
        elif target.is_file() and digest_file(target) in expected:
            target.unlink()
            row["removed_configs"].append(relative)
        else:
            row["conflicts"].append(relative)
    # Preserve payload when any owned config no longer matches its receipt.
    if not row["conflicts"]:
        runtime = no_links(row["runtime"])
        if runtime.exists():
            for relative, expected in item["payload"]["members"].items():
                member = contained(runtime, relative)
                if member.is_file() and digest_file(member) == expected:
                    member.unlink()
                    row["removed_payload_members"].append(relative)
                elif member.exists():
                    row["conflicts"].append("payload/" + relative)
            for directory in sorted((path for path in runtime.rglob("*") if path.is_dir()),
                                    key=lambda path: len(path.parts), reverse=True):
                no_links(directory)
                if not any(directory.iterdir()):
                    directory.rmdir()
            if not any(runtime.iterdir()):
                runtime.rmdir()
    atomic_json(receipt, record)
record.update(status="conflict" if any(row["conflicts"] for row in record["projects"]) else "pass",
              ended_at=datetime.now(timezone.utc).isoformat(),
              payload_policy="archives-extracted-packages-contexts-and-receipts-preserved; staged-native-payloads-removed")
atomic_json(receipt, record)
print(json.dumps({"status": record["status"], "projects": len(record["projects"]),
                  "configs_removed": sum(len(row["removed_configs"]) for row in record["projects"]),
                  "payload_members_removed": sum(len(row["removed_payload_members"]) for row in record["projects"]),
                  "conflicts": [row["conflicts"] for row in record["projects"] if row["conflicts"]]}))
