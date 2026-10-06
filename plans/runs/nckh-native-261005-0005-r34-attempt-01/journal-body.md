## What happened
Candidate r34 completed the local delivery checks: 187 deterministic tests with one Windows symlink skip; four reproducibility variants and 16 archives/extractions; 216 resource reads, 48 OFF writer no-read observations, 24 hook projections; eight installer previews and 509 protected hashes unchanged.

## Repairs and actual observations
AGY native TargetFile/AbsolutePath inputs exposed a real protected-path bypass before r33. The marker and failure receipts remain. R33 full suite then exposed a Windows Path.resolve prefix race when the receipt parent appeared concurrently. R34 creates the contained directory before resolving the child; 150 fresh directories with six concurrent calls and the full suite passed without weakening guards.

R34 AGY native file allow/denial and workspace-plugin duplicate cases passed. Twenty-five genuine callback fault attempts across five selected events were recorded. Five PreToolUse faults produced native tool ERROR before a marker. Four PostToolUse faults produced ERROR after marker creation; the interpretation collector initially assumed every other tool state was DONE, failed, and was corrected against raw native streams with its preimage retained. Invocation callbacks wrap each model invocation and occur both before and after a tool.

Cursor Grok 4.7 500K Extra High allow created a marker. Project plus transient plugin duplicate produced two same-tool callbacks and one policy receipt, but the host reported a 20-second hook timeout even though both packaged runners exited 0. This remains unverified.

## Decisions and remaining work
Use exact revision/event/version/surface bindings. Preserve historical failures; do not regrade r31 native runs as r34 after runner changes. Current r34 removed 82 matching test files (164 total with r31/r33), native global configuration hashes were unchanged, and the process audit had no matching task processes.

Plan remains in-progress, 44/45. Owner VI/EN acceptance binds the two displayed r29 samples. Installed r25 was not updated. Claude model/tool, additional Codex routes, Cursor events/timeouts, direct Desktop/IDE evidence, production timing and stable/scientific/release gates remain open. AgentWiki publish skipped.
