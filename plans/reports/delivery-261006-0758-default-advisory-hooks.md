# Default advisory hooks

User decision: project installation should activate hooks in advisory mode by default, without blocking tools or shell commands. Confirmed in this chat on 06/10/2026.

## Implemented scope

- Installer defaults to advisory hook configuration for project install/update, with `--hooks off` to skip configuration.
- Config transactions keep ownership, preimage checks, context/interpreter hashes, unowned entries and rollback.
- Advisory runner preserves policy decisions and degraded diagnostics in receipts, but emits no deny/prompt-block and exits zero for malformed input or missing context.
- Cursor advisory handlers use `failClosed=false`; enforcement still requires its native evidence and human grant.
- Global skill install requires `--hooks off`; project-specific hook configuration remains independent of skill uninstall.

## Evidence

- Final focused suite: 24 tests passed (`tests.hooks.test_runner`, `tests.hooks.test_config`, `tests.installer.test_entrypoints`). Includes actual isolated project installation and the off option.
- Additional policy/codec suite: 14 tests passed (`tests.hooks.test_policy`, `tests.runtime.test_hook_adapters`).
- Source revision 38: 281 pins, no source hash drift.
- Four full resource-on/plugin builds passed. These are static package checks, not native application qualification.
- An initial public advisory smoke attempt passed Claude/Codex but failed Cursor because promotion was still copying files and Cursor remained revision 37. This attempt was premature; final verification must wait for promotion completion and retain this failure record.

- Final public verifier passed all four r38 packages, each declaring `install_default: advisory`, resource access on, 39 skills, six agents and nine resource groups.
- Final isolated public runner smoke passed all four hosts after promotion completed. Malformed input produced no deny and exit zero; public installer imports/help passed.
- Staged publication scan passed: no credential patterns/private key files, maximum file size 609958 bytes, owning public documentation links valid.
- Local commit: `d449288970ada6c9749579ede4878f66485aeae4`, `feat(hooks): enable advisory checks by default on project install`.

Status: complete. Ordinary push succeeded; remote `main` equals `d449288970ada6c9749579ede4878f66485aeae4`, and the publication checkout is clean. Current user's project hook configuration has not been activated by these isolated tests; this delivery changes the default for subsequent confirmed project installation/update.
