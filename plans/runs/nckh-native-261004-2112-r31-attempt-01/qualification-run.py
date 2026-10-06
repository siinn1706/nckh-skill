"""Record scoped owner feedback and run installed host probes with owned processes."""

import argparse
import difflib
import hashlib
import json
import os
import re
import queue
import shutil
import sqlite3
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = Path(r"C:/Users/USER\Downloads\test-skill")
KIT = WORK / "nckh-kit"
PLAN = WORK / "plans/261004-0047-nckh-research-data-hooks-writing"
PYTHON = Path(r"C:/Users/USER\AppData\Local\Programs\Python\Python312\python.exe")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def save(path, record):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf8")


def run_command(name, argv, *, cwd=RUN, timeout=45, env=None, stdin=None):
    directory = RUN / "commands"
    directory.mkdir(exist_ok=True)
    receipt_path = directory / f"{name}.json"
    if receipt_path.exists():
        raise RuntimeError(f"Preserve existing command receipt: {receipt_path}")
    started = timestamp()
    begin = time.monotonic()
    process = subprocess.Popen([str(item) for item in argv], cwd=cwd, env=env, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               creationflags=subprocess.CREATE_NO_WINDOW)
    record = {"command": [str(item) for item in argv], "pid": process.pid, "cwd": str(cwd),
              "started_at": started, "status": "running", "owned_by": str(RUN), "port": None}
    save(receipt_path, record)
    try:
        stdout, stderr = process.communicate(stdin, timeout=timeout)
        timed_out = False
    except subprocess.TimeoutExpired:
        # This handle is the exact child created above. Stop it before returning.
        process.terminate()
        try:
            stdout, stderr = process.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate(timeout=10)
        timed_out = True
    (directory / f"{name}.stdout.txt").write_bytes(stdout)
    (directory / f"{name}.stderr.txt").write_bytes(stderr)
    record.update(status="timeout" if timed_out else "completed", exit_code=process.returncode,
                  ended_at=timestamp(), elapsed_seconds=round(time.monotonic() - begin, 3),
                  stdout_sha256=sha(stdout), stderr_sha256=sha(stderr), process_exited=process.poll() is not None)
    save(receipt_path, record)
    return record, stdout, stderr


def installed_commands():
    codex_root = Path(r"C:/Users/USER\AppData\Roaming\npm\node_modules\@openai\codex")
    codex = list(codex_root.rglob("codex.exe"))
    if len(codex) != 1:
        raise RuntimeError(f"Ambiguous installed Codex executables: {codex}")
    cursor_root = Path(r"C:/Users/USER\AppData\Local\cursor-agent\versions\2026.09.15-d2fe57e")
    commands = {"codex": [codex[0]], "claude": [Path(r"C:/Users/USER\.local\bin\claude.exe")],
                "cursor": [cursor_root / "node.exe", cursor_root / "index.js"],
                "agy": [Path(r"C:/Users/USER\AppData\Local\agy\bin\agy.exe")]}
    for name, command in commands.items():
        if not all(item.is_file() for item in command):
            raise RuntimeError(f"Missing installed executable: {name}")
    return commands


