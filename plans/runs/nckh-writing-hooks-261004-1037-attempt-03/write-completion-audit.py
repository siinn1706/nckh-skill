import re
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
PROJECT = RUN.parents[2]
PLAN = PROJECT / "plans/261004-0047-nckh-research-data-hooks-writing"
REPORTS = PROJECT / "plans/reports"
evidence = {
    1: [
        ("nckh-kit/core/registry/catalog/skills.json", "nckh-kit/tests/release/test_writer_matrix.py"),
        ("nckh-kit/core/evaluation.py", "plans/reports/checks-261004-1037-starting-baseline.json"),
        ("nckh-kit/skills/core/nckh-humanwrite/SKILL.md", "plans/reports/reviewer-261004-1037-writer-forward-test.md"),
        ("nckh-kit/skills/core/nckh-paperwrite/SKILL.md", "plans/reports/reviewer-261004-1037-writer-forward-test.md"),
        ("nckh-kit/skills/core/nckh-write/SKILL.md", "nckh-kit/core/guards.py"),
        ("nckh-kit/core/profiles/style/writer-language.md", "nckh-kit/tests/release/test_writer_matrix.py"),
        ("plans/reports/checks-261004-1037-starting-baseline.json", "plans/reports/artifacts-261004-1037/source-r26.zip"),
        ("nckh-kit/skills/core/nckh-humanwrite/references/humanizer-adaptation.md", "nckh-kit/tests/resource/test_writer_consumers.py"),
        ("nckh-kit/core/registry/catalog/resources.json", "nckh-kit/tests/resource/test_writer_consumers.py"),
        ("nckh-kit/core/profiles/style/vi.md", "nckh-kit/skills/core/nckh-humanwrite/references/humanizer-adaptation.md"),
        ("nckh-kit/core/guards.py", "nckh-kit/core/profiles/style/writer-language.md"),
        ("nckh-kit/core/profiles/style/writer-resources.md", "nckh-kit/skills/core/nckh-paperwrite/SKILL.md"),
        ("nckh-kit/evals/cases/research-writing-visuals/nckh-humanwrite.json", "nckh-kit/evals/cases/runtime/writer-invocation-matrix.json")],
    2: [
        ("nckh-kit/core/guards.py", "nckh-kit/tests/evidence/test_visual_purpose.py"),
        ("nckh-kit/core/guards.py", "nckh-kit/skills/core/nckh-visuals/SKILL.md"),
        ("nckh-kit/core/contracts/brief.schema.json", "nckh-kit/tests/evidence/test_visual_purpose.py"),
        ("nckh-kit/skills/marketing/nckh-brand/SKILL.md", "nckh-kit/skills/engineer/nckh-frontend/SKILL.md"),
        ("nckh-kit/core/contracts/brief.schema.json", "nckh-kit/core/guards.py"),
        ("nckh-kit/tests/evidence/test_visual_purpose.py", "nckh-kit/core/guards.py"),
        ("nckh-kit/skills/core/nckh-visuals/references/scientific-visual-qa.md", "plans/reports/researcher-261004-1037-hook-schemas-visual-source.md"),
        ("nckh-kit/evals/cases/research-writing-visuals/nckh-visuals.json", "nckh-kit/tests/evidence/test_visual_purpose.py"),
        ("nckh-kit/core/guards.py", "nckh-kit/docs/research-and-writing.md")],
    3: [
        ("nckh-kit/core/hook_config.py", "nckh-kit/hooks/templates/codex.json"),
        ("nckh-kit/core/hook_policy.py", "nckh-kit/tests/hooks/test_policy.py"),
        ("nckh-kit/hooks/runner.py", "nckh-kit/tests/hooks/test_runner.py"),
        ("nckh-kit/hooks/runner.py", "nckh-kit/tests/hooks/test_runner.py"),
        ("nckh-kit/hooks/runner.py", "nckh-kit/scripts/configure-hooks.py"),
        ("nckh-kit/core/contracts/hook-event.schema.json", "nckh-kit/core/contracts/hook-decision.schema.json"),
        ("nckh-kit/core/hook_policy.py", "nckh-kit/scripts/hook-preflight.py"),
        ("nckh-kit/hooks/codecs/codex.py", "nckh-kit/tests/runtime/test_hook_adapters.py"),
        ("nckh-kit/core/build.py", "nckh-kit/tests/hooks/test_closure.py"),
        ("nckh-kit/core/hook_config.py", "nckh-kit/tests/hooks/test_config.py"),
        ("nckh-kit/core/registry/compatibility/matrix.json", "nckh-kit/docs/runtime-support.md")],
    4: [
        ("nckh-kit/core/registry/catalog/skills.json", "nckh-kit/core/evaluation.py"),
        ("plans/reports/checks-261004-1037-starting-baseline.json", "nckh-kit/core/registry/source-lock/source-lock.json"),
        ("nckh-kit/core/build.py", "plans/runs/" + RUN.name + "/smoke-summary.json"),
        ("nckh-kit/docs/personal-use.md", "nckh-kit/core/profiles/acceptance/personal-use.json"),
        ("plans/reports/checks-261004-1037-starting-baseline.json", "plans/runs/" + RUN.name + "/final-preservation.json"),
        ("nckh-kit/core/evaluation.py", "nckh-kit/core/acceptance.py"),
        ("nckh-kit/core/registry/source-lock/source-lock.json", "plans/reports/review-261004-1037-r29-source.md"),
        ("plans/runs/" + RUN.name + "/archive-summary.json", "plans/runs/" + RUN.name + "/smoke-summary.json"),
        ("nckh-kit/core/evaluation.py", "nckh-kit/tests/release/test_writer_matrix.py"),
        ("plans/runs/" + RUN.name + "/deterministic.json", "plans/runs/" + RUN.name + "/installer-previews.json"),
        ("nckh-kit/tests/installer/test_transactions.py", "nckh-kit/tests/hooks/test_config.py"),
        ("nckh-kit/docs/personal-use.md", "nckh-kit/core/profiles/acceptance/personal-use.json")]
}
rows, pending = [], []
for phase, path in enumerate(sorted(PLAN.glob("phase-*.md")), 1):
    items = re.findall(r"^- \[([ x])\] (.+)$", path.read_text(encoding="utf8"), re.M)
    assert len(items) == len(evidence[phase])
    for number, ((flag, item), references) in enumerate(zip(items, evidence[phase]), 1):
        for reference in references:
            assert (PROJECT / reference).exists(), reference
        links = "; ".join(f"[{Path(reference).name}](../../{reference})" for reference in references)
        state = "LOCAL CHECKPOINT COMPLETE" if flag == "x" else "INCOMPLETE — required user/native evidence"
        escaped = item.replace("|", "&#124;")
        rows.append(f"| P{phase}.{number} | {escaped} | {state} | {links} |")
        if flag != "x":
            pending.append(f"- P{phase}.{number}: {item}")
