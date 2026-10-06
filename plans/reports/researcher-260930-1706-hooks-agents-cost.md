# Nghiên cứu: hooks, subagents và chi phí cho wrapper viết khoa học

**Ngày truy cập:** 2026-09-30 (Asia/Saigon)  
**Phạm vi:** thiết kế nghiên cứu cho skill wrapper cá nhân; chưa tạo package, chưa gọi provider, chưa cài đặt, chưa publish.  
**Kết luận ngắn:** dùng một wrapper cục bộ mỏng, giữ state `plan -> cook` ở coordinator, và coi host (Codex hoặc Claude) là adapter có khả năng không đầy đủ. Worker chỉ được dùng cho nhiệm vụ độc lập, có biên giới và schema kết quả rõ. Quyền, ngân sách, hash và cổng external phải được kiểm tra đồng bộ trước hành động; hook hậu kỳ chỉ ghi receipt/telemetry.

## Khuyến nghị xếp hạng

1. **Khuyến nghị chính — local coordinator + thin host adapter.** Coordinator sở hữu user contract, plan revision/hash, quyền, ngân sách, provenance, acceptance và tổng hợp cuối. Adapter chỉ ánh xạ catalog, hook, tool và subagent API mà runtime thực sự cung cấp. Mặc định một worker; có thể tự chọn parallelism có giới hạn trong plan/grant/budget đã duyệt, không bắt user gọi thêm lệnh hoặc duyệt lại từng worker trong scope đó.
2. **Fallback — `NOT_CALLABLE`.** Nếu không chứng minh được capability catalog, instruction/reference closure, hoặc execution interface thật sự gọi được, không suy diễn từ tên skill hay việc đọc `SKILL.md`; trả trạng thái chưa gọi được, lý do và bước cần mở quyền.
3. **Không khuyến nghị — portability-by-assumption.** Không coi hook của Claude là hook Codex, không coi Agents API/SDK là Codex CLI, và không coi CLI inventory cục bộ là catalog runtime. Một route mới có ý nghĩa phải quay lại plan.

Thiết kế này khớp ràng buộc hiện có: giao diện người dùng vẫn chỉ `plan -> cook`; discovery, matching, instruction loading và worker routing có thể diễn ra nội bộ; tag thủ công chỉ là preference, không phải bypass quyền. Cook phải revalidate capability/instruction/reference/dependency hash, permission, egress và budget trước khi chạy.

Bảng event bên dưới dùng **semantic event của wrapper**. Tên `PreToolUse`, `SubagentStart` hay `PostToolBatch` chỉ là mapping có thể có ở một host, không phải API chung. Adapter phải map sang capability thật hoặc dùng workflow gate tường minh; không chứng minh được mapping thì route cần enforcement không được hỗ trợ.

## Bằng chứng capability và mức tin cậy

| Route | Evidence hiện có | Sức mạnh và giới hạn |
|---|---|---|
| Codex CLI | Local `codex-cli 0.154.0`; `hooks`, `multi_agent`, `skill_search`: stable, enabled; `multi_agent_v2`: stable, disabled; `token_budget`, `runtime_metrics`: under development, disabled. `codex exec` có noninteractive execution, schema output, sandbox/approval/model controls. | Bằng chứng host cục bộ, không phải cam kết API ổn định. `codex help hooks` không có; không được tự chế một `listskill` hay `run-skill` interface. |
| Codex hooks | Tài liệu chính thức mô tả lifecycle, trust, deny/rewrite và giới hạn hook. | Có thể làm guardrail cục bộ; OpenAI nói rõ tool hooks không phải enforcement boundary hoàn chỉnh. |
| OpenAI Agents API/multi-agent | Tài liệu chính thức mô tả independent subagents, explicit concurrency, shared filesystem/tools và event stream. | Route API riêng; không suy ra tính tương thích với Codex CLI/SDK. Multi-agent còn beta và schema có thể đổi. |
| Claude Code/Agent SDK | Tài liệu chính thức mô tả hook events, `PreToolUse`, subagents, permissions, tracing/cost. | Host khác; failure semantics phụ thuộc event, handler và runtime. Không khái quát mọi timeout thành fail-open; route cần guard bắt buộc phải có enforcement được kiểm chứng. |
| Claude Managed Agents | Tài liệu chính thức có shared budget và tối đa 25 threads. | Sản phẩm Managed Agents riêng; không phải bằng chứng Claude Code/Agent SDK có cùng route. |
| AgentKit local | `ak skills list/search --json` và `ak agents list/search --json` trả catalog rỗng; `ak kit list-kits` lỗi vì thiếu `./kits`. | Chỉ cho thấy inventory hiện tại không đủ; phải resolve catalog native lúc execution, không coi tên lệnh là capability. |