def bootstrap():
    if (RUN / "owner-feedback.json").exists():
        raise RuntimeError("Owner feedback was already recorded")
    lock = KIT / "core/registry/source-lock/source-lock.json"
    lock_bytes = lock.read_bytes()
    lock_hash = sha(json.dumps(json.loads(lock_bytes), sort_keys=True, ensure_ascii=False,
                              separators=(",", ":"), allow_nan=False).encode("utf8"))
    if lock_hash != "6fbdf13a4ba296b3e492b89beaf7fc8299c926d73a02a0ffcd9ea16a88d16248":
        raise RuntimeError("Candidate source lock changed; inspect before qualification")
    report_path = WORK / "plans/reports/reviewer-261004-1037-writer-forward-test.md"
    report = report_path.read_text(encoding="utf8")
    samples = []
    for number, skill, locale in [(1, "nckh-humanwrite", "vi"), (2, "nckh-paperwrite", "en")]:
        section = report.split(f"## Case {number} —", 1)[1].split(f"## Case {number + 1} —", 1)[0]
        input_text = section.split("### Input\n", 1)[1].split("### Actual", 1)[0].strip()
        artifact_area = section.split("### Actual", 1)[1]
        artifact_text = re.search(r"```text\n(.*?)\n```", artifact_area, re.S).group(1)
        input_path = RUN / "owner-samples" / f"case-{number}-{locale}-input.txt"
        output_path = RUN / "owner-samples" / f"case-{number}-{locale}-output.txt"
        input_path.parent.mkdir(exist_ok=True)
        input_path.write_text(input_text + "\n", encoding="utf8", newline="\n")
        output_path.write_text(artifact_text + "\n", encoding="utf8", newline="\n")
        samples.append({"case": number, "skill": skill, "locale": locale, "feedback": "accepted",
                        "input_path": str(input_path.relative_to(WORK)), "input_sha256": sha(input_path.read_bytes()),
                        "artifact_path": str(output_path.relative_to(WORK)), "artifact_sha256": sha(output_path.read_bytes()),
                        "artifact_text_sha256": sha(artifact_text.encode("utf8"))})
    human_message = "1. cho phép\n2. **Mẫu VI:** chấp nhận\n3. **Mẫu EN:** chấp nhận"
    save(RUN / "owner-feedback.json", {"schema_version": 1, "evidence_class": "human-owner-feedback",
         "recorded_at": timestamp(), "source_revision": 29, "source_lock_sha256": lock_hash,
         "source_lock_file_sha256": sha(lock_bytes),
         "review_report": str(report_path.relative_to(WORK)), "review_report_sha256": sha(report_path.read_bytes()),
         "human_message": human_message, "human_message_sha256": sha(human_message.encode("utf8")),
         "feedback_scope": "exact-two-displayed-writing-samples", "samples": samples,
         "stable_scientific_qualification": "not-evaluated", "native_qualification": "separate"})
    save(RUN / "native-grant.json", {"schema_version": 1, "recorded_at": timestamp(), "grant_source": "direct-human-chat",
         "human_message": human_message, "human_message_sha256": sha(human_message.encode("utf8")),
         "scope": "r29 native hook qualification in owned disposable projects inside the work context",
         "work_context": str(WORK), "source_lock_sha256": lock_hash,
         "actions": ["register-test-definitions", "enable-test-definitions", "trust-exact-tested-definitions",
                     "observe-host-responses", "record-evidence", "cleanup-owned-test-config"],
         "provider_spending": "not-granted-by-this-message", "installed-r25-update": "not-granted-by-this-message"})
    preimages = RUN / "plan-preimages"
    preimages.mkdir(exist_ok=True)
    for path in [PLAN / "plan.md", PLAN / "phase-03-portable-hooks.md", PLAN / "phase-04-integration-and-personal-acceptance.md"]:
        shutil.copyfile(path, preimages / path.name)
    commands = installed_commands()
    save(RUN / "ownership.json", {"schema_version": 1, "created_at": timestamp(), "owner": "current-root-session",
         "run_directory": str(RUN), "work_context": str(WORK), "timezone": "Asia/Saigon", "language": "vi",
         "candidate_revision": 29, "source_lock_sha256": lock_hash, "installed_commands": commands_as_strings(commands)})
    print(json.dumps({"status": "recorded", "owner_feedback": [row["feedback"] for row in samples],
                      "native_grant": "recorded", "run": str(RUN)}, ensure_ascii=False))


def commands_as_strings(commands):
    return {name: [str(item) for item in command] for name, command in commands.items()}


