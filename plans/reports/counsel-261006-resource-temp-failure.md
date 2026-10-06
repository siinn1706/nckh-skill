# Counsel: P5 research-pack fixture failure on Windows

## TL;DR

The two errors are a Windows fixture/ACL failure in the default `%TEMP%` tree,
not evidence that the resource reader opened a pack incorrectly. The minimal
cause-aligned remedy is to replace `tempfile.TemporaryDirectory()` in
`tests/resource/test_research_packs.py` with the repository's existing
`core.paths.temporary_tree(ROOT.parent)` context. This keeps the fixture under
the writable workspace and lets the owning helper perform bounded cleanup.

Do not escalate the shell, change ACLs, kill processes, or modify
`core/research_io.py` for this checkpoint. Escalation could make the current
machine pass while leaving the test dependent on the restricted `%TEMP%`
behavior.

## Evidence

- The controller's run of
  `python -B -m unittest tests.resource.test_research_packs.ResearchPackContractTests`
  reached `.....E.E.......`: 13 tests passed and two tests errored during fixture
  creation or cleanup. The first error occurred at
  `path.parent.mkdir(parents=True)` below a `tempfile.TemporaryDirectory()`
  root; the second test's assertions completed but its temporary-directory
  cleanup received `PermissionError [WinError 5]`.
- `tests/resource/test_research_packs.py:49` and `:55` are the only tests in
  this class that use `tempfile.TemporaryDirectory()`. The file has no
  application behavior that requires the standard-library temporary context.
- `core/paths.py:82-96` defines `temporary_tree`. Its docstring records the
  Windows reason for the helper, creates the child with mode `0o777` on
  Windows, verifies that the resolved child remains below its supplied parent,
  rejects linked paths, and removes only that owned child in `finally`.
- Existing resource tests already use this helper, including
  `tests/resource/test_writer_consumers.py:58` for a copied registry/resource
  fixture. This is the local convention for owned filesystem fixtures.
- `scripts/search-resource.py:227-230` returns `resource-disabled` before
  touching the registry when `resource_access == "off"`. The same reader loads
  the registry before checking consumer/locale/genre and checks domain before
  `_verify_source` (`scripts/search-resource.py:233-251`). Moving the fixture
  root does not weaken these no-read paths; it only makes the root constructible
  and cleanable.
- P5 explicitly requires actual local ON reads plus OFF/no-read behavior and
  wrong-context no-read behavior before the P6 handoff
  (`plans/261005-0036-nckh-devops-aiops-research-upgrade/phase-05-curated-research-resources.md`,
  implementation step 6 and verification section). A fixture error must remain
  recorded as an incomplete gate until the focused run exits cleanly.

## Recommended minimal change

In `tests/resource/test_research_packs.py`:

1. Remove the `tempfile` import.
2. Import `temporary_tree` from `core.paths`.
3. Change both contexts to `with temporary_tree(ROOT.parent) as folder:`.

`ROOT.parent` is the workspace root (`C:/Users/USER/Downloads/test-skill`),
which is in the permitted writable area for this run. Passing the parent
explicitly matters: `temporary_tree()` without an argument still defaults to
`tempfile.gettempdir()`, so it may reproduce the restricted `%TEMP%` ACL on
this machine. The helper yields a `Path`; the existing `Path(folder)` use in
the mismatch test remains harmless.

No production source change is indicated. In particular, do not reorder the
reader's eligibility checks, add a resource stub, or catch `PermissionError`
around fixture cleanup. Swallowing cleanup errors would convert an environment
failure into a false green result.

## Why this preserves the required evidence

- `test_off_never_needs_registry_or_resource_files` can continue to pass an
  empty, workspace-owned root. The reader should return
  `{"status": "resource-disabled", "resource_read": False}` before any path
  lookup. The fixture context only supplies a valid root and does not add
  registry/resource files.
- `test_mismatches_do_not_open_resource_files` still copies only
  `core/registry/catalog/resources.json`. Consumer, locale, and genre mismatch
  cases must raise before `_verify_source`; a domain mismatch must return with
  `resource_read == False`. The workspace location does not change those
  branches.
- Cleanup remains scoped to the unique child created by `temporary_tree` and
  is guarded by its containment/link checks. The test should not call broad
  `%TEMP%` cleanup or manually remove a parent directory.

## Validation after the edit

Run from `C:/Users/USER/Downloads/test-skill/nckh-kit`:

```text
python -B -m unittest tests.resource.test_research_packs.ResearchPackContractTests
```

Record the complete exit code and summary. The acceptance target is 15 tests
with zero errors/failures. If the focused run is clean, run the neighboring
resource contract classes required by the P5 gate (`test_consumers`,
`test_real_sources`, `test_writer_consumers`, and `test_closure`) as the next
serial verification step. Do not call the gate green from the original
13-pass/2-error output, and do not retry the unchanged test merely to obtain a
different `%TEMP%` result.

## Alternatives and trade-offs

- **Use `temporary_tree(ROOT.parent)` (recommended):** smallest test-only
  change, follows repository convention, and makes the writable boundary
  explicit. It is deterministic for this workspace and keeps cleanup local.
- **Set `TEMP`/`TMP` for the command:** useful as a one-off diagnostic, but it
  leaves the test dependent on runner environment and does not make the source
  fixture contract self-contained.
- **Escalate or alter ACLs:** unnecessary and unsafe for this checkpoint. It
  changes machine permissions to compensate for a fixture choice and does not
  improve the no-read assertions.

## Status

The P5 focused verification checkpoint remains pending until the fixture-only
change is made and the 15-test command exits cleanly. The observed failure is
environment-blocked, not a confirmed product defect.

<oai-mem-citation>
<citation_entries>
MEMORY.md:732-737|note=[prior Windows test evidence recommends a permitted workspace temp root and preserving environment-blocked failures]
</citation_entries>
<rollout_ids>
</rollout_ids>
</oai-mem-citation>
