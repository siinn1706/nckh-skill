# Review-only: django__django-10087 fixtures

Case `real-source-django-code-review-01`. Static reading of packaged `code_fixtures` only. The fixtures were not executed. No file was edited and no patch is included.

## Source receipt and inspected scope

- `source_id`: `django__django-10087`
- Locator: `https://huggingface.co/datasets/SWE-bench/SWE-bench`
- Reader query: `django__django-10087`
- Reader: `C:/Users/USER\Downloads\test-skill\.agents\skills\nckh-code-review\references\_shared\scripts\search-resource.py`
- Pack: `R-django-sqlmigrate-fixtures`, domain `engineering-task`, locale `en`, genre `code-review-fixture`, consumer `nckh-code-review`
- Receipt: `plans/evaluation/personal-use/native/cursor-grok-r24/reader-receipts/nckh-code-review__R-django-sqlmigrate-fixtures__django__django-10087.json`
- Status: `matched`, one record
- Field used: plural `code_fixtures` (length 2). The record has no singular `code_fixture` key.
- Pack `resource_sha256`: `e81048922d196fd302555f192d289d51d82449b0ae724fc05cb2e2b4bfeb90cf`
- `record_sha256`: `3600a5e446a811f585fe3bc7c044cf7305db5815e2a9ff04ec1168ee52b318a8`
- `reader_sha256`: `e8eb4cb75cc3220f41f85502cd40fa93fd7e258f6629b0e2588367c1165fdffb`
- Base commit on both fixtures: `02cd16a7a04529c726e5bb5a13d5979119f25c7d`
- License label: `BSD-3-Clause`
- License URL: `https://raw.githubusercontent.com/django/django/02cd16a7a04529c726e5bb5a13d5979119f25c7d/LICENSE`
- License SHA-256: `b846415d1b514e9c1dff14a22deb906d794bc546ca6129f950a18cd091e2a669`
- License scope in the record: BSD 3-Clause evidence applies only to the two upstream Django code fixtures at this commit. Issue-authored text, benchmark patch, and dataset row stay out of scope.
- `task_locator.private_fields` lists `problem_statement`, `patch`, `test_patch`, `issue_body`, and `dataset_row`. Those fields are not in the record. Their text was not read.

Inspected fixture bytes, hashes matched after UTF-8 encoding of `content`:

| Upstream path | SHA-256 | Bytes | Lines read |
|---|---|---|---|
| `django/core/management/commands/sqlmigrate.py` | `6ca06cab795d7b1f1247c1a1327ac0ec54bc9295c68e3cbc95ac7f10be817371` | 2742 | `class Command` at line 7; `handle` at line 31; file through line 59 |
| `tests/migrations/test_commands.py` | `c69753ae276a6815faf1abdd0f78d6ab4770d65ec8ba1f38698d73e34832c81a` | 67864 | `test_sqlmigrate_forwards` at line 427; `test_sqlmigrate_backwards` at line 465; `test_sqlmigrate_for_non_atomic_migration` at line 510 |

`handle` resolves the app and migration, sets `self.output_transaction = migration.atomic`, builds one plan node, and returns `executor.collect_sql(plan)`. The forwards test checks transaction and operation order. The backwards test applies the migration, requests `backwards=True`, then checks reverse order. The non-atomic test asserts transaction SQL is absent from the split output lines when the backend exposes it.

Not executed: Django, the tests, or any database. No security guarantee, benchmark result, or ticket resolution is claimed.

## Findings or explicit no-finding result

One actionable finding in the backwards test. No actionable defect was established in `Command.handle` from static reading alone.

### Finding 1

- Severity: low
- File and line: `tests/migrations/test_commands.py`, lines 501–503, with `index_drop_table` assigned at line 480
- Impact: `test_sqlmigrate_backwards` can pass when the transaction-end marker is after the unique_together comment and before `DROP TABLE`. The failure string says the check is about `DROP TABLE`.
- Why, static only: line 480 sets `index_drop_table = output.rfind('drop table')`. Lines 497–500 compare `index_drop_table` with `index_op_desc_author`. Lines 501–503 then execute `self.assertGreater(index_tx_end, index_op_desc_unique_together, "Transaction end not found or found before DROP TABLE")`. The compared value is `index_op_desc_unique_together`, not `index_drop_table`. This run did not execute the test, so no runtime pass/fail is reported.
- Required edit: point that assertion at `index_drop_table`, or change the message so it names the unique_together comment that the comparison actually uses. No edit was applied.

Unverified, not filed as a finding: `handle` assigns `self.output_transaction` on the instance. Reuse of the same command object was not in the inspected callers.

## Evidence/reproduction and required edit for each finding

The reproduction is the static mismatch above. Required edit is the assertion-target or message correction stated in Finding 1. No patch, diff, or code change is part of this review.

## Rights and review limitations

BSD-3-Clause is recorded only for these two fixture contents at commit `02cd16a7a04529c726e5bb5a13d5979119f25c7d`. The review does not cover ticket intent, a benchmark patch, or tests outside the three named methods. Absence of a runtime run means unexecuted branches stay unverified. This is not a merge, publish, or security clearance. Owner score remains `pending-personal-review`.