def inventory():
    commands = installed_commands()
    if not (RUN / "ownership.json").exists():
        feedback = json.loads((RUN / "owner-feedback.json").read_text(encoding="utf8"))
        save(RUN / "ownership.json", {"schema_version": 1, "created_at": timestamp(), "owner": "current-root-session",
             "run_directory": str(RUN), "work_context": str(WORK), "timezone": "Asia/Saigon", "language": "vi",
             "candidate_revision": 29, "source_lock_sha256": feedback["source_lock_sha256"],
             "installed_commands": commands_as_strings(commands)})
    observations = {}
    for host, command in commands.items():
        version_record, stdout, stderr = run_command(f"{host}-version", command + ["--version"])
        help_record, help_stdout, help_stderr = run_command(f"{host}-help", command + ["--help"])
        observations[host] = {"version_output": stdout.decode("utf8", "replace").strip(),
                              "version_exit": version_record["exit_code"], "help_exit": help_record["exit_code"],
                              "executable": str(command[0]), "executable_sha256": sha(command[0].read_bytes())}
    save(RUN / "host-inventory.json", {"recorded_at": timestamp(), "hosts": observations})
    print(json.dumps(observations, ensure_ascii=False))


def protocol():
    codex = installed_commands()["codex"]
    schema_dir = RUN / "codex-protocol"
    record, stdout, stderr = run_command("codex-protocol-schema", codex + ["app-server", "generate-json-schema", "--experimental", "--out", schema_dir])
    print(json.dumps({"exit_code": record["exit_code"], "schemas": str(schema_dir), "stderr": stderr.decode("utf8", "replace")[:1500]}))


def plan_feedback():
    database = WORK / "plans/.agentkit-runtime/plans/plans.db"
    backup = RUN / "plan-preimages/plans-before-owner-feedback.db"
    if backup.exists():
        raise RuntimeError("Preserve existing index backup")
    with sqlite3.connect(database.as_uri() + "?mode=ro", uri=True) as source, sqlite3.connect(backup) as target:
        source.backup(target)
    environment = dict(os.environ, AGENTKIT_HOME=str(WORK / "plans/.agentkit-runtime"))
    command = [Path(r"C:/Users/USER\bin\ak.exe"), "plan", "check", PLAN / "phase-04-integration-and-personal-acceptance.md", "--json"]
    record, stdout, stderr = run_command("plan-check-owner-feedback", command, env=environment)
    print(stdout.decode("utf8", "replace"))
    if record["exit_code"] != 0:
        raise RuntimeError("Plan feedback update failed; keep evidence and inspect")


def prepare_projects():
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(KIT))
    from core.hook_config import EVENTS, TARGETS, payload_from_bundle, preview_config
    from core.paths import digest_record
    inventory_record = json.loads((RUN / "host-inventory.json").read_text(encoding="utf8"))
    projects = {}
    for host in ("codex", "claude", "cursor", "agy"):
        old_preview = json.loads((WORK / f"plans/runs/nckh-writing-hooks-261004-1037-attempt-03/receipts/on-standalone-{host}/hook-preview-0.json").read_text(encoding="utf8"))
        package = Path(old_preview["preview"]["payload"]["root"])
        payload = payload_from_bundle(package)
        project = RUN / "projects" / host
        project.mkdir(parents=True, exist_ok=False)
        save(project / "context.json", {"schema_version": 1, "task_id": "native-hook-qualification",
             "brief": {"mode": "auto"}, "tool_operations": {"Bash": "write", "PowerShell": "write", "Write": "write", "Edit": "write", "Read": "read"},
             "allowed_operations": ["write", "read"]})
        surface = {"codex": "codex-cli", "claude": "claude-code", "cursor": "cursor-cli", "agy": "agy-cli"}[host]
        version = inventory_record["hosts"][host]["version_output"]
        preview = preview_config(project, host, payload, context_reference="context.json", events=list(EVENTS[host]),
                                 host_version=version, surface=surface, python=PYTHON)
        save(project / "registration-preview.json", {"preview": preview, "preview_hash": digest_record(preview)})
        runtime = project / preview["runtime_relative"]
        for relative in payload["members"]:
            target = runtime / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(package / relative, target)
        save(project / "registration-plan.json", {"host": host, "version": version, "surface": surface,
             "events": list(EVENTS[host]), "target": TARGETS[host], "package": str(package), "payload": payload,
             "runner": str(runtime / payload["runner"]), "preview_hash": digest_record(preview),
             "grant_reference": str(RUN / "native-grant.json"), "purpose": "test-only-bootstrap-for-native-qualification",
             "production_apply": "not-invoked", "trust": "host-controlled; never bypass"})
        projects[host] = str(project)
    save(RUN / "projects.json", projects)
    print(json.dumps({"prepared": list(projects), "registration": "not-yet-written", "production_apply": "not-invoked"}))


