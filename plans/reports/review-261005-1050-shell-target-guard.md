# Shell target guard review

## Kết quả

Reviewed changes are limited to `core/hook_policy.py`, `tests/runtime/test_hook_adapters.py` and `docs/installation.md`. Actual r35 native Bash receipt had command-only input, `allow`, completed native execution and a created private synthetic marker; [failure bindings](./delivery-261005-1042-r35-shell-target-failure.json) establish the cause.

The repair returns pending for mapped shell tools whose full target coverage is unverifiable. An ordinary path alias cannot establish coverage of a command, so it cannot bypass the guard. Existing protected-path checks, plan-only mutation checks and missing-grant checks retain precedence. Unmapped routes remain explicitly manual/unverified; direct canonical patch routes retain their path checks. No shell parsing, execution, network/model call or raw command receipt ingestion was added.

Before repair, the new bounded regression produced21 subcase failures; after repair,20 focused tests passed, including existing policy, runner and host codec checks. Tests exercise four codec wire shapes, safe aliases that cannot conceal command targets, unchanged plan-only reasons and unmapped manual behavior. These are deterministic fixtures; they do not claim live preventive evidence for four hosts.

No additional blocking finding in the inspected diff. Review was inline using `ak-code-review`; no independent reviewer was run. Native retest and complete integration/build validation are pending for the next frozen candidate. R35 failure evidence remains historical, and installed r25 / owner r29 samples / scientific or release acceptance remain separate.
