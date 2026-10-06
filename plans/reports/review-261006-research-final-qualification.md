# P7 final qualification review - static checkpoint

Status: DONE

Summary: One concrete final-evidence source-binding defect was identified, reported and repaired by the controller. The revised reconciler closes that finding. No other concrete blocking defect was found in the bounded task-local extraction, installer-preview and complete-suite logic. Actual qualification receipts remain pending and will require the separately authorized final execution review.

## Scope and authorization

Live reference: controller delegation `/root/review_owned_provenance`, P7 task-local qualification review received 2026-10-06. Scope revision: inspect `qualify-extracted-packages.py`, `final-evidence.py`, `run-local-qualification-attempt-02.py`, active P7 plan and prior integration review while the controller's full suite runs. This report is the sole owned output. Project-local `--auto` is recorded; no `--yagni`. No source/build/test/process edits, suite execution, package build, freeze, provider/native/global installation, publication or nested delegation occurred.

Supporting read scope was limited to the existing `no_links`, `verify_bundle`, surface mapping and current inventory/lock metadata needed to resolve concrete contract questions. Existing reviewed source decisions were preserved. Requested/resolved/configured/applied model settings: inherited session; effective native model/effort, cost and usable-window telemetry: unknown. The reviewer role does not establish human or model independence.

Controller freeze reference: r41/337, canonical hash `114e57918889a52474b514c09443a2afd1999e2dd11990a099d5b8069a9267d5`. Read-only metadata independently observes revision 41, 337 file entries, and lock-file SHA-256 `4e86e15b74106a741c51b59072245661c0df9ee99bbda192f601ac9d2d1604f2`. No source-lock verification was executed by this reviewer.

## Finding and corrective inspection

The initially inspected `final-evidence.py` accepted a passing deterministic receipt/output without reconciling its recorded source hash to the current approved freeze. Its original lines 26-31 checked status, inventory flags, count arithmetic and output bytes, allowing a successful receipt from a different freeze to satisfy those conditions. That violates the P7 no-verdict-transplant requirement. Original reviewed SHA-256: `fdec7d7f97aca4c16c727bf033cd995507a649bf87d3a716d5debe77516834ba`.

The controller repaired the task-local reconciler. Direct re-inspection of revised lines 29-40 confirms:

- top-level deterministic receipt and process pre/post source hashes equal the current verified lock;
- every local-gate command's pre/post hashes equal that lock;
- the deterministic local-gate record, suite process record and actual command receipt are exactly equal;
- actual argv, exit zero, output name and output hash match the suite;
- complete inventory/no-exclusion checks, pass/skip arithmetic and actual output-file hash remain required.

Disposition: CLOSED by source inspection. Revised SHA-256: `d2444c8c5af564e2c06af9bddc1dba0b61bb08aca4da56005e602830e94ad62d`. The revised script was not executed by this reviewer; its actual reconciliation result remains pending.

## Bounded mechanical gate assessment

| Gate | Inspected evidence and disposition |
| --- | --- |
| External containment and extraction | Unique owned host-temp root is checked through `no_links` and resolved outside WORK. Separate CWD is a sibling outside extracted trees. Archive members are relative and reject parent traversal; target/source tree hashes are compared. Existing `verify_bundle` traverses every node through `no_links` and rejects missing/unowned files. No concrete defect found. |
| Sixteen actual package paths | Producer explicitly iterates four modes by four hosts: ON standalone/plugin and internal OFF standalone/plugin. Each source and extracted bundle is verified; exact file hashes and manifest equality must survive archive/extraction and all reads. Final reconciliation re-verifies persistent source manifests against current lock and exact 43 identities. Actual results pending. |
| Package/no-bytecode preservation | Both relocated reader and checker invocations use `python -I`; package/source snapshots before and after must be identical. Plugin-projected readers are separately invoked and resource hashes compared. Previously reviewed CLI bytecode suppression remains the controlling source repair. No cleanup masks package changes. |
| Actual OFF absence/no-read | Existing unchanged verifier rejects OFF resource bindings and any copied-upstream or owned-reference content, while exact file ownership rejects extra resource files. The extracted OFF reader must actually exit zero with `resource-disabled` and `resource_read=false`. This resolves absence through the verifier and no-read through the real invocation; actual receipts pending. |
| Eight read-only explicit installer previews | Existing mapping has eight surfaces. Each command supplies extracted `--package`, disposable project/home, three kits, copy mode, balanced model profile and `--dry-run`; exit zero and `status=preview` are required. Package/project file hashes must remain identical, including pre-existing `user.txt`. No real installation is invoked. |
| Legacy format 1/2 | Three preserved bundles are verified and compared before/after; observed format set must equal `{1, 2}`. No legacy mutation is performed. |
| Full 311/no exclusions/skip accounting | Current inventory contains 311 entries. Actual command is complete verbose unittest discovery with no case/module exclusions. Wrapper compares ordered observed IDs and summary count to inventory, stores each result and skip reason, hashes output/inventory, and records owned process identity and pre/post lock hashes. No arbitrary timeout is imposed. Final reconciler requires passed + skipped = tests. |
| Failure retention and cleanup | Attempt outputs/receipts use exclusive creation. Nonzero exits/source drift stop descendants; extraction errors retain owned temp evidence. Exact unchanged owned external temp snapshot is saved before bounded cleanup. Original pinned failure, deterministic timeout and Core-count diagnostic are separately bound into candidate history; original failures are not overwritten. |
| Scoped delivery | Experimental/local-package-only status and explicit scientific/native/owner/provider/stable/public/real-install pending states remain. Static route declarations, pilot claims and native acceptance are not inferred from these mechanical gates. |

