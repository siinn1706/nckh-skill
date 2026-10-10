# Freeze and verify

Status: completed.

## Context and files

The accepted r46 debug/fix contract changes are in `nckh-kit/skills/engineer/`,
`core/registry/catalog/route-boundaries.json`, the regression case/test and owning
engineer documentation. The canonical lock and packages initially identify r45.
The accepted review has no open actionable source findings and retains the
scoped owner waiver for missing historical process metadata.

## Steps and validation

1. Match accepted source hashes and inspect owned installation state.
2. Record current publication authority and experimental limits in owning docs.
3. Use the existing freeze entrypoint; retain the previous lock in history.
4. Run the affected regression modules and build each host twice for reproducibility.
5. Build into a new local staging directory, verify it, promote matching packages,
   then run the public package verifier.

## Risk and rollback

Preserve reviewed instruction bytes and resource rights. Existing packages remain
available until staging passes. If build/verification fails, retain the failure
receipt and stop promotion; do not repair skill code without separate authority.

## Observed result

Revision 46 pins 430 source files. All six accepted contract files match the
independent review. The first affected-suite attempt failed because its temporary
root inherited visible installed skills; the isolated retry passed all 52 tests.
All four builds are reproducible and the promoted public packages pass their
verifier. Raw command/process records remain local; the curated evidence retains
the failed attempt and the successful retry separately.