## Hook contract đề xuất

Hook chỉ là một lớp kiểm soát phụ trợ. Với operation cần authorization/budget/receipt guard bắt buộc, coordinator phải chặn nếu guard thiếu và không có host/adapter guard tương đương đã được kiểm chứng. Hook advisory thiếu không tự chặn tác vụ thông thường; không dựa vào một giả định fail-open/fail-closed chung cho mọi event.

| Điểm | Việc cần làm | Quyết định an toàn |
|---|---|---|
| `SessionStart` | Nạp manifest ngắn: plan/profile, capability shortlist, revision/hash, limits. | Không nạp toàn bộ corpus hoặc skill tùy tiện. |
| `UserPromptSubmit` | Phân loại `plan`/`cook`, hiển thị thiếu authorization và trạng thái pending. | Không tự nâng quyền hay biến tag thành permission. |
| `PreToolUse` / `PermissionRequest` | Kiểm tra phase, exact plan hash, tool/worker allowlist, external egress, provider, file scope, budget và dependency closure. | Fail closed; deny/ask nếu mismatch. Với Codex, `PreToolUse` có thể deny/rewrite; `ask` không được coi là semantics được hỗ trợ. |
| `SubagentStart` | Tiêm delegation packet tối thiểu gồm scope, schema và limits. | Context injection không phải authorization; Codex không dùng `continue:false` để chặn start. |
| `PostToolUse` / `SubagentStop` / `PostToolBatch` | Ghi receipt đã redact: worker/version/hash, inputs/outputs hash, source locators, status, usage và uncertainty. | Không cố rollback side effect bằng hậu hook. |
| `PreCompact` / `PostCompact` | Trước compact ghi manifest; sau compact khôi phục manifest và open gates. | Không khôi phục như sự thật một transcript/corpus stale. |
| `SessionEnd` | Đóng receipt, cleanup và đánh dấu incomplete nếu cần. | Không coi session end là completion proof. |
| Async/background | Chỉ telemetry, audit queue hoặc advisory context. | Async không được approve, deny, rewrite hay block trigger; unfinished work bị hủy khi session kết thúc. |

