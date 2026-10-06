# Default advisory hooks

Status: complete. User approved automatic activation during installation in advisory mode on 06/10/2026. Published commit `d449288970ada6c9749579ede4878f66485aeae4` is verified on remote main.

Outcome: project install/update registers owned advisory hooks by default, with an explicit off option. Advisory callbacks report actual policy diagnostics without denying tools, shell execution or prompts.

Constraints: preserve host permissions/trust, private state, unknown configuration, byte pins, rollback and enforcement evidence requirements. No native qualification claim or live project activation is implied by publishing a package.

Non-goals: change scientific policy, grant tool permissions, enable enforcement by default, or modify global host configuration.

Steps: implement runner/config/installer integration; test non-blocking output and owned config transactions; freeze and export packages; verify public packages; commit and push.

Acceptance: advisory faults return non-denying output, enforcement still requires native evidence, dry-run writes no host config, default confirmed project install produces hook config, off skips hook config, all four public packages pass integrity checks, remote commit matches local HEAD.

Verification: 24 runner/config/installer tests and 14 policy/codec tests passed. All four public r38 packages and isolated advisory fault outputs passed. Publication scan and public documentation links passed. See [delivery record](../reports/delivery-261006-0758-default-advisory-hooks.md). This changes the installation default; the existing live user project was not activated by the isolated tests.
