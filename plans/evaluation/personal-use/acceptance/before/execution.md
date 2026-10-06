# Plan and cook state

Plan captures outcome, constraints, non-goals, acceptance, source-backed options and
a short index with phase detail when complexity warrants it. --validate reads all
phases, checks current source/permissions/dependencies/owners/oracles/rollback and
reports VERIFIED/FAILED/UNVERIFIED. Unknown flags have no invented semantics.

Cook accepts --auto or --interactive, never both. Preserve an accepted plan's mode.
Without a mode, state the proposed interactive default before work. Auto completes
all authorized phases without routine confirmation; mandatory human/license/egress
and irreversible boundaries still wait. There is no stable --no-test shortcut.

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