Codex có nhiều matching command hooks chạy concurrent; deny có thể dùng `permissionDecision: "deny"` hoặc exit code `2`, nhưng trust/hash của hook vẫn là điều kiện riêng. Claude Code cũng chạy matching hooks song song và deny thắng, nhưng missing hook/nonzero thông thường có thể cho action chạy tiếp. Vì vậy wrapper cần một synchronous preflight độc lập với host. Nguồn: [Codex hooks](https://developers.openai.com/codex/hooks), [Claude Code hooks](https://code.claude.com/docs/en/hooks), [Claude Agent SDK hooks](https://code.claude.com/docs/en/agent-sdk/hooks).

Không gọi LLM ở mọi `PostToolUse` hoặc mỗi lần gõ prompt. Dedupe theo `run_id/event_id/input_hash`; có guard reentrancy/recursion, timeout, output-size và side-effect. Chỉ dùng async hook cho logging/telemetry; actual adapter/host phải chặn operation cần guard bắt buộc nếu hook crash, no-match hoặc disabled mà không có enforcement tương đương. Hook installation/configuration là deployment step cần permission riêng, không phải kết quả của plan.

## Ownership và delegation packet

**Coordinator sở hữu:** user contract; lifecycle `plan -> cook`; plan revision/hash; permission và egress; context/budget pool; worker concurrency; acceptance status; provenance; final synthesis; human-review và release gates.

**Worker chỉ nhận:** `task_id`; capability ID và lý do chọn; input paths/hashes; exact file/source allowlist; read/write scope; profile/venue và revision; output schema/acceptance; provenance/citation requirements; authority boundary; tools/egress; token/context allocation; timeout/stop rule; cwd/timezone/output language; report path; no-provider/no-write/no-publish flags. Worker không được tự spawn worker khác, ghi shared mutable state, publish, thanh toán, hoặc tự chuyển output thành human-reviewed/accepted.

**Worker phải trả structured result:** `status`; claims và supporting evidence/source locators; uncertainty/open limits; artifact/input/output hashes; worker/model/version; usage và retry count; failure reason. Không có execution interface thật thì `status=NOT_CALLABLE`, không thay bằng việc đã đọc instruction.

OpenAI khuyến nghị subagent cho nhiệm vụ độc lập có câu hỏi/kết quả rõ; Claude cũng cảnh báo parallelism chỉ hữu ích khi thật sự độc lập và summary chi tiết làm tăng context/token. Do đó mặc định một worker; chỉ chạy các track độc lập như source verification và citation audit với bound explicit, không nested spawn. Nguồn: [OpenAI multi-agent](https://developers.openai.com/api/docs/guides/agents-api/multi-agent), [OpenAI deployment checklist](https://developers.openai.com/api/docs/guides/deployment-checklist), [Claude sub-agents](https://code.claude.com/docs/en/sub-agents).

## Chi phí, chất lượng và observability

Định nghĩa một task được chấp nhận:

```text
all_attempt_cost
  = planning/discovery + root/controller calls + every worker call
  + hooks/tools/sandbox/provider/image/review charges
  + retries, recovery and other third-party charges
cost_per_accepted_task = all_attempt_cost / accepted_task_count
```

`accepted_task_count=0` làm metric **undefined**, không phải zero/savings. Luôn thêm `unknown_cost` khi usage null/thiếu, estimate không authoritative, cache-write không lộ ra, batch có khả năng overshoot, subscription quota khác hóa đơn API hoặc không rõ, hoặc tool/provider charge chưa phân giải. `accepted_task_cost` không phải chỉ là USD: ghi cùng evidence coverage, citation/source integrity, factual fidelity, safety, human-review status, edit effort, latency và failure/retry count.

- Không báo “tiết kiệm” chỉ vì context ngắn, cache hit cao, hay dùng worker rẻ. So sánh direct route và worker route dưới cùng quality bar, corpus/profile, retry policy và acceptance gates.
- Tài liệu **OpenAI Agents API** cảnh báo usage có thể best-effort/null và có thể undercount subagent; phải inspect root và child turns/traces. Tracing của route đó tách usage root/subagent; parent span không bao gồm child span. Đây không phải bằng chứng telemetry của Codex hiện tại. Tài liệu **Claude Agent SDK** phân biệt client-side `total_cost_usd` estimate với Usage/Cost API authoritative; top-level usage không bao gồm subagent token. Mỗi adapter phải xác minh semantics riêng trước cộng chi phí.
- Giá là dynamic. Chỉ lookup [OpenAI pricing](https://developers.openai.com/api/docs/pricing?tab=suite) hoặc [Claude pricing](https://platform.claude.com/docs/en/about-claude/pricing) lúc evaluation/execution; không hard-code trong skill/report.
- Receipt tối thiểu: `task_id`, plan/profile/hash, worker/model/version/hash, dependency closure, tool/provider calls, input/output/cache tokens, duration, retries, estimated/unknown cost, quality metrics, status và open limits.

Nguồn: [OpenAI observability](https://developers.openai.com/api/docs/guides/agents-api/observability), [OpenAI tracing](https://developers.openai.com/api/docs/guides/agents-api/tracing), [Claude SDK cost tracking](https://code.claude.com/docs/en/agent-sdk/cost-tracking).

## Context và cost optimization

Áp dụng policy nội bộ của project, không trình bày như host limit phổ quát. Với context `i`, gọi `K_i` là skill-related tokens (catalog metadata, active `SKILL.md`, required references, upstream instructions, delegation prompt, hook injection, routing/tool schemas và phần lặp kế thừa), `W_i` là window đã xác minh, `H_i` là host overhead, `D_i` là task/source text và `O_i` là output/reasoning reserve; phải kiểm `K_i + H_i + D_i + O_i <= W_i`. Trần đồng thời: soft `min(20,000, floor(0.10 × W_i))`, hard `min(40,000, floor(0.20 × W_i))`. Đây là shared pool của coordinator + workers còn giữ context/resume, không phải quota độc lập mỗi worker; cumulative token/cost không reset khi đổi worker. Không truncate mandatory skill file; giảm worker count hoặc load theo phase.

Đây là upper bounds, không phải mục tiêu dùng hết. Ví dụ giả định `W=128k` cho soft `12.8k`, hard `25.6k`; 40k vẫn sai dù chưa chạm absolute ceiling. Cần serialize packet thực tế và ghi `measured|estimated|partial|unknown`, window source, tokenizer revision và safety buffer; không dùng `chars/4` như phép đo chính xác. Host overhead/catalog ẩn không đo được thì không certify budget-compliant.

1. Đặt stable wrapper instructions, contract schemas, tool definitions và capability metadata ở prefix; task biến đổi ở sau breakpoint. Prompt cache chỉ tái sử dụng computation khi prefix render chính xác; session không bảo đảm cache hit.
2. Shortlist bằng metadata trước; chỉ đọc full `SKILL.md` và references của candidate thực sự; phase-scope dependency closure.
3. Invalidate/rescan khi source/profile/version/hash/rights/retraction/venue policy đổi. Cache không chứng minh freshness, licensing hay scientific validity.
4. Batch chỉ dành cho offline eval, classification, embedding, reranking và fault suite. Không dùng cho interactive `plan`/`cook`; kiểm tra endpoint support, completion/expiry và spend limit ở execution time.
5. Nếu vượt cap: bỏ optional reference, giảm shortlist, reuse exact-revision evidence, serialize worker, hoặc mở fresh phase-scoped context. Không cắt rules/citations, đổi scope hay hạ quality để vừa cap; nếu mandatory baseline đã vượt thì đánh dấu runtime/profile incompatible.

Nguồn: [OpenAI prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching), [OpenAI Batch](https://developers.openai.com/api/docs/guides/batch), [Claude prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching), [Claude Batch](https://platform.claude.com/docs/en/build-with-claude/batch-processing).

## Trade-off và adoption risk

| Phương án | Safety/evidence | Cost/latency | Maturity/portability | Xếp hạng |
|---|---|---|---|---|
| Local coordinator + host adapter | Cao nhất: một owner cho hash, quyền, provenance và acceptance | Thêm preflight/receipt latency; cost đo được hơn | Phải viết adapter; portability có kiểm soát | **1 — chọn** |
| Native multi-agent trực tiếp | Tốt nếu task độc lập và event/trace đủ | Có thể nhanh hơn nhưng worker/retry/tool cost tăng; cache/savings không chắc | OpenAI route beta; Claude route host-specific | **2 — chỉ dùng cho track bounded** |
| Hook-only policy | Thấp: hook có trust, fail-open, async và host gaps | Rẻ lúc đầu, nhưng khó chứng minh cost/evidence | Dễ drift, không portable | **3 — không làm boundary** |
| Ad-hoc worker/fan-out | Thấp: shared writes, duplicate work, thiếu provenance | Có thể rẻ trong demo; khó kiểm soát retry và total spend | Cao adoption risk, không audit được | **4 — loại** |

Adoption risk chính: Codex hooks trust/hash và semantics khác Claude; multi-agent item schema/limits có thể thay đổi; tài liệu OpenAI về default `max_concurrent_subagents` có drift (trang multi-agent nêu `6`, deployment checklist nêu `3`). Vì vậy luôn set concurrency explicit, lưu host/version/capability snapshot và revalidate lúc cook. Claude có giới hạn depth/concurrency riêng; không bê nguyên sang Codex.

## Approval và giới hạn còn mở

- Responses API/Agents SDK không tự thừa hưởng Codex Auto-review; wrapper phải có approval/enforcement riêng và fail closed khi review timeout/unavailable. Nguồn: [guardrails and approvals](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals).
- Hook presence/registration không chứng minh host đang enforce; Codex plugin yêu cầu path tương đối dưới plugin root, script tồn tại và hook trust; plugin enable không tự trust hook. Nguồn: [plugin packaging](https://developers.openai.com/plugins/build/plugins).
- Hook Claude không tự portable sang Codex; phải adapt runtime và không phụ thuộc prompt/agent hook handler trong Chat thường. Nguồn: [Claude plugin conversion](https://developers.openai.com/plugins/guides/submit-claude-plugin).
- Chưa có bằng chứng consumer run của wrapper trong workspace hiện tại, provider quota/economics, venue/mentor/API permission, licensing/release, human gold labels, scientific validity hoặc nghiệm thu artifact trên runtime đích. Những gate này vẫn `PENDING`; không được hoàn thành bằng local CLI help, synthetic fixture, planning, hay receipt giả. Catalog/tool có mặt không thay bằng chứng chạy thành công.

## Giới hạn của nghiên cứu

Nghiên cứu không benchmark model/giá thật, không chạy provider, không test hook trên production host, không đo cache hit, không đánh giá chất lượng khoa học, và không xác nhận quota của subscription. Official docs là nguồn ưu tiên nhưng vẫn có thể drift; local CLI observations chỉ có giá trị cho host tại ngày truy cập. Bước execution phải lookup docs/pricing/capability hiện hành và ghi snapshot vào receipt.

## Nguồn chính thức đã kiểm tra

Các nguồn OpenAI/Claude ở trên được chọn vì là tài liệu maintainer/vendor; key claims về hooks, multi-agent, tracing, pricing, caching, batch và permissions đều được đối chiếu từ nhiều trang độc lập. Khi đưa vào implementation plan, giữ URL + section name + access date, không chép giá cố định.
