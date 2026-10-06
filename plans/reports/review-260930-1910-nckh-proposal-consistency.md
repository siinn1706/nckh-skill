# Review consistency — NCKH portable skill-kit proposal

**Ngày:** 2026-09-30, Asia/Saigon  
**Phạm vi:** đọc objective và toàn bộ 13 tài liệu trong `plans/260930-1910-nckh-portable-skill-kit/`; đối chiếu với runtime evidence đã có cho Claude Code, Cursor và Antigravity/`agy`. Codex được giữ ở mức đối chiếu của proposal vì parent sở hữu phần runtime đó. Đây là review read-only của **proposal chưa duyệt**, không phải acceptance của package.

## Verdict

Proposal nhất quán ở cấp kiến trúc và giữ đúng scope DESIGN: đủ NCKH Core, Engineer Kit, Marketing Kit và bốn adapter; Engineer/Marketing không bị thu hẹp thành scientific-only. Không có bằng chứng implementation, consumer run, native hook/plugin run, model call hoặc installer mutation trong lượt này. Có 5 vấn đề cần chốt trước khi duyệt contract, và 4 gap cần bổ sung trước khi gọi route/installer là release-ready.

## Những điểm đã khớp và không nên đảo ngược

- Full scope được giữ rõ: `plan.md:21-24`, `architecture.md:14-18`, `phase-03-engineer-and-xia.md:10-27`, `phase-04-marketing.md:10-27`, `skill-catalog.md:32-78`. Việc các phase chưa code là đúng trạng thái `PROPOSED/PENDING`, không phải thiếu deliverable hiện tại.
- Source-of-truth, ownership và build closure đã tách hợp lý: `architecture.md:42-88,120-166`, `phase-01-start.md:31-59`, `phase-05-runtime-adapters-and-build.md:31-57`. Không thấy parallel ownership nguy hiểm giữa P1/P2/P3/P4/P5/P6/P7; registry/shared contract đã yêu cầu integrate tuần tự.
- Evidence boundary tốt: docs/help không được coi là host acceptance (`runtime-compatibility.md:3-12,96-125`); human/native, rights, paid budget và release vẫn pending (`phase-02-core-research-writing-visuals.md:44-52`, `phase-07-qualification-and-migration.md:20-29,46-55`).
- Auto/interactive đã được phân biệt bằng state, review boundary và feedback/resume thay vì “hỏi nhiều hơn” (`workflow-and-model-routing.md:27-68`). `auto` không được biến thành unrestricted shell/commit/publish (`workflow-and-model-routing.md:37-39`), và mandatory human gate vẫn giữ (`workflow-and-model-routing.md:59-65`).
- Runtime research được phản ánh đúng các khác biệt đã xác minh: Cursor IDE launcher khác Agent CLI, Agy CLI/global khác IDE/global, fresh context không đồng nghĩa sandbox, và Agy `max` chưa được nâng thành enum portable (`phase-05-runtime-adapters-and-build.md:17-29`; `runtime-compatibility.md:26-28,44-85`).

## Findings cần xử lý

### F-01 — High: tên và public contract của Xia chưa quyết định

**Evidence:** Objective yêu cầu `/ak-xia` và các mode compare/port/improve tại `goal-objective.md:87-101,380`. Proposal lại giữ upstream `/ak-xia` nhưng đặt workflow mới là `/nckh-xia` (`architecture.md:168-177`; `workflow-and-model-routing.md:83-97`; `skill-catalog.md:53-55`; `phase-03-engineer-and-xia.md:23-27`). Installer còn cấm cài alias shadow `/ak-xia` (`installer-evaluation-migration.md:20-22`).

**Risk:** Đây là thay đổi public namespace chứ không chỉ merge nội bộ. Người duyệt không thể biết `/ak-xia` trong objective là surface NCKH phải cung cấp hay chỉ là upstream semantics cần nghiên cứu.

**Fix đề nghị:** ghi một decision gate trước P1: (a) giữ `/ak-xia` nguyên bản và quảng bá `/nckh-xia` là workflow riêng, có handoff rõ; hoặc (b) tạo adapter projection cho `/ak-xia` với collision/ownership check nhưng không shadow file upstream. Không tự chọn một phương án trong implementation.

### F-02 — High: logical `/nckh-*` chưa có support matrix cho UI và headless

