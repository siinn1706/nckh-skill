# Full kit GitHub publication

Status: complete. Target: siinn1706/nckh-skill, main.

## Outcome

Publish the current r41 source and four self-contained packages with all registered resources, data, hook tooling, optional agents and plugin projections. Project installation retains advisory hooks by default.

## Phases

1. Verify source lock, repository identity and current remote revision.
2. Export pinned development source and build full resource-enabled packages.
3. Update public verification and documentation; verify source, data reads, hooks and credential hygiene.
4. Commit, push normally and verify remote commit identity.

## Acceptance

The public checkout rebuilds from its own source; all four packages contain the exact current catalog/resource inventory and source revision. Required data, provenance, notices and licenses are present. Secrets, private runtime receipts, installation state and raw upstream acquisitions stay outside publication. Preserve experimental/native/human/scientific qualification labels.

## Verified checks

- Full source export: 338 pinned members including current lock, revision 41.
- Four resource-enabled/plugin-projected packages: 43 skills, six agents, 13 resource groups, 35 bindings.
- Two independent builds produce identical four-host closure hashes. Public-source build matches those hashes.
- 110 focused research/resource/hook policy/configuration tests pass.
- 140 actual resource reads in isolated Python from outside the repository pass. Four advisory malformed-input checks pass.
- Public verifier, credentials/private-file/size scan and public docs links pass.
- git diff --check reports inherited blank lines at EOF in pinned source/package bytes; bytes preserved to retain r41 integrity.
- Commit: bafa5ae. Published to origin/main; remote SHA bafa5ae744af77a3fa05662aa8a2dc2905c44680 matches local HEAD; public checkout clean.
