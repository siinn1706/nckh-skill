# Plan and cook state

Plan captures outcome, constraints, non-goals, acceptance and source-backed options
and writes them as the Plan artifact below. --validate runs the plan checker, then
reads all phases, checks current source/permissions/dependencies/owners/oracles/rollback
and reports VERIFIED/FAILED/UNVERIFIED claims. Unknown flags have no invented semantics.

Cook accepts optional --auto or --interactive, never both. Preserve an accepted
plan's mode. Without a mode, continue already-authorized implementation, checks
and delivery. Ask only for a material missing decision or an action outside that
authorization. Auto completes authorized phases without routine confirmation;
required human/license/egress and irreversible boundaries without a grant still
wait. There is no stable --no-test shortcut.

Progression: planned -> authorized -> running -> checking -> ready-for-review ->
accepted. Waiting-human, blocked, failed and timeout-unknown require a reason and
next action. State is durable private task data, not chat memory or permission proof.

For interactive work define substantive boundaries before downstream material work:
protocol, thesis/outline, visual pilot, UX or campaign message. Give artifact path/hash,
revision, changed scope, checks/limits and approve/request-changes/reject decision.
Wait for actual feedback. Bind it to the exact artifact; invalidate descendants on
change and reauthorize affected scope. Technical phases may join when no material
decision is crossed; do not ask after every file.

Resume reopens state and artifacts, reconciles outstanding handles before retry,
verifies scope/input/profile/closure hashes and retains past failed attempts.
A source file existing does not prove a phase passed. Review and handoff aggregate
gates without creating their own competing execution lifecycle.

## Plan artifact

Write the plan to files in the repository's plan location; when none exists, ask
once, then record the chosen location in the new plan's own `plan.md` frontmatter
and in task state once the plan directory exists. A plan shown only in chat is not an
artifact. `plan.md` is the index: frontmatter, outcome, acceptance and a phase
table that links every phase file. Two or more dependent steps require one
`phase-NN-slug.md` per phase with Requirements, Files, Steps, Checks and
Risk/Rollback sections; only a single-step task may stay in `plan.md` alone.

Deliverable verbs inside a planning request (write the report, export a PDF, take
screenshots) become phases assigned to nckh-cook; planning creates none of those
deliverables. A done/completed/verified status in `plan.md` or a `phase-NN-*.md`
file needs a receipt link on the same line or a frontmatter `receipt:`; without
one the phase stays planned.

Validator: run [`check-plan.py`](../../scripts/check-plan.py) `<plan-dir>` before handoff and report its verdict and exit status.

## Command discipline

Run each dependent command as its own invocation and record that command's own
exit status: `$LASTEXITCODE` right after a native command in PowerShell, `$?` in
bash. When a step fails, stop the steps that depend on it. The last exit of a
chain joined by `;`, `&`, `&&`, `||` or a pipe, or an output file left by an earlier
run, is not evidence that a step passed. A command expected to fail records
`expected_nonzero: true`. Record every command in receipt v2 `command_results`
with shell, cwd, exit status, stdout/stderr hashes and, for an unavoidable
chain, `segment_exit_statuses`.

Validator: [`check-receipt.py`](../../scripts/check-receipt.py) `verify --receipt <receipt>` rejects missing segment exits and a failing step hidden behind a passing total.

## Attempt ledger

Start an attempt with `check-receipt.py inventory --root <workspace> --output <new-path>`.
Put `<new-path>` outside the workspace being measured (for example beside a plan
kept outside it) so the inventory file is not counted as created by the attempt.
The final answer separates four lists: `existing-before-attempt`,
`created-this-attempt`, `verified-this-attempt` and `unverified`. VERIFIED applies
only to a claim backed by a command run in the current attempt with its recorded
exit. Every reported hash, count or size is the output of a recorded command;
never write a value before measuring it. A figure inherited from an earlier
artifact, slide, dashboard or user restatement without a locator in this
attempt's inputs is `unverified` and cannot be stated as fact. A file or receipt
that predates the attempt is `existing-before-attempt` until rechecked.

Keep task state and attempt records in the task's plan directory by default;
otherwise ask once and record the chosen location in the state.

Validator: [`check-receipt.py`](../../scripts/check-receipt.py) `verify --receipt <receipt> --before <inventory> --workspace <dir>` recomputes hashes on disk and compares created files with the inventory.

## Host shell robustness

- Run Python as `python -X utf8`, or set `PYTHONIOENCODING=utf-8`; Windows consoles
  default to a legacy code page.
- Put a multi-line or long script in a UTF-8 file and run that file; do not pass
  multi-line code through `python -c` or exceed the command-line length limit.
- Copy Unicode file names from a directory listing; never ASCII-fold or retype them.
- Write text with an explicit UTF-8 encoding. Windows PowerShell 5.1 `Set-Content`
  and `Out-File` default to ANSI or UTF-16, and `-Encoding utf8` adds a BOM; write
  through Python with `encoding="utf-8"` and keep an edited file's original BOM/EOL.

Validator: [`check-receipt.py`](../../scripts/check-receipt.py) `verify` compares recorded hashes and EOL with the files on disk, which exposes an encoding or line-ending change.

## Personal-use acceptance

The shared default is the `personal-use` profile at
`core/profiles/acceptance/personal-use.json`. It is looked up by exact skill ID
and supplies route/identity, positive behavior, output/facts,
authority/side-effect and receipt/feedback checks. The profile has no universal
percentage and does not change the catalog status from `experimental`.

An owner may score the final personal-use result and request a revision. An
external reviewer, protected holdout or human-gold corpus is not required for
this lane. Missing owner feedback remains `pending-personal-review`; any
feedback must identify the current revision, artifact hash and input hashes.
Mismatched feedback is rejected, and a personal-use verdict never certifies
stable, scientific, native, provider or venue acceptance.

Already-authorized reversible routine phases continue with or without `--auto`.
Personal-use delivery may be ready for the owner to use while final taste and
owner feedback remain pending. Required rights, provider, paid, external and
irreversible actions still need their actual scope grant; honor grants already
given in the session. The historical qualification protocol and its
holdout/reviewer gates are read-only from this lane.