**Evidence:** Objective mô tả `/nckh-plan`, `/nckh-cook` như public primitives (`goal-objective.md:41-82`). Proposal lại nói đây chỉ là notation, adapter mới chọn host handle (`workflow-and-model-routing.md:1-5`; `runtime-compatibility.md:70-73`). Runtime evidence xác nhận slash headless chưa consumer-probe cho Claude, Cursor và Agy (`plans/reports/researcher-260930-1910-runtime-compatibility.md:50-68,98-104`). P5 mới yêu cầu probe chung “explicit + implicit VI/EN” (`phase-05-runtime-adapters-and-build.md:49-57`), chưa tách từng invocation surface.

**Risk:** Có thể ghi “skill installed” nhưng người dùng không gọi được `/nckh-plan` trong CLI; `cursor.cmd` không phải Agent CLI, còn `agy -p` là prompt runner chứ chưa chứng minh arbitrary skill API.

**Fix đề nghị:** thêm ma trận `logical_entrypoint × host/surface × invocation` với các cell `ui-slash`, `native-menu`, `headless-prompt`, `implicit`, `unsupported`, và trạng thái `verified|docs-only|unverified`. Generated docs chỉ quảng bá syntax đã có consumer receipt; cell chưa probe phải trả `UNVERIFIED/NOT_CALLABLE`, không tạo shell alias để giả support.

### F-03 — High: shared roots và compatibility roots có thể tạo duplicate/wrong projection

**Evidence:** Proposal biết phải detect duplicate visibility (`runtime-compatibility.md:38-42`) và cấm artifact thủ công (`architecture.md:72-88`). Nhưng matrix chỉ ghi `.cursor/skills/` hoặc `.agents/skills/` cho Cursor, không liệt kê cụ thể compatibility roots `.claude/skills/`, `.codex/skills/` và global counterparts đã có trong runtime research (`plans/reports/researcher-260930-1910-runtime-compatibility.md:57-61`). Agy CLI/IDE cũng dùng chung workspace `.agents/skills/` nhưng global roots khác (`runtime-compatibility.md:26-28`; report `:65-69`). Installer mới yêu cầu hiển thị skill trùng tên (`installer-evaluation-migration.md:16-29`), chưa định nghĩa ownership khi một target hiển thị qua nhiều host.

**Risk:** Chọn nhiều runtime có thể copy cùng skill vào `.agents/skills`, `.cursor/skills`, `.claude/skills` và `.codex/skills`; một host sẽ thấy nhiều bản, uninstall có thể gỡ nhầm consumer khác, hoặc host-specific frontmatter bị dùng ở shared root.

**Fix đề nghị:** manifest phải có `physical_path`, `visible_surfaces`, `owner`, `representation` (`shared-neutral|host-specific`), precedence và conflict action. Chỉ dùng một shared artifact khi đã chứng minh cùng artifact chạy đúng các host; nếu projection khác nhau thì cài các bounded paths riêng. Bổ sung fixture cho toàn bộ compatibility roots, nested discovery, case-fold collision và uninstall khi còn owner.

### F-04 — High: `--auto` là workflow state nhưng chưa có permission mapping theo host

**Evidence:** Proposal đúng khi cấm `auto` tự cấp shell/admin/network/paid/publish (`workflow-and-model-routing.md:31-39,59-65`; `phase-05-runtime-adapters-and-build.md:25-29`). Tuy nhiên P5 chỉ nói map permissions/hooks riêng theo surface (`phase-05-runtime-adapters-and-build.md:23-29,49-57`), chưa có bảng chuyển logical `auto` sang permission profile thực tế. Runtime research đã khuyến cáo không dùng prompt text để giả enforcement và phải `NOT_CALLABLE` khi host không đủ isolation (`plans/reports/researcher-260930-1910-runtime-compatibility.md:87-95`).

**Risk:** Adapter tương lai có thể nhầm `--auto` với vendor force/yolo/dangerously-skip-permissions, hoặc coi soft-denied tool là thành công. Khi đó auto/interactive boundary trong workflow không còn tương ứng với quyền host.

**Fix đề nghị:** định nghĩa `auto_policy` theo `host/surface/version`: routine operations được phép, external/irreversible operations phải ask/deny, sandbox, approval mode, tool/egress allowlist và stop behavior. Cấm blanket force flags trong contract. Test shell, MCP, web, file write, paid/external và mandatory human gate trên từng surface; thiếu enforcement thì route là `NOT_CALLABLE`.

### F-05 — High: model profile có policy tốt nhưng thiếu schema mapping/effective proof đủ cụ thể

