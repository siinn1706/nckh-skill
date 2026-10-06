# AGY CLI: read-only agent inventory chưa xác định effective toolset

[Verified bindings](./delivery-261005-2310-r37-agy-agent-inventory.json) ghi hai CLI commands: help agents và agents inventory, đều exit0; **zero model prompts, zero agent/profile changes, zero controller config changes**. Inventory có16 names: Explore, advisor, brainstormer, code-reviewer, code-simplifier, debugger, docs-manager, fullstack-developer, git-manager, journal-writer, kongming, planner, project-manager, researcher, tester, ui-ux-designer. Không spawn/invoke các agents này.

Help stdout trống; names-only inventory không chỉ active agent hoặc effective callable tools. Chênh lệch [init/list_dir model statement32](./delivery-261005-2255-r37-agy-read-tool-refusal.md) vẫn unresolved; không suy availability từ names. [Multi-replace31](./delivery-261005-2240-r37-agy-tool-controls.md) có actual native unknown-tool ERROR và giữ status not-callable trên observed CLI/version.

Exact Win32 process capture và union audit226 observed identities: zero matching/tracked-live, no taskkill. Native command outputs/logs/creation identities giữ local; source/install/publication không đổi. Full native task unchecked/44 of45/P3 active. Current route vẫn CLI dangerous theo owner; không chờ IDE bring-to-front.