assert len(rows) == 45 and len(pending) == 3
audit = REPORTS / "audit-261004-1037-r29-completion.md"
if audit.exists():
    raise RuntimeError("Preserve existing completion audit")
audit.write_text("""# NCKH r29 — completion audit

Status: **FULL GOAL NOT ACHIEVED**. Local implementation/package checkpoint complete; three native/owner requirements remain incomplete.

Audit against the current accepted plan, not a reduced scope. Source revision r29, 281 pins,
canonical hash `6fbdf13a4ba296b3e492b89beaf7fc8299c926d73a02a0ffcd9ea16a88d16248`.
This controller audit reads the source/test owners and reconciles actual process/result/archive/read/preview/preservation receipts.
It is not an independent reviewer or a new scientific/human/native acceptance event.

## Authoritative run evidence

- [Full deterministic](../runs/""" + RUN.name + """/deterministic.json): 181 discovered, 180 passed, 1 Windows real-symlink skip; 806.511 seconds. It discovers the named tests in the table; synthetic fixtures test code behavior, not human gold/native prevention.
- [Delivery](delivery-261004-1037-r29-local-candidate.md) / [structured chains](delivery-261004-1037-r29-local-candidate.json): four reproducibility variants, sixteen persistent archives/extracted bundles, 216 resource reads, 48 disabled/no-read checks, 24 hook projections, eight installation previews, 509 unchanged protected hashes and four legacy schema-v1 bundles readable.
- [Finalization verification](../runs/""" + RUN.name + """/finalization-verification.json): 9 Markdown files, 80 local links and 1 anchor; 42/45 actual checkboxes; 154 completed owned commands with exit/cleanup receipts. These are state/integrity checks, not acceptance quality evidence.
- [Independent local writer trial](reviewer-261004-1037-writer-forward-test.md), [source/schema comparison](researcher-261004-1037-hook-schemas-visual-source.md), [r29 delta review](review-261004-1037-r29-source.md). No native/human label is borrowed from these records.

## Forty-five explicit checkbox requirements

The COMPLETE label below is limited to the local technical work authorized and observed. Conditional install/trust/native grants mentioned within a checked mechanical task remain conditions, not claims that activation happened. The uncovered native task stays unchecked. No acceptance criterion was removed to raise the completion count.

| Item in phase order | Requirement from current phase | Audit result | Source/test/record owners read |
|---|---|---|---|
""" + "\n".join(rows) + """

## Additional named artifacts, commands and gates

- Exact baseline identity union and case IDs verified by starting snapshot, source capture and current validation. The historical 148 IDs/224 cells/comparator/receipts are preserved; changed visual prompt bytes invalidate old grading for the new input.
- Writer matrix/schema/validator are named artifacts, present and integrated automatically: 256 planned native cells / 20 scenarios; all remain unobserved/not-callable/not-run as declared. VI/EN style/output and source-resource locale are distinct. Four local trials do not cover the full native matrix.
- Humanizer linked/re-authored Markdown contains contextual rules, counterexamples, protected fields and path/hash/license; not a tenth resource pack. Selected K-Dense guidance/source ledger was adapted; restricted ClaudeKit/document source was not imported. LanguageTool stays deferred/optional English diagnostic; no Java/service/server installation is claimed.
- Scientific visual QA/purpose guard, closed brief fields, actual World Bank locator/blank-unit and executed transform calculation are implemented. Hash/declared slot/source-to-mark checks do not authenticate a fabricated but consistent receipt or certify scientific meaning. Research logos/ads/banners/thumbnails/generic art remain prohibited; no additional simulation pipeline was added.
- Runner, four codecs, inactive templates, manual checker, hook schemas, exact closure and config lifecycle/recovery owners exist. Config tests cover changed preview, invalid/duplicate JSON, user/shared edits, concurrent/partial failure and interrupted recovery. Native responses/failure behavior and preventive side effects are not established by codec fixtures.
- All named build/validate/resource-smoke/preview commands have actual receipts in the current attempt; archive/extract paths, source/closure/archive bindings are resolved, not placeholders. Legacy v1/v2 handling remains compatible; current source requires its exact hook inventory. Resource-access ON is the public package contract; OFF artifacts are internal comparison only.
- Installation docs and the six affected owning documentation surfaces were updated before r29 freeze. Plan files retain historical adjudication links and reconciled evidence. Native activation/trust, installation update, stable/scientific/rights/reviewer/holdout/economics acceptance remain gates; no external publication occurred. Conditional Git simplifier is unavailable without a Git live diff; no fake signal or simplifier result is claimed.

## Incomplete requirements and next authority

""" + "\n".join(pending) + """

`ak-cook --auto` preserves the explicit P3/P4 grants; it does not grant install/trust/native or owner approval. To proceed, the human must authorize the native qualification scope and supply personal-use feedback for actual reviewed artifacts bound to r29/input/output hashes. No elapsed time, generated report, automation continuation or controller judgment substitutes for those inputs.

The native goal stays active. This turn made progress through r29 packaging, integrity reconciliation and this audit; no blocked status is asserted on the first missing-input turn. Do not mark goal complete, close the plan or replace these incomplete requirements with local test evidence.
""", encoding="utf8")
print(str(audit))