**Evidence:** Objective yêu cầu 5 profile và map `fast/worker/deep` theo runtime (`goal-objective.md:197-233,256-266`). Proposal có logical tiers, fallback và logging requested/resolved (`workflow-and-model-routing.md:117-152`; `phase-05-runtime-adapters-and-build.md:19-29,51-73`). Installer chỉ yêu cầu preview `effective/inherit/unavailable` (`installer-evaluation-migration.md:30-39`). Runtime evidence cho thấy Cursor effort nằm trong parameterized model syntax, Claude có effort CLI/agent riêng, còn Agy custom-agent model aliases và CLI `--effort max` không đồng nhất (`plans/reports/researcher-260930-1910-runtime-compatibility.md:71-76`).

**Risk:** `config-models` có thể ghi một chuỗi cấu hình nhưng runtime không đọc, hoặc requested model bị report như effective model. Đặc biệt dễ sai ở Cursor parameterized model, Agy agent-vs-CLI effort và host precedence.

**Fix đề nghị:** khóa schema per `host/surface/version` gồm `requested_tier`, `requested_model`, `requested_effort`, `encoding/field`, `config_path`, precedence, `resolved`, `effective`, evidence source, fallback reason và billing/availability status. Chỉ đặt `applied/effective` sau native receipt; thêm negative cases cho model invalid, Cursor parameterized effort và Agy `max`. Không downgrade `deep` thành `fast` âm thầm.

### F-06 — Medium: plugin/hook lifecycle chưa phân biệt projected, installed, enabled và trusted

**Evidence:** Architecture xác định plugin là optional projection chứ không phải source authority (`architecture.md:83-88`); P5 cấm builder sửa runtime config (`phase-05-runtime-adapters-and-build.md:31-47`); installer tách hook trust (`installer-evaluation-migration.md:30-39`). Runtime research cho thấy Claude/Cursor có `--plugin-dir` local/session loading, trong khi Agy có plugin install/enable lifecycle và path CLI/IDE khác nhau (`plans/reports/researcher-260930-1910-runtime-compatibility.md:79-85`).

**Risk:** Installer có thể ghi “installed” khi mới copy plugin hoặc load session-only, hoặc tự coi plugin/hook đã trusted; uninstall/update ownership sẽ sai.

**Fix đề nghị:** manifest tách `projected`, `copied`, `registered`, `enabled`, `trusted`, `session_only`, `tested`; mỗi transition cần user authorization và receipt. `--plugin-dir` chỉ là load route nếu host không persist; Agy `plugin install/enable` là external mutation riêng. Không auto-trust hook, không claim plugin support chỉ từ manifest/help.

### F-07 — Medium: OS/host qualification target chưa được chốt, dù installer scope đã mở rộng

**Evidence:** Objective yêu cầu cả `install.ps1` và `install.sh` (`goal-objective.md:237-282`). P6 yêu cầu validate Windows/macOS/Linux và success chỉ pass khi mọi OS/runtime cell có evidence (`phase-06-installer-and-recovery.md:45-53,63-77`). Local runtime evidence hiện chỉ là Windows binary/help observations (`plans/reports/researcher-260930-1910-runtime-compatibility.md:22-27`).

**Risk:** `install.sh` và effort 4–6 ngày có thể bị hiểu là đã hỗ trợ POSIX/macOS/Linux, trong khi chưa có lab/owner/fixture cho các OS đó. Đây không chặn DESIGN, nhưng chặn release claim và làm effort hiện tại khó đáng tin.

**Fix đề nghị:** khóa advertised OS matrix trước P6 (`design-only|fixture-tested|native-accepted`), ghi lab owner và test surface cho mỗi cell. Không gọi script POSIX là macOS/Linux support; cell không có native evidence phải giữ pending và không nằm trong default release profile.

### F-08 — Medium: eval có per-skill coverage nhưng chưa explicit routing-conflict suite

**Evidence:** Objective yêu cầu routing đúng, spawn hợp lý và runtime compatibility (`goal-objective.md:348-367`). Catalog yêu cầu positive/negative/outcome/failure cho từng skill (`skill-catalog.md:98-113`), còn case matrix đã có duplicate discovery và host paths (`installer-evaluation-migration.md:109-134`). Chưa thấy case family riêng cho no-tag routing, manual-tag conflict/unsupported tag, direct domain skill versus plan/cook, hoặc duplicate metadata với cùng trigger.

**Risk:** Từng skill có eval vẫn có thể pass nhưng router chọn sai owner, spawn trùng hoặc bypass `/nckh-plan`/`/nckh-cook` boundary.

**Fix đề nghị:** thêm routing cases và oracle: no tag, valid tag, conflicting tag, unavailable tag, incomplete catalog, same-trigger collision, plan-only versus cook intent, direct skill versus logical primitive. Ghi selected/rejected candidates, reason, fallback và `NOT_CALLABLE`; không đánh giá routing bằng tên folder hoặc prompt match đơn thuần.

