from tests._lab import lab_root
import unittest
from pathlib import Path
from unittest import mock

from core.build import SCRIPT_REQUIREMENTS, closure, load_json, validate_catalog
from core.ledger import command_segments, eol_profile, inventory, validate_claim, validate_receipt, validate_task_state
from core.paths import digest_bytes, temporary_tree
from core.state import new_task


ROOT = Path(__file__).resolve().parents[2]
CRLF_TEMPLATE = "TIÊU ĐỀ BÁO CÁO\r\n<báo cáo tại đây>\r\nChân trang — Lab 2\r\n".encode("utf-8")
ZERO = "0" * 64


def claim(**changes):
    record = {"schema_version": 2, "id": "C1", "statement": "Export succeeded", "type": "fact",
              "scope": "lab 2", "evidence_ids": [], "verdict": "unverified", "allowed_certainty": "none",
              "counterevidence_ids": [], "profile_revision": "r1", "attempt_status": "unverified"}
    record.update(changes)
    return record


def receipt(**changes):
    record = {"schema_version": 2, "id": "R1", "evidence_class": "deterministic", "host": "local",
              "surface": "shell", "version": "1", "logical_entrypoint": "gen_report.py", "mode": "auto",
              "actual_invocation": "python gen_report.py", "requested_model": "none", "resolved_model": "none",
              "effective_model": "none", "requested_effort": "none", "resolved_effort": "none",
              "effective_effort": "none", "permission_mode": "default", "sandbox": "none",
              "tool_trace_reference": "trace.json", "egress_trace_reference": "none", "exit_status": "0",
              "output_status": "written", "cost_coverage": "none", "cost": "0", "as_of": "2026-10-08",
              "skill_ids": [], "agent_ids": [], "plugin_ids": [], "input_hashes": [], "output_hashes": [],
              "checks": [], "limitations": [], "closure_hash": ZERO,
              "command_results": [], "input_files": [], "output_files": []}
    record.update(changes)
    return record


def command(text, exit_status=0, **changes):
    record = {"command": text, "shell": "bash", "cwd": ".", "exit_status": exit_status,
              "stdout_sha256": ZERO, "stderr_sha256": ZERO, "expected_nonzero": False}
    record.update(changes)
    return record