At the 2026-10-06T04:17:13.481330+00:00 metadata checkpoint, `p7-local-gates.json`, `p7-deterministic-attempt-02.json`, `p7-extracted-qualification.json` and `experimental-candidate.json` did not yet exist. This report does not assign an execution pass to them.

## Reviewed fingerprints

Relative to the workspace:

```text
plans/runs/nckh-upgrade-261006-0850-attempt-01/qualify-extracted-packages.py
  44a43a5d13abd2434435e604445cce0f7cd6b57e24174fb72562823a85a8dfdc
plans/runs/nckh-upgrade-261006-0850-attempt-01/final-evidence.py (repaired)
  d2444c8c5af564e2c06af9bddc1dba0b61bb08aca4da56005e602830e94ad62d
plans/runs/nckh-upgrade-261006-0850-attempt-01/run-local-qualification-attempt-02.py
  cd8d5f94db021d4720182a61414d14587e8f7fc50ab066ba75e71de8d89198d0
plans/runs/nckh-upgrade-261006-0850-attempt-01/p7-test-inventory.json
  a8c20476cd2835233790ca7d54af88861f92f544fd9852112a1361faa3bf56e4
plans/261005-0036-nckh-devops-aiops-research-upgrade/phase-07-integration-and-qualification.md
  0dc43dc3d1bed5bc5087efa3c4e82400254c89f4a039a6ef310ef35323c82cff
plans/reports/review-261006-research-integration-p7.md
  83ec82c3dbe6264bf1e38283793a61b3c3803507bc4a5ad0561ea0ebe1a96297
nckh-kit/core/build.py
  bd8046619803d14060d8e9f87bc95c0d5dad408c4dfbc4203e8d468b4754a168
nckh-kit/core/paths.py
  403750482c2bcf4df1a794fe91fd85c85e6c160194378a447838ca112c76032b
nckh-kit/core/install.py
  7aeae862234362235f4b21f89679f9ff82a3bfbe23dec9984005b68e3db8e7b2
```

[Active P7 plan](../261005-0036-nckh-devops-aiops-research-upgrade/phase-07-integration-and-qualification.md) and [preserved integration/repair review](review-261006-research-integration-p7.md) retain their existing authority and chronology.

Concerns/Blockers: none outstanding in this bounded static review. Actual full-suite, extraction/preview/cleanup and final-delivery receipts remain pending. Final execution review awaits the controller's authorized follow-up when those artifacts exist.

Recorded at: 2026-10-06T04:18:44.477548+00:00 / Asia/Saigon 2026-10-06T11:18:44.477548+07:00.

## Final actual qualification and delivery review - 2026-10-06

Status: DONE

Summary: The completed r41 receipts, actual verbose test output, package/read/checker/preview records, preserved snapshots and delivery claims agree. No concrete blocking finding remains. The earlier source-binding finding is closed by the repaired reconciler and matching actual receipt/process/command evidence. The authorized local mechanical delivery scope is complete; scientific, owner, semantic/full-native, paid-provider, stable/public and real-install acceptance retain their explicit separate states.

### Scope amendment and evidence method

Live authorization reference: controller's final bounded actual qualification delegation to `/root/review_owned_provenance`, followed by the process/link receipt update on 2026-10-06. Scope revision: read actual P7 receipts and append only to this report. `--auto`, no `--yagni`. Reused unchanged source/static verdicts. No full-suite rerun, new build, provider/native run, process action, source/test/plan edit, publication or nested delegation occurred. These are inspected controller execution receipts plus independent read-only hash/record reconciliation; no reviewer execution of the product gates is claimed.

