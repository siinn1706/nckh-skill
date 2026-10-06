"""Update owned plan records only after the actual r35 delivery report exists."""

import json
import shutil
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PLAN = WORK / "plans/261004-0047-nckh-research-data-hooks-writing"
REPORT = WORK / "plans/reports/delivery-261005-0710-r35-patch-retest.json"
PREIMAGE = RUN / "plan-preimages-r35-delivery"
record = json.loads(REPORT.read_text(encoding="utf8"))
assert record["status"] == "local-delivery-and-native-patch-retest-recorded-full-native-gate-open"
assert len(record["native_patch_operations"]) == 8 and all(row["after_matches_expected"] for row in record["native_patch_operations"])
assert record["local_counts"] == {"tests": 190, "skipped": 1, "archives_extractions": 16,
    "resource_reads": 216, "writer_disabled_no_read": 48, "hook_projections": 24,
    "installer_previews": 8, "protected_hashes": 509}
if PREIMAGE.exists():
    raise RuntimeError("Preserve the earlier plan update")
targets = [PLAN / "plan.md", PLAN / "phase-03-portable-hooks.md", PLAN / "phase-04-integration-and-personal-acceptance.md",
    WORK / "plans/journals/2026-10-05-nckh-r34-native-delivery-checkpoint.md",
    WORK / "plans/reports/delivery-261005-0658-r34-codex-file-failure.md"]
text = {path: path.read_text(encoding="utf8") for path in targets}
PREIMAGE.mkdir()
for path in targets:
    shutil.copyfile(path, PREIMAGE / path.name)
index = targets[0]
updated = text[index].replace('R35 native patch-path repair; local revalidation running; native event/surface gate còn mở.',
    'R35 local delivery và native canonical patch repair verified; full native event/surface gate còn mở.')
updated = updated.replace('Candidate hiện **r35**, bounded native patch-path repair và local revalidation đang chạy; r34 là latest completed local delivery.',
    'Candidate hiện **r35**, local delivery và scoped native canonical patch repair đã có receipts; full native event/surface gate còn mở.')
updated = updated.replace('12/12 retained; completed r34 delivery; r35 revalidation running; owner samples accepted',
    '12/12 retained; r35 local delivery và scoped file retest completed; owner samples accepted')
updated = updated.replace('[R35 revalidation](../runs/nckh-native-261005-0710-r35-attempt-01/revalidation-summary.json) đang chạy; full/package/native r35 chưa được gọi PASS.',
    '[R35 delivery](../reports/delivery-261005-0710-r35-patch-retest.md) / [bindings](../reports/delivery-261005-0710-r35-patch-retest.json): 190 deterministic tests successful (một Windows symlink skip), 16 archives/extractions, 216 resource reads, 48 OFF observations, 24 hook projections, tám previews và 509 protected hashes. Four genuine Codex apply_patch turns xác nhận allow/plan-only-deny/protected-deny/manual; protected marker absent. Tám further native operations xác nhận update/delete/move allow và protected denial (source/destination/mixed patch). Canonical patch routes có scoped evidence; full native task vẫn unchecked.')
updated = updated.replace('R35 revalidation là process đang cần.',
    'R35 pipeline và native file processes đã terminal; final audit zero matching. New cleanup receipt giữ raw global config/hook hashes và historical project members; [helper review](../runs/nckh-native-261005-0658-r34-codex-file-attempt-01/cleanup-helper-review.json) sửa static receipt-target shadowing, chưa chứng minh nguyên nhân stall cũ.')
