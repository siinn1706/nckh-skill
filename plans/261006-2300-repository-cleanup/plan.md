# Repository publication and cleanup

Status: in progress. Target: existing `siinn1706/nckh-skill` repository, main.

## Outcome and constraints

Keep one working repository at the workspace root, publish important source,
reference acquisitions, plans and reviewed execution evidence. Preserve upstream
licenses, pinned source/package bytes, experimental qualification labels and
local installation ownership. The user explicitly authorized reference resources
and reviewed run evidence for this public repository.

Raw evidence remains local when a sanitized public copy is necessary. Do not
publish credentials, personal machine configuration, private installation
backups or runtime databases. Do not disturb concurrent runs or locked folders.

## Phases

1. Inventory source, publication checkout, reference resources and evidence.
2. Consolidate Git and public tools at root; preserve recoverable originals.
3. Review publication files, redact private evidence and document navigation.
4. Verify package integrity and publication hygiene, commit and push normally.
5. Archive redundant exports and temporary artifacts; verify final local and
   remote state.

## Acceptance

The root checkout retains existing Git history, the remote commit matches local
HEAD, public packages verify against the unchanged source lock, references keep
their license files, and removed/replaced local artifacts have recovery records.
Active and access-denied directories remain explicitly reported when cleanup
cannot safely include them.

## Recovery

Keep the pre-cleanup checkout and moved artifacts in the ignored
`plans/local-backups/repository-cleanup-261006-2300/` directory. Restore only the
recorded paths. Public evidence substitutions are labelled and originals are
retained there. Publication does not establish native/scientific acceptance.