def unchanged_input(path, data):
    return {"path": path, "sha256_before": digest_bytes(data), "sha256_after": digest_bytes(data),
            "eol_before": eol_profile(data), "eol_after": eol_profile(data), "mutation": "none"}


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.tree = temporary_tree(lab_root())
        self.root = self.tree.__enter__()
        self.addCleanup(self.tree.__exit__, None, None, None)

    def write(self, relative, data):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def assertVerdict(self, result, verdict, fragment=None):
        self.assertEqual(result["verdict"], verdict, result["findings"])
        if fragment:
            self.assertTrue(any(fragment in finding for finding in result["findings"]), result["findings"])

    def test_supported_claim_requires_evidence(self):
        self.assertVerdict(validate_claim(claim(verdict="supported")), "FAILED", "supported verdict")
        self.assertVerdict(validate_claim(claim(verdict="supported", evidence_ids=["E1"])), "VERIFIED")
        self.assertVerdict(validate_claim(claim(schema_version=1)), "FAILED", "claim schema")

    def test_verified_this_attempt_requires_evidence(self):
        self.assertVerdict(validate_claim(claim(attempt_status="verified-this-attempt")), "FAILED",
                           "verified-this-attempt")
        self.assertVerdict(validate_claim(claim(attempt_status="verified-this-attempt",
                                                evidence_ids=["receipt-R1"])), "VERIFIED")
        self.assertVerdict(validate_claim(claim(attempt_status="existing-before-attempt")), "VERIFIED")

    def test_gate_pass_or_fail_requires_evidence_reference(self):
        task = new_task({"outcome": "lab 2"}, mode="auto", revision="r1")
        self.assertVerdict(validate_task_state(task), "VERIFIED")
        for status in ("pass", "fail"):
            task["gates"] = [{"id": "export", "required": True, "status": status, "revision": "r1"}]
            self.assertVerdict(validate_task_state(task), "FAILED", f"status {status}")
            task["gates"][0]["evidence_reference"] = "receipt-R1"
            self.assertVerdict(validate_task_state(task), "VERIFIED")
        task["gates"] = [{"id": "export", "required": True, "status": "pending", "revision": "r1"}]
        task["attempts"] = [{"handle": "a1", "status": "done", "output_hashes": [],
                             "created_this_attempt": ["out/bao-cao.txt"]}]
        self.assertVerdict(validate_task_state(task), "FAILED", "no output hash")

    def test_compound_command_requires_segment_exit_statuses(self):
        compound = "python gen_report.py; python export.py | tee log.txt && echo ok || echo bad"
        self.assertEqual(len(command_segments(compound)), 5)
        self.assertEqual(command_segments('echo "a; b | c" && find . -exec rm {} \\;'),
                         ['echo "a; b | c"', "find . -exec rm {} \\;"])
        self.assertEqual(len(command_segments("Write-Output 'x;y'; Get-Item `;z", "pwsh")), 2)
        self.assertVerdict(validate_receipt(receipt(command_results=[command(compound)])), "FAILED",
                           "no segment_exit_statuses")
        self.assertVerdict(validate_receipt(receipt(command_results=[
            command(compound, segment_exit_statuses=[0, 0])])), "FAILED", "2 segment exit statuses")
        self.assertVerdict(validate_receipt(receipt(command_results=[
            command(compound, segment_exit_statuses=[0, 0, 0, 0, 0])])), "VERIFIED")
        self.assertVerdict(validate_receipt(receipt(command_results=[command('echo "a;b"')])), "VERIFIED")

    def test_nonzero_segment_cannot_yield_passing_receipt(self):
        masked = command("python gen_report.py; python export.py", 0, segment_exit_statuses=[2, 0])
        for overall in ("0", "pass", "PASS"):
            self.assertVerdict(validate_receipt(receipt(exit_status=overall, command_results=[masked])),
                               "FAILED", "hides unexpected nonzero")
        self.assertVerdict(validate_receipt(receipt(exit_status="2", command_results=[masked])), "VERIFIED")
        failed = command("python gen_report.py", 2)
        self.assertVerdict(validate_receipt(receipt(command_results=[failed])), "FAILED", "hides")
        expected = command("python gen_report.py", 2, expected_nonzero=True)
        self.assertVerdict(validate_receipt(receipt(exit_status="pass", command_results=[expected])), "VERIFIED")

    def test_unchanged_input_detects_hash_and_eol_change(self):
        self.write("mẫu-báo-cáo.txt", CRLF_TEMPLATE)
        self.write("__pycache__/x.pyc", b"\x00")
        before = inventory(self.root)
        self.assertEqual(list(before["files"]), ["mẫu-báo-cáo.txt"])
        self.assertEqual(before["files"]["mẫu-báo-cáo.txt"]["eol"], "crlf")
        lf = CRLF_TEMPLATE.replace(b"\r\n", b"\n")
        self.write("mẫu-báo-cáo.txt", lf)
        honest = {**unchanged_input("mẫu-báo-cáo.txt", CRLF_TEMPLATE),
                  "sha256_after": digest_bytes(lf), "eol_after": "lf"}
        result = validate_receipt(receipt(input_files=[honest]), before=before, workspace=self.root)
        self.assertVerdict(result, "FAILED", "unauthorized EOL change crlf -> lf")
        self.assertVerdict(result, "FAILED", "unauthorized content change")
        claimed = unchanged_input("mẫu-báo-cáo.txt", CRLF_TEMPLATE)
        self.assertVerdict(validate_receipt(receipt(input_files=[claimed]), before=before, workspace=self.root),
                           "FAILED", "after-state does not match disk")
        self.write("mẫu-báo-cáo.txt", CRLF_TEMPLATE)
        self.assertVerdict(validate_receipt(receipt(input_files=[claimed]), before=before, workspace=self.root),
                           "VERIFIED")

    def test_output_over_input_requires_preimage(self):
        new = CRLF_TEMPLATE.replace("<báo cáo tại đây>".encode("utf-8"), b"Ket qua")
        self.write("mẫu-báo-cáo.txt", new)
        overwrite = {**unchanged_input("mẫu-báo-cáo.txt", CRLF_TEMPLATE), "sha256_after": digest_bytes(new)}
        output = {"path": "mẫu-báo-cáo.txt", "sha256": digest_bytes(new), "created_this_attempt": False}
        self.assertVerdict(validate_receipt(receipt(input_files=[overwrite], output_files=[output]),
                                            workspace=self.root), "FAILED", "without an authorized preimage")
        authorized = {**overwrite, "mutation": "authorized-with-preimage", "preimage_path": "preimage/mẫu.txt"}
        record = receipt(input_files=[authorized], output_files=[output])
        self.assertVerdict(validate_receipt(record), "FAILED", "without a workspace")
        self.assertVerdict(validate_receipt(record, workspace=self.root), "FAILED", "missing on disk")
        self.write("preimage/mẫu.txt", b"other bytes")
        self.assertVerdict(validate_receipt(record, workspace=self.root), "FAILED", "preimage hash differs")
        self.write("preimage/mẫu.txt", CRLF_TEMPLATE)
        self.assertVerdict(validate_receipt(record, workspace=self.root), "VERIFIED")

    def test_receipt_hash_must_match_disk(self):
        planned = "BẢN DỰ KIẾN\n".encode("utf-8")
        written = "BẢN THẬT\n".encode("utf-8")
        self.write("out/bao-cao.final.txt", written)
        early = {"path": "out/bao-cao.final.txt", "sha256": digest_bytes(planned), "created_this_attempt": True}
        self.assertVerdict(validate_receipt(receipt(output_files=[early]), workspace=self.root),
                           "FAILED", "recorded sha256 does not match disk")
        measured = {**early, "sha256": digest_bytes(written)}
        self.assertVerdict(validate_receipt(receipt(output_files=[measured]), workspace=self.root), "VERIFIED")
        escaping = {**measured, "path": "../outside.txt"}
        self.assertVerdict(validate_receipt(receipt(output_files=[escaping]), workspace=self.root), "FAILED")

    def test_created_this_attempt_matches_before_inventory(self):
        stale = "BẢN CŨ từ phiên trước\n".encode("utf-8")
        self.write("out/bao-cao.txt", stale)
        before = inventory(self.root)
        fresh = "Báo cáo mới\n".encode("utf-8")
        self.write("out/bao-cao.final.txt", fresh)
        reused = {"path": "out/bao-cao.txt", "sha256": digest_bytes(stale), "created_this_attempt": True}
        self.assertVerdict(validate_receipt(receipt(output_files=[reused]), before=before, workspace=self.root),
                           "FAILED", "existed before the attempt")
        created = {"path": "out/bao-cao.final.txt", "sha256": digest_bytes(fresh), "created_this_attempt": False}
        self.assertVerdict(validate_receipt(receipt(output_files=[created]), before=before, workspace=self.root),
                           "FAILED", "was absent before the attempt")
        honest = [{**reused, "created_this_attempt": False}, {**created, "created_this_attempt": True}]
        self.assertVerdict(validate_receipt(receipt(output_files=honest), before=before, workspace=self.root),
                           "VERIFIED")

    def test_inventory_does_not_need_path_is_junction(self):
        def missing(_self):
            raise AttributeError("Path.is_junction needs Python 3.12")

        self.write("đầu-vào.txt", CRLF_TEMPLATE)
        with mock.patch.object(Path, "is_junction", property(missing), create=True):
            record = inventory(self.root)
        self.assertEqual(list(record["files"]), ["đầu-vào.txt"])

    def test_lone_ampersand_separates_bash_and_cmd_commands(self):
        for shell in ("bash", "cmd"):
            with self.subTest(shell=shell):
                self.assertEqual(command_segments("pytest & echo ok", shell), ["pytest", "echo ok"])
                self.assertEqual(command_segments("python a.py 2>&1 & echo done", shell),
                                 ["python a.py 2>&1", "echo done"])
                self.assertEqual(command_segments("tool >&2 && next", shell), ["tool >&2", "next"])
                masked = command("pytest & echo ok", 0, shell=shell)
                self.assertVerdict(validate_receipt(receipt(command_results=[masked])), "FAILED",
                                   "no segment_exit_statuses")
        self.assertEqual(command_segments("run &> log.txt; next"), ["run &> log.txt", "next"])
        self.assertEqual(command_segments("sleep 1 &"), ["sleep 1"])
        self.assertEqual(command_segments("& python a.py; Write-Output x", "pwsh"),
                         ["& python a.py", "Write-Output x"])
        self.assertEqual(command_segments(r"& 'C:\a b\x.exe' --flag", "powershell.exe"),
                         [r"& 'C:\a b\x.exe' --flag"])

    def test_cmd_quoting_uses_double_quotes_and_literal_caret(self):
        self.assertEqual(command_segments("echo it's && exit 1", "cmd"), ["echo it's", "exit 1"])
        self.assertEqual(command_segments('echo "x^" & exit 1', "cmd.exe"), ['echo "x^"', "exit 1"])
        self.assertEqual(command_segments('echo "a & b" & exit 1', "cmd"), ['echo "a & b"', "exit 1"])
        self.assertEqual(command_segments("echo a^&b & exit 1", "cmd"), ["echo a^&b", "exit 1"])
        self.assertEqual(command_segments("echo a;b", "cmd"), ["echo a;b"])

    def test_bash_substitutions_and_comments_do_not_split(self):
        self.assertEqual(command_segments("echo $(date; whoami) && ls"), ["echo $(date; whoami)", "ls"])
        self.assertEqual(command_segments('echo "$(a; b)" | c'), ['echo "$(a; b)"', "c"])
        self.assertEqual(command_segments("echo $((1 + 2)); x"), ["echo $((1 + 2))", "x"])
        self.assertEqual(command_segments("diff <(a; b) c"), ["diff <(a; b) c"])
        self.assertEqual(command_segments("echo `a; b`; c"), ["echo `a; b`", "c"])
        self.assertEqual(command_segments("make # build; deploy"), ["make"])
        self.assertEqual(command_segments("make # note\nnext"), ["make", "next"])
        self.assertEqual(command_segments("echo a#b; echo ${#x}"), ["echo a#b", "echo ${#x}"])

    def test_v1_record_clear_message(self):
        task = new_task({"outcome": "lab 2"}, mode="auto", revision="r1")
        message = "schema_version 1 is unsupported for {}; regenerate the record as schema_version 2"
        for kind, validator, record in [("claim", validate_claim, claim()), ("receipt", validate_receipt, receipt()),
                                        ("task-state", validate_task_state, task)]:
            with self.subTest(kind=kind):
                record["schema_version"] = 1
                result = validator(record)
                self.assertVerdict(result, "FAILED", message.format(kind))
                self.assertEqual(len(result["findings"]), 1)
                record["schema_version"] = True
                self.assertNotIn(message.format(kind), " ".join(validator(record)["findings"]))

    def test_heredoc_body_not_split(self):
        command = "cat <<EOF > notes.txt\nx; y && z | w\nEOF\necho done"
        self.assertEqual(command_segments(command), ["cat <<EOF > notes.txt\nx; y && z | w\nEOF", "echo done"])
        self.assertEqual(command_segments("cat <<EOF | tr a b\n1;2\nEOF"), ["cat <<EOF\n1;2\nEOF", "tr a b"])
        self.assertEqual(command_segments("a <<ONE && b <<TWO\n1;\nONE\n2;\nTWO\nlast"),
                         ["a <<ONE\n1;\nONE", "b <<TWO\n2;\nTWO", "last"])

    def test_heredoc_dash_and_quoted_delimiters(self):
        self.assertEqual(command_segments("cat <<-END\n\ta; b\n\tEND\nnext"), ["cat <<-END\n\ta; b\n\tEND", "next"])
        self.assertEqual(command_segments("cat <<'END'\n$x; y\nEND\nnext"), ["cat <<'END'\n$x; y\nEND", "next"])
        self.assertEqual(command_segments('cat << "E N D"\na|b\nE N D\nnext'), ['cat << "E N D"\na|b\nE N D', "next"])
        self.assertEqual(command_segments("cat <<\\END\na;b\nEND\nnext"), ["cat <<\\END\na;b\nEND", "next"])
        # Without <<- an indented terminator does not close the body.
        self.assertEqual(command_segments("cat <<END\na\n\tEND\nb"), ["cat <<END\na\n\tEND\nb"])

    def test_unterminated_heredoc(self):
        self.assertEqual(command_segments("cat <<EOF\na; b\nc && d"), ["cat <<EOF\na; b\nc && d"])
        self.assertEqual(command_segments("cat <<EOF"), ["cat <<EOF"])

    def test_here_string_not_heredoc(self):
        self.assertEqual(command_segments('cat <<< "a;b"; next\nlast'), ['cat <<< "a;b"', "next", "last"])
        self.assertEqual(command_segments("cat <<<word\nnext"), ["cat <<<word", "next"])
        self.assertEqual(command_segments('echo "<<EOF"\na; b'), ['echo "<<EOF"', "a", "b"])
        for shell in ("cmd", "pwsh"):
            with self.subTest(shell=shell):
                self.assertEqual(command_segments("x <<EOF\nnext\nEOF", shell), ["x <<EOF", "next", "EOF"])

    def test_arithmetic_shift_not_heredoc(self):
        self.assertEqual(command_segments("(( n = 1 << 4 ))\nrm -rf x\nfalse"),
                         ["(( n = 1 << 4 ))", "rm -rf x", "false"])
        self.assertEqual(command_segments("(( x << 2 ))\nfalse"), ["(( x << 2 ))", "false"])
        self.assertEqual(command_segments("(( (a + 1) << 2 )) && false\ntrue"),
                         ["(( (a + 1) << 2 ))", "false", "true"])
        self.assertEqual(command_segments("echo $(( 1 << 4 ))\nfalse"), ["echo $(( 1 << 4 ))", "false"])
        self.assertEqual(command_segments("n=$((1<<2)); false"), ["n=$((1<<2))", "false"])
        self.assertEqual(command_segments("[[ $a < $b ]]\nfalse"), ["[[ $a < $b ]]", "false"])
        # A heredoc after a closed arithmetic command is still recognized.
        self.assertEqual(command_segments("(( n = 1 << 4 ))\ncat <<EOF\na; b\nEOF\nfalse"),
                         ["(( n = 1 << 4 ))", "cat <<EOF\na; b\nEOF", "false"])

    def test_heredoc_then_separator_splits(self):
        self.assertEqual(command_segments("cat <<EOF\nbody\nEOF\nfalse; true && echo ok"),
                         ["cat <<EOF\nbody\nEOF", "false", "true", "echo ok"])
        self.assertEqual(command_segments("cat <<EOF; false\nbody\nEOF\ntrue"),
                         ["cat <<EOF\nbody\nEOF", "false", "true"])

    def test_validator_scripts_ship_with_every_skill_reaching_the_workflow(self):
        validators = {"core/workflows/execution.md": ("scripts/check-receipt.py", "scripts/check-plan.py"),
                      "core/policies/preservation-policy.md": ("scripts/check-receipt.py",)}
        catalog = validate_catalog(load_json(ROOT / "core/registry/catalog/skills.json"))
        for skill_id, entry in sorted(catalog.items()):
            skill_dir = ROOT / entry["path"]
            members = {path.relative_to(ROOT).as_posix()
                       for path in closure(ROOT, [p for p in skill_dir.rglob("*") if p.is_file()])}
            for document, scripts in validators.items():
                if document not in members:
                    continue
                for script in scripts:
                    missing = {script, *SCRIPT_REQUIREMENTS[script]} - members
                    with self.subTest(skill=skill_id, document=document):
                        self.assertFalse(missing, f"{skill_id} reaches {document} without {sorted(missing)}")


if __name__ == "__main__":
    unittest.main()
