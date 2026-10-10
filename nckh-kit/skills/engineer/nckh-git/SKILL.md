---
name: nckh-git
description: "Perform requested Git, branch, commit, worktree or GitHub operations (tạo commit, tạo nhánh, đẩy lên GitHub, tạo PR, sang nhánh) while preserving dirty edits and secrets. Does not auto-commit, reset, push or publish. Reviewing the resulting diff remains nckh-code-review."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-git

## Inputs and owned output

Inputs: Requested operation, actual repository/branch/diff, owned files and remote authority.

Output: Narrow Git operation and factual repository/PR status with preserved unrelated work.

## Required contracts

Read [Authorization](../../../core/policies/authorization-policy.md),
[Evidence](../../../core/policies/evidence-policy.md),
[Preservation](../../../core/policies/preservation-policy.md) and
[Acceptance](../../../core/policies/acceptance-policy.md) before work.
Run commands under [Command discipline](../../../core/workflows/execution.md#command-discipline) and [Host shell robustness](../../../core/workflows/execution.md#host-shell-robustness),
label claims with the [Attempt ledger](../../../core/workflows/execution.md#attempt-ledger) and keep inputs per
[Input preservation](../../../core/policies/preservation-policy.md#input-preservation).
Output follows the brief's locale. Same-agent is the default. Use
[model/context policy](../../../core/workflows/model-and-context.md) before delegation.

## Workflow and boundaries

Inspect repository identity, branch, staged/unstaged/untracked state and existing worktrees before a mutation. Preserve user changes and separate owned files. Do not initialize a repository, reset, force push or commit merely because another workflow finished.

Perform only the requested operation. Use conventional focused commits when commit is authorized, with no AI references in the subject or body. For trailers, explicit user or repository instructions take precedence over a host's default attribution trailer (such as Co-Authored-By); without such an instruction keep the host default. Record which source decided the trailer; scan the actual selected content for secrets/dotenv/private data. Stage exact owned paths rather than every dirty file.

For GitHub operations use current supported tooling and actual remote/PR identity. Read a multiline body from a file or structured field; preserve literal newlines. Attach created/reviewed PR artifacts when the host provides that capability.

Worktree creation/reuse follows actual repository instructions; stop owned background processes before removal. Report commands/results and remaining state. Review semantics belong to nckh-code-review; a Git action does not grant merge/publish authority.

## References

- [Execution/authority modes](../../../core/workflows/execution.md)
- [Review/handoff](../../../core/workflows/review-and-handoff.md)
