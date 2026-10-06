# Counsel: r39 pinned regression failures

## TL;DR

The preserved `p7-pinned-tests-attempt-01.txt` result has four independent
fixture/integration issues; `verify_bundle()` is correctly enforcing the
package boundary.

1. Acceptance expects 35 profile sources, while the current profile contains
   36.
2. The writer test expects 9 registry resources, while the current registry
   contains 13.
3. The isolated rights-drift fixture copies resource files but not the newly
   required `core/registry/catalog/skills.json`.
4. The isolated reader imports local helpers and writes `__pycache__` into the
   extracted bundle; the post-smoke `verify_bundle()` correctly rejects that
   unowned file.

Repair the candidate source/test freeze together, copy the current skills
catalog into the isolated fixture, and set `sys.dont_write_bytecode = True`
before local imports in the read-only CLI entry points. Preserve the failed
run and require the affected tests plus an isolated before/after no-write check
to pass before calling r39/337 complete.

## Verified findings

### Current count assertions are stale

- `tests/acceptance/test_profile.py:25` asserts
  `len(self.profile["sources"]) == 35`; the retained run reports the current
  profile value as 36.
- `tests/resource/test_writer_consumers.py:78` asserts
  `len(registry["resources"]) == 9`; the retained run reports the current
  registry value as 13.
- These are exact membership/count assertions, so changing them is a source
  freeze decision. For the current candidate, reconcile them to 36 and 13
  after confirming those values in the corrective r39 freeze. Do not remove a
  current source/resource or weaken the equality to make the old historical
  constants pass. If the intended r39 freeze still says 35/9, the integration
  itself must be corrected instead; do not silently choose a new baseline.

### Legacy resource fixture is incomplete

- `tests/resource/test_writer_consumers.py:58-59` copies only
  `core/profiles/resources` into the isolated target and then creates the
  `resources.json` catalog.
- The current `scripts/search-resource.py:239` reads and validates
  `core/registry/catalog/skills.json` before selecting a resource consumer.
- The rights-drift test therefore reaches the new catalog read and fails with
  `FileNotFoundError` before it can exercise the intended rights-hash drift.
- The fixture should copy the current `core/registry/catalog/skills.json` to
  the corresponding target catalog path, alongside the copied resource files.
  This supplies the real exact consumer catalog and keeps the test’s rights
  mutation focused on `resources.json`.

### Isolated reader creates unowned bytecode

- `tests/resource/test_extracted_smoke.py:20-31` verifies the extracted bundle,
  runs the smoke reader, and verifies the same extracted bundle again. That
  second verification is a meaningful no-write regression and must remain.
- `scripts/resource-smoke.py:53-56` launches each extracted reader with
  `python -I`, a bundle path, and `PYTHONPATH` removed. Isolated mode does not
  disable bytecode generation.
- `scripts/search-resource.py:15-18` imports local `core` helpers without
  disabling bytecode. The child reader consequently writes `__pycache__` into
  the extracted package during smoke.
- `core/build.py:509-515` enumerates actual bundle files and compares them with
  the declared manifest set; the resulting
  `ContractError("artifact has missing or unowned files")` is the correct
  response to that extra file.
- `scripts/check-research-artifacts.py:7-10` has the same local-import shape
  and should apply the same read-only entry-point invariant before its imports.
  The flag must be set before any local `core` import:

  ```python
  sys.dont_write_bytecode = True
  sys.path.insert(0, str(ROOT))
  from core...
  ```

  Do not delete `__pycache__` after the CLI runs; that would hide the write
  regression. Do not rely only on a caller environment variable; the entry
  points must be safe when invoked directly with `-I`.

## Cause-aligned repair order

1. Confirm the intended current r39 counts, then update the exact profile and
   resource assertions together with the corrective source freeze (36 sources,
   13 resources if the current candidate is authoritative).
2. Extend the rights-drift fixture with the current `skills.json` catalog.
3. Set `sys.dont_write_bytecode = True` before local imports in
   `search-resource.py` and `check-research-artifacts.py`.
4. Preserve the post-smoke `verify_bundle(extracted)` call and run an isolated
   snapshot comparison around both CLIs: the helper-tree file set must be
   unchanged after the read-only CLI, while the checker receipt is written only
   in its explicitly separate project/output location.

No change to `verify_bundle()` is justified. No source-lock bypass, ACL change,
bytecode cleanup, production reader relaxation, or test assertion weakening is
appropriate.

## Affected verification

Run the repaired checks serially from
`C:/Users/USER/Downloads/test-skill/nckh-kit`:

```text
python -B -m unittest tests.acceptance.test_profile.AcceptanceProfileTests
python -B -m unittest tests.resource.test_writer_consumers.WriterConsumerTests
python -B -m unittest tests.resource.test_extracted_smoke.ExtractedSmokeTests
```

Then rerun the planned isolated before/after helper-tree regression for both
read-only CLIs and retain the original `p7-pinned-tests-attempt-01.txt` as a
failed historical attempt. The original 78-test result was 2 failures and 2
errors; it is not a green r39/337 gate.

## Status

Status: DONE

Summary: Stale counts, an incomplete skills-catalog fixture, and child-reader
bytecode writes account for the four failures. Reconcile the current source
freeze, copy `skills.json`, disable bytecode before local CLI imports, and keep
the post-smoke bundle verification as the no-write guard.

Concerns/Blockers: The pinned gate remains incomplete until the corrective
freeze and affected reruns pass. No background Python process remains from the
failed run, so there is no process cleanup blocker.