def register_observers(host, *, mode="normal", selected_events=None):
    project = RUN / "projects" / host
    registration = json.loads((project / "registration-plan.json").read_text(encoding="utf8"))
    config = {"version": 1, "hooks": {}} if host == "cursor" else {"nckh": {"enabled": True}} if host == "agy" else {"hooks": {}}
    area = config["nckh"] if host == "agy" else config["hooks"]
    for event in selected_events or registration["events"]:
        command = subprocess.list2cmdline([str(PYTHON), "-I", str(RUN / "hook-observer.py"), "--host", host,
                   "--event", event, "--project", str(project), "--runner", registration["runner"], "--mode", mode])
        handler = {"type": "command", "command": command, "timeout": 1 if mode == "timeout" else 5}
        if host == "cursor" and event == "preToolUse":
            handler["failClosed"] = True
        if host == "cursor" and event == "stop":
            handler["loop_limit"] = 1
        area[event] = [handler] if host == "cursor" or (host == "agy" and event not in {"PreToolUse", "PostToolUse"}) else [{"matcher": ".*", "hooks": [handler]}]
    path = project / registration["target"]
    path.parent.mkdir(parents=True, exist_ok=True)
    save(path, config)
    save(project / f"registered-{mode}.json", {"config": config, "config_sha256": sha(path.read_bytes()),
         "observer_sha256": sha((RUN / "hook-observer.py").read_bytes()), "source_closure_hash": registration["payload"]["closure_hash"],
         "definition_scope": "test-only instrumented runner", "registered_at": timestamp()})
    return project


def claude_start():
    project = register_observers("claude", selected_events=["SessionStart"])
    command = installed_commands()["claude"] + ["--init-only", "--setting-sources", "project,local",
               "--debug-file", str(project / "native-debug.log")]
    record, stdout, stderr = run_command("claude-session-start-normal", command, cwd=project)
    print(json.dumps({"exit_code": record["exit_code"], "stdout": stdout.decode("utf8", "replace")[:800],
                      "stderr": stderr.decode("utf8", "replace")[:800], "observer_records": len(list((project / "observations").glob("*.json")))}))


def claude_start_explicit():
    project = RUN / "projects/claude"
    command = installed_commands()["claude"] + ["--init-only", "--setting-sources", "project,local",
               "--settings", str(project / ".claude/settings.local.json"),
               "--debug-file", str(project / "native-explicit-debug.log")]
    record, stdout, stderr = run_command("claude-session-start-explicit", command, cwd=project)
    print(json.dumps({"exit_code": record["exit_code"], "observer_records": len(list((project / "observations").glob("*.json")))}))