Read the complete actual 311-case output and compared ordered IDs/results against both the receipt and the actual inventory. Reconciled all nine per-command records, current freeze, candidate bindings, sixteen package manifests and recorded extraction snapshots. Read every ON/plugin/OFF/checker/preview observation; directly rehashed all protected files and ownership. Inspected cleanup/process evidence and the current delivery/final-reconciler text after the controller's duration/readability changes. The earlier pending-execution statements remain historical checkpoints; the results below supersede them for the local mechanical gates.

### Derived qualification results

| Required gate | Actual reconciled result |
| --- | --- |
| Frozen source | r41, 337 pins. Canonical SHA-256 `114e57918889a52474b514c09443a2afd1999e2dd11990a099d5b8069a9267d5`; lock-file SHA-256 `4e86e15b74106a741c51b59072245661c0df9ee99bbda192f601ac9d2d1604f2`. Current lock, approval, candidate, local gates and deterministic receipt agree. |
| Exact identities/cases/resources | Actual catalog has 43 unique identities; current validated case receipt records 172 base cases and 19 required families. Actual resource registry has thirteen groups and 35 consumer bindings. Preserved exact-set source verdict remains bound to r41. |
| Complete deterministic suite | 311 unique ordered IDs exactly match inventory and actual verbose output; 310 `ok`, one skip, zero failures/errors, exit zero, 914.791 seconds. Actual discovery argv includes `-B -m unittest discover -s tests -t . -p test_*.py -v`; no exclusions or arbitrary 900-second cutoff. |
| Sole skip | `tests.evidence.test_visual_engine_binding.VisualEngineBindingTests.test_symlink_observation_is_rejected`: Windows denied creation of the real symlink fixture with WinError 1314. The actual reason is preserved in output, receipt and candidate; this specific fixture was not exercised on this host. |
| Nine command descendants | Exact expected nine names, each exit zero, reaped owned handle, matching current pre/post source hashes, matching actual output SHA-256 and identical separately saved command receipt. Deterministic gate record equals suite process record and actual command receipt; argv/exit/output bindings agree. |
| Two-build reproducibility | Actual standalone and plugin `--check` outputs each cover all four hosts with `reproducible=true`; their closure hashes match the corresponding persistent ON bundles. Native qualification stays unverified. |
| Sixteen packages | Exact four modes by four hosts. All candidate manifest bindings, closure/source hashes and 43-identity sets match. Recorded final extracted file maps equal manifest file maps exactly, archive hashes match retained pre-cleanup snapshot, and no bytecode files occur. No pilot/private evaluation paths enter the inspected manifests. |
| Actual reads and checkers | Four ON standalone packages yield 140 bound reads; four ON plugin packages yield 280 (standalone plus projected readers), total 420. All 35 bindings per invocation match resource and reader hashes, isolated/outside-CWD flags and zero exits. Eight isolated checker observations match actual saved outputs, contract pass, read-only and `commands_executed=false`; scientific acceptance remains pending. |
| OFF treatment | Eight actual OFF reader invocations exit zero with `resource-disabled`, no read and empty records. Their manifests have no resource bindings and no copied-upstream/owned-reference content. Internal OFF remains separate from the eight ON delivery bundles. |
| Eight installer previews | All eight expected surfaces use the correct explicit extracted package, project scope, core/engineer/marketing kits, copy mode, balanced profile and dry-run. Exit/status and exact source/project pre/post hashes agree; original Windows CRLF user-file bytes are preserved. No real installation acceptance is inferred. |
| Legacy preservation | Three original bundle manifest hashes match recorded rows; formats are 1, 2, 2, all verified/pass and unchanged in actual extraction qualification. |
| Protected bytes | Independently rehashed 46 protected source files + 506 installed files + 37 historical lock files + one ownership file = exactly 590; zero mismatches. Candidate and preservation receipt agree. |
| Owned cleanup | Qualification root is the exact recorded external host-temp root owned by RUN; 20,528 final snapshot files retained before removal, with no CWD files. Its recorded archive/extracted/package hashes reconcile. Both exact timeout roots retain their 320-file/zero-file snapshots and ownership mapping. All three roots are absent. |
| Process/link closeout | Actual process reconciliation records nine command receipts, completed supervisor/final-reconciler sessions with exit zero, no observed tracked PID, owned_live zero and no unrelated process stopped. Pre-closure link receipt contains 57 checked links and zero missing; every recorded target currently exists. |

