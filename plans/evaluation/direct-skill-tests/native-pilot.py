"""One authorized native development probe; private project-local telemetry."""

import hashlib
import json
import os
from pathlib import Path
import sys
import tomllib

PROJECT = Path(__file__).resolve().parents[3]
AREA = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT / "nckh-kit"))
from core.processes import run_owned_command


def toml_value(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, dict):
        return "{" + ", ".join(json.dumps(k) + " = " + toml_value(v) for k, v in value.items()) + "}"
    if isinstance(value, (int, float)):
        return str(value)
    raise ValueError("Unsupported selected native configuration value")


def main():
    native = Path(r"C:/Users/USER\AppData\Local\OpenAI\Codex\bin\de8a38d2100ae498\codex.exe")
    private = AREA / "private"
    native_home = private / "native-home"
    workspace = AREA / "workspaces" / "pilot-write"
    for path in (native_home, workspace):
        path.mkdir(parents=True, exist_ok=True)
    configuration = tomllib.loads((Path(r"C:/Users/USER\.codex") / "config.toml").read_text("utf-8"))
    provider = configuration["model_provider"]
    lines = [f"{key} = {toml_value(configuration[key])}" for key in
             ("model", "model_provider", "model_reasoning_effort") if key in configuration]
    lines += ["[model_providers." + json.dumps(provider) + "]"]
    lines += [json.dumps(k) + " = " + toml_value(v) for k, v in configuration["model_providers"][provider].items()]
    (native_home / "config.toml").write_text("\n".join(lines) + "\n", "utf-8")
    os.environ["CODEX_HOME"] = str(native_home)
    for variable in ("TEMP", "TMP"):
        os.environ[variable] = str(native_home / "tmp")
    (native_home / "tmp").mkdir(exist_ok=True)
    prompt = '''Use the installed project skill nckh-write for requests it owns. Read its SKILL.md and required references from C:/Users/USER/Downloads/test-skill/.agents/skills/nckh-write before working. When a request belongs to another skill, name that actual owner and explain the handoff briefly. Use Vietnamese for notes. Work directly; do not delegate. Treat all supplied passages as owned synthetic development inputs. Do not browse or install anything. Read only these installed skill/reference files and files in the current workspace; write only in the current workspace. Do not read test-controller/private directories or host credentials. No publication or external writes are requested.

Return substantive answers for each numbered request, with a usable draft where requested and short factual-delta notes. Do not evaluate or score yourself.

1. Polish this paragraph minimally; preserve the quotation byte-for-byte, all numbers, denominator, time, negation, citation and uncertainty. Glossary: truy hồi = retrieval; độ chính xác = accuracy. Source paragraph:
Trong khảo sát tháng 8/2026, 18/60 sinh viên cho biết công cụ truy hồi giúp họ tìm tài liệu nhanh hơn. Kết quả này chưa cho thấy công cụ làm tăng độ chính xác; thời gian được đo bằng giây và chỉ có 12 sinh viên hoàn thành cả hai lượt thử. Một người viết: “Tôi thấy nhanh hơn, nhưng chưa chắc đúng hơn.” [S1]. Do mẫu thuận tiện và dữ liệu tự báo cáo, chưa thể suy ra quan hệ nhân quả.

2. Translate the preceding paragraph into English for a methods/results note. Keep [S1] as a supplied marker, preserve the quotation in Vietnamese exactly, and retain all limitations.

3. A collaborator asks you to replace the result with “The tool proved that it improved accuracy for all students.” Decide whether this is supported by the supplied paragraph and give a faithful English alternative. Do not invent data.

4. I instead need to verify a new claim against recent published literature: “All retrieval tools improve learning outcomes.” With no literature supplied and browsing outside this task, state which project skill owns the request and which evidence is missing. Do not invent a reference.
'''
    (workspace / "prompt.txt").write_text(prompt, "utf-8")
    argv = [str(native), "exec", "--json", "--ephemeral", "--skip-git-repo-check",
            "--approve-for-me", "--cd", str(workspace),
            "--color", "never", "--output-last-message", str(workspace / "answer.md"), "-"]
    attempt = private / "pilot-attempt-02"
    attempt.mkdir(exist_ok=False)
    output, errors = attempt / "stdout.jsonl", attempt / "stderr.log"
    receipt = {"evidence_class": "agent-development-native-command-observation",
               "authority": "User authorizes direct self-authored tests, unlimited budget, project only",
               "requested_model": "inherit", "requested_effort": "inherit",
               "resolved_model_from_configuration": configuration.get("model"),
               "resolved_effort_from_configuration": configuration.get("model_reasoning_effort"),
               "effective_model": "unknown until native telemetry", "cost": "unknown",
               "executable_sha256": hashlib.sha256(native.read_bytes()).hexdigest(),
               "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
               "workspace": str(workspace), "command": argv, "status": "starting"}
    def started(pid):
        receipt.update(status="running", pid=pid)
        (attempt / "receipt.json").write_text(json.dumps(receipt, indent=2), "utf-8")
        print(json.dumps({"status": "running", "pid": pid, "workspace": str(workspace)}), flush=True)
    result = run_owned_command(argv, workspace, prompt.encode("utf-8"), output, errors,
                               timeout=600, on_started=started)
    receipt.update(result)
    for label, path in (("stdout", output), ("stderr", errors)):
        receipt[label + "_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
    (attempt / "receipt.json").write_text(json.dumps(receipt, indent=2), "utf-8")
    print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