class CodexRPC:
    def __init__(self, name, project, *, isolated=False):
        self.name = name
        self.project = project
        self.directory = RUN / "commands"
        self.path = self.directory / f"{name}.json"
        if self.path.exists():
            raise RuntimeError("Preserve existing RPC receipt")
        # This is the exact disposable project grant. Hook-definition trust is still enforced.
        project_trust = f'projects.{json.dumps(str(project).casefold())}.trust_level="trusted"'
        configuration = ["-c", project_trust]
        if isolated:
            state = project / "native-state"
            state.mkdir(exist_ok=True)
            configuration += ["-c", f"sqlite_home={json.dumps(str(state / 'sqlite'))}",
                              "-c", f"log_dir={json.dumps(str(state / 'logs'))}", "-c", 'history.persistence="none"']
        self.command = installed_commands()["codex"] + configuration + ["app-server", "--stdio"]
        self.process = subprocess.Popen([str(item) for item in self.command], cwd=project, stdin=subprocess.PIPE,
             stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
        self.record = {"status": "running", "pid": self.process.pid, "command": [str(item) for item in self.command],
                       "cwd": str(project), "started_at": timestamp(), "owned_by": str(RUN), "port": None}
        save(self.path, self.record)
        self.inbox = queue.Queue()
        self.messages = []
        self.stderr = []
        self.next_id = 0
        self.reader = threading.Thread(target=self.read_stdout, daemon=True)
        self.error_reader = threading.Thread(target=self.read_stderr, daemon=True)
        self.reader.start()
        self.error_reader.start()

    def read_stdout(self):
        for line in self.process.stdout:
            self.messages.append(line)
            try:
                self.inbox.put(json.loads(line))
            except ValueError:
                self.inbox.put({"unparsed_stdout_sha256": sha(line)})

    def read_stderr(self):
        for line in self.process.stderr:
            self.stderr.append(line)

    def request(self, method, params):
        self.next_id += 1
        identifier = self.next_id
        request = {"id": identifier, "method": method, "params": params}
        with (self.directory / f"{self.name}.requests.jsonl").open("ab") as stream:
            stream.write(json.dumps(request).encode("utf8") + b"\n")
        self.process.stdin.write(json.dumps(request).encode("utf8") + b"\n")
        self.process.stdin.flush()
        deadline = time.monotonic() + 25
        while time.monotonic() < deadline:
            try:
                message = self.inbox.get(timeout=0.2)
            except queue.Empty:
                if self.process.poll() is not None:
                    raise RuntimeError(f"Native app server exited: {self.process.returncode}")
                continue
            if message.get("id") == identifier and "method" not in message:
                return message
            if "id" in message and "method" in message:
                # Never invent approval for another tool, provider or definition.
                response = {"id": message["id"], "error": {"code": -32601, "message": "No delegated approval for this server request"}}
                self.process.stdin.write(json.dumps(response).encode("utf8") + b"\n")
                self.process.stdin.flush()
        raise RuntimeError(f"Native RPC request timed out: {method}")

    def close(self):
        if self.process.stdin and not self.process.stdin.closed:
            self.process.stdin.close()
        try:
            self.process.wait(timeout=8)
            stop = "stdin-closed"
        except subprocess.TimeoutExpired:
            self.process.terminate()
            self.process.wait(timeout=8)
            stop = "owned-process-terminated"
        self.reader.join(timeout=2)
        self.error_reader.join(timeout=2)
        stdout = b"".join(self.messages)
        stderr = b"".join(self.stderr)
        (self.directory / f"{self.name}.stdout.jsonl").write_bytes(stdout)
        (self.directory / f"{self.name}.stderr.txt").write_bytes(stderr)
        self.record.update(status="completed", exit_code=self.process.returncode, ended_at=timestamp(),
             stdout_sha256=sha(stdout), stderr_sha256=sha(stderr), cleanup=stop, process_exited=self.process.poll() is not None)
        save(self.path, self.record)

    def notifications(self, seconds=3):
        deadline = time.monotonic() + seconds
        messages = []
        while time.monotonic() < deadline:
            try:
                messages.append(self.inbox.get(timeout=0.2))
            except queue.Empty:
                if self.process.poll() is not None:
                    break
        return messages


def codex_discovery(isolated=False, elevated=False):
    project = register_observers("codex")
    name = "codex-native-discovery-elevated" if elevated else "codex-native-discovery-isolated" if isolated else "codex-native-discovery"
    if elevated:
        for number, database in enumerate((project / "native-state/sqlite").glob("*.sqlite")):
            backup = RUN / "plan-preimages" / f"codex-native-before-elevated-{number}.sqlite"
            with sqlite3.connect(database.as_uri() + "?mode=ro", uri=True) as source, sqlite3.connect(backup) as target:
                source.backup(target)
    rpc = CodexRPC(name, project, isolated=isolated)
    try:
        initialization = rpc.request("initialize", {"clientInfo": {"name": "nckh-native-qualification", "version": "r29"},
             "capabilities": {"experimentalApi": True}})
        discovery = rpc.request("hooks/list", {"cwds": [str(project)]})
        save(project / f"{name}.json", {"initialization": initialization, "discovery": discovery})
        result = discovery.get("result", {})
        print(json.dumps({"initialize_error": initialization.get("error"), "hooks_response": result,
                          "request_error": discovery.get("error")}, ensure_ascii=False))
    finally:
        rpc.close()


def codex_discovery_isolated():
    codex_discovery(isolated=True)


def codex_discovery_elevated():
    codex_discovery(isolated=True, elevated=True)


def codex_discovery_normalized():
    project = RUN / "projects/codex"
    rpc = CodexRPC("codex-native-discovery-normalized", project, isolated=True)
    try:
        initialization = rpc.request("initialize", {"clientInfo": {"name": "nckh-native-qualification", "version": "r29"},
             "capabilities": {"experimentalApi": True}})
        discovery = rpc.request("hooks/list", {"cwds": [str(project)]})
        save(project / "native-discovery-normalized.json", {"initialization": initialization, "discovery": discovery})
        entries = discovery.get("result", {}).get("data", [])
        selected = [row for entry in entries for row in entry.get("hooks", []) if row.get("sourcePath") == str(project / ".codex/hooks.json")]
        print(json.dumps({"project_hooks": [{key: row.get(key) for key in ("eventName", "enabled", "trustStatus", "currentHash")} for row in selected],
                          "errors": [entry.get("errors") for entry in entries], "request_error": discovery.get("error")}))
    finally:
        rpc.close()


def claude_start_isolated(elevated=False):
    project = RUN / "projects/claude"
    state = project / "native-state"
    state.mkdir(exist_ok=True)
    environment = dict(os.environ, CLAUDE_CONFIG_DIR=str(state), CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC="1")
    command = installed_commands()["claude"] + ["--init-only", "--setting-sources", "project,local",
               "--settings", str(project / ".claude/settings.local.json"),
               "--debug-file", str(project / ("native-elevated-debug.log" if elevated else "native-isolated-debug.log"))]
    name = "claude-session-start-elevated" if elevated else "claude-session-start-isolated"
    record, stdout, stderr = run_command(name, command, cwd=project, env=environment)
    print(json.dumps({"exit_code": record["exit_code"], "observer_records": len(list((project / "observations").glob("*.json")))}))


def claude_start_elevated():
    claude_start_isolated(elevated=True)


def claude_start_exec():
    project = RUN / "projects/claude"
    registration = json.loads((project / "registration-plan.json").read_text(encoding="utf8"))
    handler = {"type": "command", "command": str(PYTHON), "args": ["-I", str(RUN / "hook-observer.py"),
               "--host", "claude", "--event", "SessionStart", "--project", str(project), "--runner", registration["runner"],
               "--mode", "normal"], "timeout": 5}
    config = {"hooks": {"SessionStart": [{"matcher": ".*", "hooks": [handler]}]}}
    save(project / ".claude/settings.local.json", config)
    save(project / "registered-exec-form.json", {"config": config, "config_sha256": sha((project / ".claude/settings.local.json").read_bytes())})
    environment = dict(os.environ, CLAUDE_CONFIG_DIR=str(project / "native-state"), CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC="1")
    command = installed_commands()["claude"] + ["--init-only", "--setting-sources", "project,local", "--settings", str(project / ".claude/settings.local.json"),
               "--debug-file", str(project / "native-exec-form-debug.log")]
    record, stdout, stderr = run_command("claude-session-start-exec-form", command, cwd=project, env=environment)
    print(json.dumps({"exit_code": record["exit_code"], "observer_records": len(list((project / "observations").glob("*.json")))}))


def focused_checks():
    command = [PYTHON, "-X", "utf8", "-B", "-m", "unittest", "tests.hooks.test_config", "tests.hooks.test_policy",
               "tests.hooks.test_runner", "tests.runtime.test_hook_adapters", "-v"]
    record, stdout, stderr = run_command("focused-hooks-after-native-fix", command, cwd=KIT, timeout=None)
    print(json.dumps({"exit_code": record["exit_code"], "summary": stderr.decode("utf8", "replace")[-700:]}))
    if record["exit_code"] != 0:
        raise RuntimeError("Focused hook checks failed")


def review_and_freeze():
    checks = json.loads((RUN / "commands/focused-hooks-after-native-fix.json").read_text(encoding="utf8"))
    if checks["exit_code"] != 0:
        raise RuntimeError("Review must follow successful focused checks")
    mappings = {"core/hook_config.py": "hook_config.py", "tests/hooks/test_config.py": "test_config.py", "docs/installation.md": "installation.md"}
    changes = []
    diffs = []
    for relative, original_name in mappings.items():
        before = (RUN / "source-preimages-r29" / original_name).read_bytes()
        after = (KIT / relative).read_bytes()
        changes.append({"path": relative, "before_sha256": sha(before), "after_sha256": sha(after)})
        diffs.extend(difflib.unified_diff(before.decode("utf8").splitlines(keepends=True), after.decode("utf8").splitlines(keepends=True),
                     fromfile=relative + " before", tofile=relative + " after"))
    (RUN / "source-review.diff").write_text("".join(diffs), encoding="utf8")
    save(RUN / "source-review.json", {"schema_version": 1, "recorded_at": timestamp(), "reviewer": "root-inline-review",
         "independent_review": False, "scope": list(mappings), "changes": changes,
         "cause_evidence": "projects/claude/native-elevated-debug.log", "repair_evidence": "projects/claude/native-exec-form-debug.log",
         "reviewed_invariants": ["controller-owned argument array", "no event payload command execution", "unchanged other-host encoding",
             "arguments included in definition hashes and recursive reference checks", "activation and conflict gates preserved"],
         "findings_remaining": [], "focused_checks": "commands/focused-hooks-after-native-fix.json"})
    previous = json.loads((KIT / "core/registry/source-lock/source-lock.json").read_text(encoding="utf8"))
    if previous["revision"] != "29":
        raise RuntimeError("Freeze owner must review the actual starting revision")
    record, stdout, stderr = run_command("freeze-r30-native-path-repair", [PYTHON, "-X", "utf8", "-B", KIT / "scripts/freeze-source-lock.py", "--write"], cwd=KIT)
    if record["exit_code"] != 0:
        raise RuntimeError("Freeze failed")
    current = json.loads((KIT / "core/registry/source-lock/source-lock.json").read_text(encoding="utf8"))
    changed = [path for path in current["files"] if previous["files"].get(path) != current["files"][path]]
    if current["revision"] != "30" or set(changed) != set(mappings) or set(previous["files"]) != set(current["files"]):
        raise RuntimeError("Freeze delta is not the reviewed repair")
    canonical = sha(json.dumps(current, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode("utf8"))
    save(RUN / "r30-source-checkpoint.json", {"recorded_at": timestamp(), "source_revision": 30, "source_lock_hash": canonical,
         "files": len(current["files"]), "changed": changed, "previous_lock_hash": current["previous_lock_hash"],
         "owner_feedback": "accepted-r29-samples-retained-with-original-binding", "writer_instruction_pins_unchanged": True})
    print(json.dumps({"revision": 30, "source_lock_hash": canonical, "changed": changed, "files": len(current["files"])}))


def deterministic_checks():
    record, stdout, stderr = run_command("deterministic-r30", [PYTHON, "-X", "utf8", "-B", KIT / "evals/run-evals.py",
         "--run-deterministic", "--output", RUN / "deterministic-r30.json"], cwd=KIT, timeout=None)
    print(json.dumps({"exit_code": record["exit_code"], "stderr_tail": stderr.decode("utf8", "replace")[-500:]}))
    if record["exit_code"] != 0:
        raise RuntimeError("Deterministic checks failed")


def codex_native_local():
    project = RUN / "projects/codex"
    rpc = CodexRPC("codex-native-local-shell", project, isolated=True)
    try:
        initialization = rpc.request("initialize", {"clientInfo": {"name": "nckh-native-qualification", "version": "r29"},
             "capabilities": {"experimentalApi": True}})
        discovery = rpc.request("hooks/list", {"cwds": [str(project)]})
        selected = [row for entry in discovery.get("result", {}).get("data", []) for row in entry.get("hooks", [])
                    if row.get("source") == "project" and row.get("sourcePath", "").casefold() == str(project / ".codex/hooks.json").casefold()]
        save(project / "native-trust-observation.json", {"recorded_at": timestamp(), "project_hooks": selected})
        required = {"preToolUse", "sessionStart"}
        if not required <= {row["eventName"] for row in selected if row["trustStatus"] == "trusted"}:
            raise RuntimeError("Selected native definitions are not trusted; do not bypass")
        thread = rpc.request("thread/start", {"cwd": str(project), "ephemeral": True, "sandbox": "read-only", "approvalPolicy": "on-request"})
        save(project / "native-local-thread.json", thread)
        if "error" in thread:
            raise RuntimeError("Native local thread failed")
        thread_id = thread["result"]["thread"]["id"]
        # Local user-shell route, no model turn and no intended file mutation.
        local = rpc.request("thread/shellCommand", {"threadId": thread_id, "command": "Write-Output 'nckh-native-local-probe'", "timeoutMs": 5000})
        notifications = rpc.notifications(seconds=5)
        save(project / "native-local-shell-response.json", {"thread_id": thread_id, "response": local, "notifications": notifications,
             "model_turn_started": False, "route": "local-user-shell; do not equate with model-generated-tool coverage"})
        print(json.dumps({"project_hooks": [{key: row.get(key) for key in ("eventName", "trustStatus", "currentHash")} for row in selected],
                          "shell_error": local.get("error"), "notifications": [row.get("method") for row in notifications],
                          "observer_records": len(list((project / "observations").glob("*.json")))}))
    finally:
        rpc.close()


def cursor_pre_call():
    project = register_observers("cursor", mode="deny", selected_events=["sessionStart", "beforeSubmitPrompt", "preToolUse", "postToolUse", "stop"])
    command = installed_commands()["cursor"] + ["--print", "--trust", "--workspace", str(project),
               "--endpoint", "http://127.0.0.1:9", "--output-format", "stream-json", "Native hook test; do not run tools."]
    environment = dict(os.environ, NODE_COMPILE_CACHE=str(project / "compile-cache"))
    record, stdout, stderr = run_command("cursor-native-pre-call", command, cwd=project, timeout=40, env=environment)
    print(json.dumps({"exit_code": record["exit_code"], "status": record["status"],
                      "stdout_tail": stdout.decode("utf8", "replace")[-1200:], "stderr_tail": stderr.decode("utf8", "replace")[-1200:],
                      "observer_records": len(list((project / "observations").glob("*.json")))}))


def agy_local_probe():
    project = register_observers("agy", mode="deny", selected_events=["PreInvocation"])
    command = installed_commands()["agy"] + ["--print", "Native hook test; do not run tools.", "--project", str(project),
               "--print-timeout", "15s", "--mode", "plan", "--sandbox", "--log-file", str(project / "native-probe.log")]
    environment = dict(os.environ, HTTP_PROXY="http://127.0.0.1:9", HTTPS_PROXY="http://127.0.0.1:9")
    record, stdout, stderr = run_command("agy-native-local-probe", command, cwd=project, timeout=25, env=environment)
    print(json.dumps({"exit_code": record["exit_code"], "status": record["status"],
                      "stdout_tail": stdout.decode("utf8", "replace")[-900:], "stderr_tail": stderr.decode("utf8", "replace")[-900:],
                      "observer_records": len(list((project / "observations").glob("*.json")))}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["bootstrap", "inventory", "protocol", "plan_feedback", "prepare_projects", "claude_start", "claude_start_explicit", "codex_discovery", "codex_discovery_isolated", "claude_start_isolated", "codex_discovery_elevated", "claude_start_elevated", "codex_discovery_normalized", "claude_start_exec", "focused_checks", "review_and_freeze", "deterministic_checks", "codex_native_local", "cursor_pre_call", "agy_local_probe"])
    globals()[parser.parse_args().action]()