index.write_text(updated, encoding="utf8", newline="\n")
targets[1].write_text(text[targets[1]] + '\n## Current delivery — r35 native canonical patch retest\n\n[Delivery](../reports/delivery-261005-0710-r35-patch-retest.md) / [bindings](../reports/delivery-261005-0710-r35-patch-retest.json) bind four genuine Codex CLI 0.154.0 exec turns using GPT-5.6 Luna medium and verified extracted r35 payload. The existing native-trusted r34 file project was reused with a new evidence namespace. Callback command hashes matched each requested patch exactly. Allow/manual created markers; plan-only and private-path policy blocks had no completed file change and no marker. This verifies the repaired canonical add-file route; native update/delete/move, shell targets, plugin duplicates and other surfaces retain their own pending/manual status.\n\nCleanup removed 26 matching payload members, preserved historical project hashes and raw global config/hook hashes, added zero trust keys, and final process audit found zero matching task processes. [Static cleanup helper review](../runs/nckh-native-261005-0658-r34-codex-file-attempt-01/cleanup-helper-review.json) repairs receipt variable shadowing; no global overwrite was observed and the prior stall cause is not proven by its retained trace. Earlier native receipts remain unchanged. Full native checkbox remains unchecked.\n', encoding="utf8", newline="\n")
targets[2].write_text(text[targets[2]] + '\n## Current delivery — r35 local integration and native file retest\n\n[Delivery r35](../reports/delivery-261005-0710-r35-patch-retest.md) / [bindings](../reports/delivery-261005-0710-r35-patch-retest.json) confirm 190 deterministic tests successful with one Windows symlink skip; four reproducibility variants, 16 archives/extractions, 216 resource reads, 48 OFF writer no-read observations, 24 hook projections, eight installer previews, 509 protected hashes and four legacy bundles preserved. Source-lock r35/281 pins is unchanged. Four native Codex apply_patch turns confirm the repaired private add-file denial alongside allow/plan-only-deny/manual controls. Final cleanup/process audit completed. P4 remains 12/12; P3 full native event/version/surface task remains unchecked. Owner acceptance still binds only the two r29 VI/EN samples; installed r25 and scientific/stable/release gates are separate.\n', encoding="utf8", newline="\n")
targets[3].write_text(text[targets[3]] + '\n## Delivery — r35 local integration and canonical patch retest\n\nThe frozen r35 passed 190 deterministic tests with one Windows symlink skip, 16 archives/extractions, 216 resource reads, 48 writer disabled/no-read observations, 24 hook projections and eight installer previews. All 509 protected hashes and four legacy bundles were preserved. Four genuine Codex apply_patch turns reused the already trusted file scratch project and verified the repaired private add-file denial with no marker/file change, alongside allow, plan-only denial and uncovered/manual controls. Raw global config/hook bytes and historical project hashes remained unchanged; cleanup completed and final process audit found no matching task processes. The static cleanup target-shadowing defect was repaired with its source preimage retained, without claiming an execution trace for the earlier stall. Eight further genuine attempts verified public update/delete/move and protected source/destination/mixed-patch denial with actual before/after hashes. Shell/plugin/other surfaces remain pending. Plan is in-progress, 44/45. AgentWiki publish skipped.\n', encoding="utf8", newline="\n")
targets[4].write_text(text[targets[4]] + '\n## Subsequent evidence — reporting/helper correction and r35 retest\n\n[Cleanup helper review](../runs/nckh-native-261005-0658-r34-codex-file-attempt-01/cleanup-helper-review.json) found static receipt-target shadowing: the global-config inspection loop reused the receipt variable. The helper source preimage is retained and the target name/containment guard are repaired. The observed global file retains its hooks structure; no overwrite is observed, and the retained trace does not prove the earlier stall reached this call. The historical claim that the controller helper had no global writer must be read with this static correction. Native trust observation and cleanup reconciliation receipts remain unchanged.\n\n[R35 delivery/retest](./delivery-261005-0710-r35-patch-retest.md) records four genuine turns using the repaired packaged codec. The private add-file marker was absent and no file-change completed, while allow/manual controls produced markers. Historical r34 failure is retained; the later eight native operations verified public update/delete/move and protected source/destination/mixed-patch denial; full event/surface qualification remains pending.\n', encoding="utf8", newline="\n")
print(json.dumps({"status": "updated-r35-delivery-records", "native_checkbox": "unchecked", "plan_progress": "44/45"}))
