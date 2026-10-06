---
title: NCKH r34 native delivery checkpoint
date: 2026-10-05
summary: R34 local delivery pass; AGY event faults recorded; full native surface gate remains open
---

# NCKH r34 native delivery checkpoint

## What happened
Candidate r34 completed the local delivery checks: 187 deterministic tests with one Windows symlink skip; four reproducibility variants and 16 archives/extractions; 216 resource reads, 48 OFF writer no-read observations, 24 hook projections; eight installer previews and 509 protected hashes unchanged.

## Repairs and actual observations
AGY native TargetFile/AbsolutePath inputs exposed a real protected-path bypass before r33. The marker and failure receipts remain. R33 full suite then exposed a Windows Path.resolve prefix race when the receipt parent appeared concurrently. R34 creates the contained directory before resolving the child; 150 fresh directories with six concurrent calls and the full suite passed without weakening guards.

R34 AGY native file allow/denial and workspace-plugin duplicate cases passed. Twenty-five genuine callback fault attempts across five selected events were recorded. Five PreToolUse faults produced native tool ERROR before a marker. Four PostToolUse faults produced ERROR after marker creation; the interpretation collector initially assumed every other tool state was DONE, failed, and was corrected against raw native streams with its preimage retained. Invocation callbacks wrap each model invocation and occur both before and after a tool.

Cursor Grok 4.7 500K Extra High allow created a marker. Project plus transient plugin duplicate produced two same-tool callbacks and one policy receipt, but the host reported a 20-second hook timeout even though both packaged runners exited 0. This remains unverified.

## Decisions and remaining work
Use exact revision/event/version/surface bindings. Preserve historical failures; do not regrade r31 native runs as r34 after runner changes. Current r34 removed 82 matching test files (164 total with r31/r33), native global configuration hashes were unchanged, and the process audit had no matching task processes.

Plan remains in-progress, 44/45. Owner VI/EN acceptance binds the two displayed r29 samples. Installed r25 was not updated. Claude model/tool, additional Codex routes, Cursor events/timeouts, direct Desktop/IDE evidence, production timing and stable/scientific/release gates remain open. AgentWiki publish skipped.

> Historical work record — not durable authority. Prefer docs/specs/ADRs for current decisions.

## Continuation — native events and patch-path repair

Codex r34 CLI exec recorded 25 faults across five events; explicit pretool deny blocked the marker while several hook failures let the tool continue. Cursor recorded 20 later turns, including 15 faults across three actual events and two successful project/plugin duplicates. Its earlier 20-second duplicate timeout remains retained, with root cause unresolved. CLI prompt/stop callbacks were absent.

Four further Codex native apply_patch turns exposed a private-path bypass: native tool_input.command carried exact patch text, but r34 decoded no paths. The synthetic private marker and failure receipts remain. Three regressions produced 22 failures before repair. R35 reads bounded canonical file/move headers and both aliases; 12 focused codec/policy tests passed. The current full delivery pipeline is separate and running; r34 observations do not certify r35.

The dangerous CLI also persisted its own project trust. Removing only that key in memory reproduced the baseline parsed hash; the controller did not edit the global store. Cleanup removed 26 matching payload members then consumed CPU without a final receipt. The exact owned PID/time/command were verified, graceful stop failed, force stop succeeded, and a separate filesystem/process reconciliation verified absent payload and zero native test processes. The helper stall cause remains unresolved; no invented completion receipt was written. Native trust is retained. AgentWiki publish skipped.