### F-09 — Medium: receipt contract chưa phản chiếu hết qualification dimensions

**Evidence:** Architecture receipt tối thiểu mới nêu skill/adapter/runtime/model, hashes, checks, cost và limits (`architecture.md:102-114`). Workflow có requested/resolved model/effort (`workflow-and-model-routing.md:139-143`), còn P7 yêu cầu evidence theo skill/host/surface/version/mode (`phase-07-qualification-and-migration.md:18-29,46-55`).

**Risk:** Có thể không reconstruct được invocation nào, permission state nào, plugin lifecycle nào và kết quả exit/output format đã tạo một receipt; khi đó “per-cell qualification” không audit được.

**Fix đề nghị:** mở rộng receipt schema với `host`, `surface`, `version`, `entrypoint`, `invocation_mode`, `skill/agent/plugin identity`, requested/resolved/effective model+effort, permission/sandbox, tool/egress calls, output/exit status, artifact/closure hashes, usage/cost coverage và `observed|docs-only|unverified|not-run`. Giữ raw transcript/credentials ngoài report.

## Release probes bắt buộc trước khi đổi proposal thành approved build

1. Fixture disposable cho từng host/surface: project/global/plugin precedence, duplicate roots, UI slash/native menu, headless prompt, implicit VI/EN và cleanup; không coi help là consumer run.
2. Read-only subagent fixture: fresh context, `readonly`/tool scope, shared-vs-worktree/branch, background/parallel join, timeout-unknown và owner cleanup.
3. Model fixture: valid/invalid ID, requested-vs-effective receipt, effort encoding; riêng Cursor parameterized effort, Claude effort, Agy CLI `max` và custom-agent aliases.
4. Permission fixture: logical auto/interactive trên file, shell, MCP/web/external/irreversible actions; hook allow/deny/invalid output/nonzero/timeout/crash; không dùng dangerous bypass flags.
5. Installer fixture: all compatibility roots, copy/symlink, shared ownership, plugin session-vs-persistent state, user edits, crash/recovery/uninstall và OS cells đã được quảng bá.

## Kết luận trạng thái

**Status:** DONE_WITH_CONCERNS

**Summary:** Proposal có nền tảng tốt, full 3 kits/4 host adapters ở DESIGN, ownership rõ, evidence boundaries và auto/interactive intent đúng hướng. Runtime research không cho thấy contradiction lớn trong các claims đã được đánh dấu docs/local/unverified; các khác biệt Cursor Agent CLI, Agy CLI/IDE roots, fresh context/isolation và effort `max` đã được phản ánh.

**Concerns/Blockers:** Chưa duyệt namespace Xia; chưa có invocation support matrix theo UI/headless; shared/compatibility roots, logical auto permission mapping, model config/effective proof và plugin lifecycle cần khóa trước P1/P5/P6. Chưa có native consumer/hook/plugin/model/OS acceptance; không được gọi proposal này là portable/release-ready cho đến khi các receipt/probes trên hoàn tất. Report validation link hiện là dependency của proposal và được giữ ngoài review implementation.

## Follow-up delta review — bounded contract integration

**Phạm vi follow-up:** chỉ đọc các phần mới của `runtime-compatibility.md`, `workflow-and-model-routing.md`, `architecture.md`, `installer-evaluation-migration.md` và delta của P1/P5/P6/P7. Không chạy native probe, provider, installer, hook, plugin hoặc model. Các probe đó là gate trước acceptance/release, không phải điều kiện để duyệt DESIGN/no-code.

### Kết quả F02–F09

