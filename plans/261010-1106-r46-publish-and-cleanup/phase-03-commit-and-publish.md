# Commit and publish

Status: reviewed public tree prepared; final audit and publication in progress.

## Context and files

The verified Git remote is `siinn1706/nckh-skill`, default branch `main`; the caller
has ADMIN access. Initial remote HEAD is
`fa3c5224d2dfb48d04e4145bb7668f0717587f34`, with five local skill-related commits
ahead. Stage only source, matching packages, owning docs and reviewed summary
records. Raw transcripts and machine installation receipts remain local.

The initial audit found 267 raw-output paths and 32 files containing private
machine paths in the unpublished local tree. Preserve the original local commits
and exact files under a verified local backup. Construct the public tree from
the verified remote parent, overlaying current source/packages/owning docs and
only explicitly reviewed new summary records. This preserves public history and
keeps immutable historical raw evidence local.

## Steps and validation

1. Review the complete outgoing commit range and exact staged files for secrets,
   private paths, local-only content and accidental generated test workspaces.
2. Run the publication audit and check changed documentation links.
3. Create conventional commits for the reviewed r46 source/packages and records.
4. Push normally to `origin/main`; do not force-push.
5. Verify remote HEAD equals local HEAD and retain the result in the delivery record.

## Risk and rollback

If remote moved, inspect its new commits before integrating. A public publication
rollback is a reviewed revert/new commit, never a forced rewrite of main. Stable
qualification and historical receipts retain their original status.