### Historical failures and scope disposition

The candidate's three retained failure bindings match actual bytes. Original r39 receipt remains 78 tests in 225.417 seconds with two failures and two errors. Original r40 public-runner receipt remains `timeout-unknown`, explicitly timed out after 900 seconds, with no complete inner-suite exit status; its source hash matches the preserved r40 freeze. The separate focused Core diagnostic remains one test in 52.021 seconds failing with `16 != 12`. None of those failed/unknown results was rewritten into a pass or transplanted into r41.

The current [delivery report](delivery-261006-research-upgrade-r41.md) truthfully presents the derived local results and the sole skip. The [experimental candidate](../runs/nckh-upgrade-261006-0850-attempt-01/experimental-candidate.json) remains `experimental-delivered`, `local-package-only`. Its semantic routes are unverified; scientific/owner/full-native acceptance remains pending; provider-paid, stable/public and real install/migration are not authorized. The quick genuine Codex callback is still described as the bounded pre-upgrade check; old full-native plan 44/45 remains separate. The delivery retains retrospective/dependent single-country pilot limits and makes no new scientific/causal/generalization/blind efficacy claim. This qualification review does not re-evaluate those scientific or native lanes.

All five candidate evidence bindings, four prior-review bindings and three historical-failure bindings match their current artifacts. The repaired final-evidence source binding remains present in the current task-local script; its subsequent duration field/wording addition does not alter the reviewed package source. No concrete discrepancy was found between inspected receipts and delivery claims.

### Final fingerprints

The following SHA-256 values bind the exact inspected RUN artifacts; canonical-record and file hashes are kept distinct above:

```text
experimental-candidate.json
  526999b48853121b071cbcf674b8ce7fc6d39678791ea2cd15ef43d87faabab8
p7-local-gates.json
  9efc16a8efb0c16d6f01903d7b5e319bde6635a52cf9dfc18a7a90d28e772dde
p7-deterministic-attempt-02.json
  53822004e28228451f4ed11fc66d5514d7ca7fa1abf1581ee765439c328854d8
p7-deterministic-attempt-02.txt
  e93e1285acc39786d63b5b31a5d6c81499327c0234e839e4abf771469a74949b
p7-extracted-qualification.json
  6eb3ea5b285639e6f0739abee48a0c2a56a48d0bb76b808470fd22083b91f685
p7-final-preservation.json
  f6cd73f5da70a2c17af9651429f423a627da012531814e575bc7bae71c2824d2
p7-temp-cleanup.json
  08193615384d6b25b30db1d99957f3819bbff46b92ee3b4a288d2d7cee308d7b
p7-temp-before-cleanup.json
  ed659fa83d2185fa294feefb4a32baa75fea3a9da13aa296047bdfdea115395f
p7-timeout-temp-cleanup.json
  458fb1ff59da91b15577132515279bee8e08f6bd59dca7feff859ce98e08fccc
p7-approved-freeze-attempt-03.json
  8d84699f86677de3193a286020adab6ea3c69d6e09610bdb4a7e1cb1972010bd
final-evidence.py
  133634f49811a6fddee5b8e99a3879791793a26e63f3dd61ac79180618bbebdc
p7-final-process-reconciliation.json
  cfc5cfe95dba766bbda510f54dcee0e0b77283f84955c04f1c174ac3f300231a
p7-handoff-links-before-closure.json
  19daa4f1e26a4099ffa12342c646b1a95d3ac4d2aa6c06ed842660e6577db512
p7-pinned-tests-attempt-01.txt
  2d6fa00875903bee325bb1a68d1b8f0963168d2fad01ed1760bb851e5803c174
p7-deterministic.json
  f30c9f171f2c11af23dcc05b46da943543691d7e1356ba1b252097af3aa776f4
p7-core-count-diagnostic-attempt-01.txt
  0f9e6eb1b9f50fdc58006dc9771aab8f12feedfec7e3ce0fa56c4c7984abd221
delivery-261006-research-upgrade-r41.md (reports/)
  d0a81e1f61b76c1e152a8bf317023d0aecd8f14507a3b99eb4e867aaca71fbed
```

Concerns/Blockers: none within the authorized local qualification/delivery scope. The Windows symlink skip is explicitly retained; separate scientific/owner/semantic/full-native/provider/stable/public/real-install gates retain their actual pending or not-authorized states. No further local mechanical work is required by this review.

Recorded at: 2026-10-06T05:10:23.309936+00:00 / Asia/Saigon 2026-10-06T12:10:23.309936+07:00.
