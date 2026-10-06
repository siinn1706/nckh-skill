# Repository cleanup and publication

Status: completed publication and cleanup record.

## Published references

Licensed reference snapshots and source/license notices were published in
[5573a589](https://github.com/siinn1706/nckh-skill/commit/5573a5894620df56ec5b9c5f5a617320cdd82a76).
The two ClaudeKit snapshots remain local by the owner decision. Restricted
Anthropic office-document snapshots also remain local; public notices identify
source and redistribution limits.

The reviewed repository consolidation, recovery utility and evidence changes
were published in
[65cf5aa](https://github.com/siinn1706/nckh-skill/commit/65cf5aa71c7a095afe821f02404dfb58cb231b62).
The push used ordinary `origin/main`; the remote SHA matched the local commit
after push.

## Cleanup and retention

The cleanup records count at least 197,000 removed redundant/generated/runtime
files and approximately 2.6 GB. Later whole-directory removals are not fully
included in this conservative total. Owners and paths are recorded in the
[cleanup plan](../261006-2300-repository-cleanup/plan.md) and its manifests:
[cleanup](../261006-2300-repository-cleanup/cleanup-manifest.json),
[local state](../261006-2300-repository-cleanup/local-state-cleanup.json),
[protected folders](../261006-2300-repository-cleanup/protected-folder-cleanup.json),
[publication](../261006-2300-repository-cleanup/publication-manifest.json), and
[runtime workspaces](../261006-2300-repository-cleanup/runtime-workspace-cleanup.json).
The owning route is documented in
[repository maintenance](../../docs/repository-maintenance.md).
Old unimportant logs, prompts/transcripts and private installation receipts were
removed. Current installation ownership, rollback distribution and agent
configuration remain local.

The three active r41 test plans and their attempts, reports and journals were
preserved. Their reviewed public ZIP contains 42 files with personal paths
removed and stdout/stderr excluded. The compatibility checkout remains local
while those tests run. Six research acquisition JSONL files were restored
byte-exact and remain local.

The draft kit-read test was moved into its owning plan to restore the frozen
source inventory. The global deployment utility was recovered from its original
creation and patches at [scripts/install-global-kits.py](../../scripts/install-global-kits.py).
Only workspace/package/output locators were adapted. Syntax was checked;
global installation was not rerun.

## Verification

- The public-package verifier passed for Claude, Codex, Cursor and Antigravity:
  source revision 41, 43 skills, six agents, resource access ON, 13 resource types
  and 35 bindings. Pinned package/source bytes remain unchanged.
- Publication audit passed for 23,408 tracked paths with zero failures under its
  concrete credential/private-path checks.
  One upstream redaction test fixture is hash-allowlisted as synthetic content.
- Root README and docs publication links were checked against staged targets.
- Automatic review rejected the attempted broad maintenance commit/push before
  execution. The subsequent exact-blob reconciliation found that its 1,370-file
  result covered the full index, including already published source/resources.
  The staged delta had 226 matching files and 368 matches: 364 suffixes inside
  ordinary words and four scanner-source expressions (two private-key markers
  and two token-prefix alternatives). None was an actual credential.
  Full-index reconciliation inspected 3,483 ordinary-word suffix matches and
  117 remaining matches: scanner source, language codes/dictionaries, upstream
  placeholder examples and synthetic test fixtures. No real secret was found. No maintenance commit or push occurred
  at that rejection. The staged historical evidence also retains legacy
  trailing-whitespace/new-blank-line warnings reported by `git diff --check`;
  those bytes were preserved and were not changed as part of this cleanup.

This cleanup does not establish native, scientific or human acceptance. No
provider calls, paid evaluations, global installation or native acceptance tests
were run by this cleanup task.
