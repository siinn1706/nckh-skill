"""Keep declared hook bounds distinct from an observed native timeout response."""
import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
target = RUN / "verify-posttool-observations.py"
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
bind = lambda path: {"path":path.relative_to(WORK).as_posix(),"sha256":sha(path)}
adaptation = json.loads((RUN / "controller-adaptation.json").read_text(encoding="utf8"))
expected = next(row["sha256"] for row in adaptation["created"] if row["path"] == target.relative_to(WORK).as_posix())
assert sha(target) == expected
preimage = RUN / "verification-preimage.py"
with preimage.open("xb") as stream:
    stream.write(target.read_bytes())
text = target.read_text(encoding="utf8")
old = 'read(RUN / "terminal-exit-poll-01.json")'
assert text.count(old) == 1
text = text.replace(old, 'read(RUN / "terminal-exit-completed.json")')
old = '    results.append({"mode":mode'
assert text.count(old) == 1
text = text.replace(old, '''    elapsed = ((datetime.fromisoformat(post["completed_at"])-datetime.fromisoformat(post["started_at"])).total_seconds()
        if post.get("completed_at") else None)
    timeout_observation = None
    if mode == "timeout":
        assert elapsed is not None and elapsed >= frozen["injected_sleep_seconds"]
        assert elapsed > frozen["postToolUse_timeout_seconds"]
        case_outputs = [read(path).get("output", "") for path in RUN.glob("terminal-05-*.json")]
        case_text = re.sub(r"\\x1b\\[[0-?]*[ -/]*[@-~]", "", "\\n".join(case_outputs))
        case_text = re.sub(r"\\x1b\\][^\\x07]*\\x07", "", case_text)
        witness = bool(re.search(r"(?im)^\\s*(?:\\[[A-Z ]+\\]\\s*)?(?:hook\\s+(?:command\\s+|execution\\s+|run\\s+)?(?:failed|timed out|timeout)|hook\\s+.{0,120}\\btimed out\\b|(?:error|warning).{0,120}\\bhook\\b.{0,120}\\b(?:timed out|timeout)\\b)", case_text))
        retained = not any("truncated output" in value for value in case_outputs)
        timeout_observation = {"declared_hook_bound_seconds":frozen["postToolUse_timeout_seconds"],
            "injected_sleep_seconds":frozen["injected_sleep_seconds"],"observed_callback_elapsed_seconds":elapsed,
            "receipt_after_declared_bound":bool(selected_receipts),"explicit_native_timeout_message_observed":witness,
            "selected_terminal_retention_complete":retained,"effective_native_deadline":"unqualified"}
    results.append({"mode":mode''')
old = '"late_post_receipt":mode == "timeout" and bool(selected_receipts)})'
assert text.count(old) == 1
text = text.replace(old, '"post_callback_elapsed_seconds":elapsed,"timeout_observation":timeout_observation})')
old = '"backend_parameters_attestation":"not-observed",'
assert text.count(old) == 1
text = text.replace(old, old+'\n    "native_timeout_deadline_qualification":"unqualified; declared bound and delayed receipt only",')
compile(text, str(target), "exec")
target.write_text(text, encoding="utf8", newline="\n")
record = {"status":"retained-verifier-preimage-and-precise-scope", "before":bind(preimage), "after":bind(target),
    "reason":"Actual delayed observer completed at 8.263741 seconds; explicit native timeout message was not found in the bounded read. Do not infer effective host deadline.",
    "oracle_byte_and_content_requirements_changed":False,"case_requirements_weakened":False,"exit_zero_requirements_changed":False,
    "new_terminal_exit_anchor":"actual terminal-exit-completed tool result; early exit poll also retained", "source_kit_modified":False}
with (RUN / "observation-scope-refinement.json").open("x", encoding="utf8", newline="\n") as stream:
    stream.write(json.dumps(record,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"status":record["status"],"byte_oracles_changed":False,"effective_native_deadline":"unqualified"}))