- **F02 — resolved at contract level.** Projection matrix hiện tách ba logical entrypoints theo 8 host/surface, `ui-slash`, `native-menu`, `headless-prompt`, `implicit`, cùng các trạng thái `docs-only|observed|unverified|unsupported|not-applicable`; route chưa có proof không tự dispatch (`runtime-compatibility.md:45-66`). P5 đã yêu cầu probe riêng theo UI/menu/headless/implicit và giữ cell unverified (`phase-05-runtime-adapters-and-build.md:49-57`). Đây là contract proposal, chưa phải consumer evidence.
- **F03 — resolved at design level.** Matrix đã ghi Cursor compatibility roots (`runtime-compatibility.md:38-43`); installer manifest có `physical_path`, `visible_surfaces`, owners, `representation`, precedence và conflict action, kể cả shared-neutral/host-specific projection (`installer-evaluation-migration.md:64-83`). P6 đã nhận ownership/neutral-vs-host-specific/nested-root tests (`phase-06-installer-and-recovery.md:47-53`).
- **F04 — resolved at design level.** Permission projection định nghĩa `auto_policy`, giữ native sandbox/approval/tool policy, cấm blanket bypass và tách mandatory human boundaries; external/irreversible paths có negative tests (`runtime-compatibility.md:139-155`). P5/P7 đã propagate tool coverage và permission cases (`phase-05-runtime-adapters-and-build.md:52-57,67-73`; `phase-07-qualification-and-migration.md:48-52`). Native enforcement vẫn pending, đúng với trạng thái DESIGN.
- **F05 — resolved at schema level.** Model-resolution contract đã có target, request, native encoding/path/precedence, resolution, effective observation và evidence class; `configured`, `applied`, `effective` được phân biệt (`workflow-and-model-routing.md:145-167`). P1 khóa negative cases và không dùng requested-as-effective (`phase-01-start.md:51-59`); P5/P6 giữ model mapping unsupported/overridden là limitation (`phase-05-runtime-adapters-and-build.md:51-73`; `phase-06-installer-and-recovery.md:47-52`).
- **F06 — resolved at transaction-design level.** Plugin/hook lifecycle đã tách `projected`, `copied`, `registered`, `enabled`, `trusted`, `session-only`, `tested`; `--plugin-dir` không bị gọi là persistent install và không auto-trust (`installer-evaluation-migration.md:64-90`). Đây vẫn là future implementation contract, chưa chứng minh native state.
- **F07 — resolved at scope/evidence level.** OS matrix hiện phân Windows/macOS/Linux, design/local evidence, fixture/native acceptance và owner; POSIX script không được coi là macOS/Linux proof (`runtime-compatibility.md:157-169`). P6 đã yêu cầu khóa lab owner/support cells trước phase và giữ thiếu lab là pending (`phase-06-installer-and-recovery.md:47-53,63-77`).
- **F08 — resolved.** Case matrix đã thêm routing intent/tag/catalog conflicts: no-tag, valid/conflicting/unsupported tag, incomplete catalog, same-trigger collision và direct domain versus plan/cook (`installer-evaluation-migration.md:137-159`). P1 cũng đã nhận các cases và oracle này (`phase-01-start.md:51-59`); P7 đồng bộ thành 19 case families (`phase-07-qualification-and-migration.md:14,48-63`).
- **F09 — resolved.** Receipt hiện bao gồm host/surface/version, logical entrypoint/mode/actual invocation, skill/agent/plugin identities, requested/resolved/effective model+effort, permission/sandbox, tool/egress, exit/output, hashes, cost coverage, evidence class và limitations (`architecture.md:102-111`).

### Kiểm tra propagation và vấn đề còn mở

- P1/P5/P6/P7 đều đã nhận contract mới mà không chuyển future probes thành current pass: P1 giữ consumer/paid/OS probe pending khi chưa được phép (`phase-01-start.md:57-59`); P5 ghi native cells unverified (`phase-05-runtime-adapters-and-build.md:56-57,67-73`); P6 giữ OS/native acceptance opt-in (`phase-06-installer-and-recovery.md:61,69-77`); P7 tách validate-only khỏi provider/human execution (`phase-07-qualification-and-migration.md:48-55,73-81`).
- F01 **vẫn là explicit user decision gate, không phải contradiction cần tự sửa**: architecture giữ `/ak-xia` upstream (`architecture.md:170-177`), workflow đặt `/nckh-xia` riêng và ghi rõ trade-off cần duyệt (`workflow-and-model-routing.md:83-97`), installer không cài alias shadow (`installer-evaluation-migration.md:20-22`). Không được tự đổi namespace.
- Không phát hiện contradiction concrete mới trong delta đã đọc. Proposal hiện coherent để tiếp tục **DESIGN review**, nhưng chưa được gọi là native-compatible/release-ready; các native receipts vẫn đúng chỗ ở acceptance/release.

**Follow-up Status:** DONE_WITH_CONCERNS  
**Follow-up Summary:** F02–F09 đã được tích hợp nhất quán ở mức contract/schema/phase ownership; F01 được giữ nguyên là quyết định người dùng. Không native test nào được chạy hoặc cần chạy trước khi duyệt DESIGN.

**Follow-up Concerns/Blockers:** Chỉ còn namespace Xia và các lựa chọn support/OS cells cần user/owner khóa; native behavior, effective model, hook/plugin lifecycle và installer safety vẫn là pending release evidence, không phải bằng chứng hiện tại.
