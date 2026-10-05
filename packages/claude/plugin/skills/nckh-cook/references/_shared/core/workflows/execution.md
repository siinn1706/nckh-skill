# Plan and cook state

Plan captures outcome, constraints, non-goals, acceptance, source-backed options and
a short index with phase detail when complexity warrants it. --validate reads all
phases, checks current source/permissions/dependencies/owners/oracles/rollback and
reports VERIFIED/FAILED/UNVERIFIED. Unknown flags have no invented semantics.

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
