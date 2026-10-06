# NCKH r41 installation

Updated the active project installation, default packages and global skills to the
latest GitHub main observed on 2026-10-06 (Asia/Saigon):
`bafa5ae744af77a3fa05662aa8a2dc2905c44680`, source-lock revision 41.

Each host package contains 43 skills, six optional agents and 13 resource groups
with resource access enabled. All three kits and the tooling skill were installed.

## Installed locations

| Scope and host | Skill root |
|---|---|
| Current project, Codex | `C:/Users/USER/Downloads/test-skill/.agents/skills` |
| Global Codex desktop, CLI and IDE | `C:/Users/USER/.agents/skills` |
| Global Claude Code | `C:/Users/USER/.claude/skills` |
| Global Cursor CLI and IDE | `C:/Users/USER/.cursor/skills` |
| Global Antigravity CLI | `C:/Users/USER/.gemini/antigravity-cli/skills` |
| Global Antigravity IDE | `C:/Users/USER/.gemini/config/skills` |

Native agents use the adapter's global agent roots: `.codex/agents`,
`.claude/agents`, `.cursor/agents` and `.gemini/config/agents` under the user home.
Model configuration inherits the host settings.

The project update used the official ownership-aware installer and registered
Codex advisory hooks. Global deployment used the
[targeted deployment utility](../../scripts/install-global-kits.py), which
checks exact adapter destinations, preserves unowned or edited files, stages
content and verifies installed hashes. Its ownership record is
`C:/Users/USER/Downloads/test-skill/.nckh-state/global-kit-deployment.json`;
it is separate from the official project installer's ownership index.
The recovered utility now reads packages from the workspace root and writes private run records under `.nckh-state/global-deployment-runs/`. Its syntax was checked after relocation; installation was not rerun.
Use this route for these global definitions on a future update; the official
installer's recursive visibility check also finds nested project definitions.
No global hooks were activated. Host discovery, trust and precedence were not
tested in fresh native sessions. Identical project/global skill content was
installed, without asserting native dedup qualification.

## Verification and recovery

- Package verification (historical evidence path: `2026-10-06-nckh-update/package-verification.stdout.txt`; unavailable in the cleaned checkout)
  passed for all four hosts at r41.
- Project update receipt (historical evidence path: `2026-10-06-nckh-update/project-install.json`; unavailable in the cleaned checkout) records a
  successful installation and committed advisory hook configuration.
- Project doctor (historical evidence path: `2026-10-06-nckh-update/project-doctor.json`; unavailable in the cleaned checkout) reports all 49 owned
  items current.
- Global receipt (historical evidence path: `2026-10-06-nckh-update/global-install-receipt.json`; unavailable in the cleaned checkout) records 239
  installed and hash-verified destinations: 215 skill trees and 24 native agents.
- Default package receipt (historical evidence path: `2026-10-06-nckh-update/default-package-receipt.json`; unavailable in the cleaned checkout)
  records r41 promotion and the retained old `dist` backup.

The first project attempt failed on a Windows directory rename and rolled back.
After the user confirmed applications were closed, directory access was checked
and the project update succeeded. First-attempt stdout/stderr were removed during repository cleanup.
The first global attempt detected a Windows newline mismatch in staged native
agent content and rolled back. The utility now writes the exact encoded bytes;
the successful attempt verified all destination hashes.
Global definitions were then restaged from unchanged owned bytes using normal
Windows directory inheritance so sandbox readers can access the installed files.
No ACLs were changed. The final global receipt covers the restaged installation.

No pending installation steps remain. Existing sessions may retain their old
skill catalog; use a new turn or restart the host to refresh discovery.
