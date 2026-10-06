# Security adversary + fact-check review

Ngày review: 2026-09-30 (Asia/Saigon). Phạm vi: chỉ sáu phase của plan `260930-0905-vietnamese-research-skill-kit`; đọc thêm blueprint, brainstorm, synthesis và ba research reports. Không chạy provider/implementation, không sửa plan.

## Kết luận

Plan có định hướng fail-closed tốt, nhưng chưa đủ cụ thể để chuyển sang implementation an toàn. Bốn ranh giới cần khóa trước là authorization có thể chống replay, write boundary, fetch/parser/egress isolation và provenance xác thực cho upstream candidate. Tôi không coi các file `research-skill-kit/**` chưa tồn tại là lỗi: plan ghi rõ chúng là CREATE tương lai và filesystem hiện xác nhận điều đó.

## Findings

### SEC-01 — High — approval không bind actor, scope và thời hạn

- Location: `phase-01-start.md:28-30,46-49,57-64,102-108`.
- Failure scenario: một process/caller trên cùng máy có plan revision/hash có thể replay `research-cook` sau khi input, egress hoặc quyết định duyệt đã đổi; plan không yêu cầu run binding, expiry, revocation hay one-shot authorization. Đây là rủi ro local-run; không mặc định giả định multi-tenant.
- Evidence: contract chỉ nói “được người dùng cho phép” và hash/revision; không có authorization-record trong danh sách contract `phase-01-start.md:72-90`.
- Fix: với project-local mặc định, thêm authorization record bind vào local run ID/worktree, plan revision, exact input/profile/dependency/worker/egress scope, issued-at/expiry, nonce và revoke/consume state; verify trước worker/filesystem/network call và ghi approver/run vào receipt. Chỉ thêm principal/session isolation nếu sau này mở shared host.

### SEC-02 — High — plan-only có thể vô tình tạo side effect của `ak-plan`

- Location: `phase-01-start.md:28-30`; `plan.md:49-52`.
- Failure scenario: adapter gọi upstream `ak-plan` nhưng không chặn các side effect mà skill hiện hành mô tả: task hydration mặc định, HTML artifact khi có flag, handoff và journal. Điều này phá hợp đồng “chỉ plan/profile/permission record” hoặc làm lộ brief vào artifact khác.
- Evidence: `C:/Users/USER\.agents\skills\ak-plan\SKILL.md:21-24,72-84` ghi task hydration và journal; plan chưa có capability/deny-list cho các write này.
- Fix: route plan-only phải dùng interface tối thiểu đã chứng minh, chặn task/HTML/journal/publish, giới hạn output root và chạy sentinel-workspace test; nếu host không bảo đảm thì trả `NOT_CALLABLE`.

### SEC-03 — High — raw URL chưa có SSRF, redirect và parser isolation contract

- Location: `phase-02-evidence-and-research.md:43-52,88-89,152-156`; `phase-04-slides-and-scientific-visuals.md:39-40,93-95`.
- Failure scenario: raw source URL redirect tới loopback/private-IP/metadata endpoint, `file://`/UNC path hoặc signed URL; PDF/HTML parser tải tài nguyên phụ, archive bomb hoặc active content rồi đưa dữ liệu vào provider/native worker. “Allowlisted tools” không định nghĩa host, method, redirect hop, IP hay quota.
- Evidence: discovery bắt buộc giữ raw URL và reader nhận candidate/access; egress chỉ được nêu ở mức allowlist/redaction.
- Fix: fetch sandbox exact-host/scheme/method; resolve và kiểm lại IP ở mọi redirect; chặn loopback, private/link-local/metadata, file/UNC; giới hạn bytes/pages/time/MIME; tắt JS/external loads; parser không network; strip query credentials trước receipt.

### SEC-04 — High — source-injection policy chưa tạo trust boundary thực thi

- Location: `phase-02-evidence-and-research.md:43-44,88-89,123-133,147-149`; `phase-01-start.md:47-49,61-64`.
- Failure scenario: HTML/PDF chứa chỉ dẫn độc hại đi cùng context với reader/native subagent có tool capability. Model có thể gọi worker khác, gửi private manuscript hoặc thay đổi claim; ghi “ignored as data” không ngăn được tool call hay prompt-following.
- Evidence: plan định nghĩa source instruction là data nhưng không yêu cầu separate untrusted-content channel, tool-less reader hoặc mediation bắt buộc.
- Fix: truyền source qua structured data channel/delimiter, cấm raw source vào system/developer prompt, reader không có tool/network/write capability, mọi call qua capability-token proxy; thêm injection fixtures cho exfiltration, recursion và prompt-confusion.

### SEC-05 — High — hash drift detection không đủ chống upstream supply-chain compromise

- Location: `phase-01-start.md:38-40,85-87,109-110`; `phase-05-evaluation-and-packaging.md:37-40,109-111`.
- Failure scenario: repo/branch/dependency bị compromise nhưng candidate vẫn có hash mới và có thể qua local compatibility cases; hash ghi nhận content, không chứng minh content đến từ maintainer/trust root. Candidate sau đó được dispatch như worker.
- Evidence: source lock yêu cầu URL/path/commit/hash/license nhưng không yêu cầu signed commit/release, dependency lock provenance hoặc approval của trusted maintainer.
- Fix: pin immutable commit và lock dependency; verify signature/trusted digest/provenance; quarantine candidate, sandbox không network/write, require explicit promotion approval và review license trước khi `accepted`.

### SEC-06 — High — receipt/hash/locator có thể làm lộ private corpus

- Location: `phase-01-start.md:35-37,65-66`; `phase-02-evidence-and-research.md:50-58`; `phase-05-evaluation-and-packaging.md:60-62`.
- Failure scenario: raw URL chứa token/signed query, absolute private path, input/profile/brief/output hash hoặc generated-artifact path bị đưa vào shared receipt/manifest. Hash tài liệu ngắn có thể bị dictionary-match để chứng minh user có corpus cụ thể.
- Evidence: plan yêu cầu giữ hashes, source locators và output paths nhưng chỉ nói “redacted”, chưa định nghĩa canonicalization, secret stripping, keying, ACL hoặc TTL.
- Fix: opaque IDs; strip query/fragment/auth/signed params và absolute paths; dùng HMAC key ngoài receipt thay raw hash khi cần; encrypt + ACL + retention/deletion policy; DLP test trước khi publish/package.

### SEC-07 — High — package path/link validation chưa chặn traversal và symlink

- Location: `phase-01-start.md:63-66`; `phase-05-evaluation-and-packaging.md:60-62,112-115,168-169`.
- Failure scenario: artifact/source path do worker hoặc source cung cấp chứa absolute/UNC/`..` hoặc symlink/junction. `validate-package.py` có thể package file ngoài root, lộ secret hoặc overwrite file khi regeneration; plan chỉ yêu cầu verify links/hashes.
- Evidence: chưa có containment/no-follow/atomic-staging requirement trong package manifest hay regeneration path.
- Fix: enforce package root; normalize và reject drive/UNC/absolute/`..`, symlink/junction; open no-follow, stage trong temp rồi atomic move; không overwrite user originals; test malicious names/links.

### SEC-08 — Medium — rollback không vô hiệu hóa artifact/side effect của candidate

- Location: `phase-01-start.md:155-158`; `phase-05-evaluation-and-packaging.md:156-160`.
- Failure scenario: candidate đã tạo output, receipt, cache hoặc queued provider call rồi rollback chỉ đổi mapping/disable capability. Artifact candidate vẫn có thể được handoff hoặc cache reuse; external side effect không được thu hồi.
- Evidence: rollback mô tả mapping/disable và giữ failure record, chưa yêu cầu quarantine/invalidation, credential revoke, queue cancellation hay dependent-receipt invalidation.
- Fix: quarantine toàn bộ candidate outputs; invalidate dependent receipts/manifests; revoke/rotate worker credentials; cancel queued work; cấm handoff cho artifact candidate cho tới khi re-review.

### SEC-09 — Medium — Unpaywall wording có thể bị hiểu nhầm là quyền phân phối

- Location: `phase-02-evidence-and-research.md:38-40`.
- Failure scenario: implementer coi location do Unpaywall trả về là xác nhận quyền lưu/đóng gói full text. Research report nói rõ free/OA access không mặc nhiên cho phép redistribution.
- Evidence: `plans/reports/research-260930-0905-local-sources-and-evidence.md:90-94` (đặc biệt line 92) yêu cầu kiểm host/version/license riêng.
- Fix: đổi wording thành “discovery/OA-location signal”; bắt buộc verify version, host, license và redistribution right độc lập trước evidence storage/package.

## Verification sampling — 75 claims

Ký hiệu: `V` = evidence hiện hữu/record hoặc filesystem đã xác nhận, không phải implementation proof; `U` = chưa thể xác nhận current/live; `P` = đề xuất tương lai, không dùng làm bằng chứng; `F` = mâu thuẫn hiện hữu. Tôi lấy đúng 15 claim/phase, không chạy test/provider.

| Phase | 15 claim cụ thể và phân loại |
|---|---|
| P1 | 01 plan-only boundary (V, plan:17,49-60); 02 future root absent (V, p1:21-22); 03 English future instructions (P, p1:26-27); 04 cook needs permission (P, p1:28-30); 05 no `run-skill`/Darwin limitation (V-record, p1:31-34); 06 receipt fields (P, p1:35-37); 07 candidate vs accepted (P, p1:38-40); 08 resolve/execute/critic flow (P, p1:46-53); 09 lifecycle drift invalidation (P, p1:57-58); 10 separate schemas (P, p1:59-60); 11 capability fail-closed (P, p1:61-62); 12 default egress policy (P, p1:63-64); 13 portable path rule (P, p1:65-66); 14 rollback mapping (P, p1:155-158); 15 validation not run (V, p1:139-141). |
| P2 | 01 pending/no result (V, p2:12-17,137-139); 02 evidence-first order (P, p2:12-17); 03 access tiers (P, p2:27-33); 04 journal-strict Q1/Q2 (P, p2:34-37); 05 Scholar/PaperPop/Unpaywall roles (U, p2:38-40); 06 source text untrusted (P, p2:43-44); 07 immutable search log (P, p2:48-50); 08 reader anchors (P, p2:51); 09 verdict ledger (P, p2:52); 10 bounded reasoning (P, p2:53-54); 11 source hash/locator (P, p2:56-58); 12 systematic-label gate (P, p2:62-63); 13 quote locator gate (P, p2:64-69); 14 correction/retraction handling (P, p2:104-107); 15 no accepted research result now (V, p2:137-139). |
| P3 | 01 pending/future files (V, p3:18-19); 02 evidence-bound writer (P, p3:12-16); 03 English instructions/output switch (P, p3:17-18); 04 licensed corpus/human taste (P, p3:28-30); 05 mode/certainty preservation (P, p3:31-34); 06 EN scientific constraints (P, p3:35-37); 07 pure-prose exception (P, p3:38-41); 08 English instruction is not evidence (P, p3:42-44); 09 style/protected-region lock (P, p3:46-50); 10 critic non-factual (P, p3:51-58); 11 writer cannot create evidence (P, p3:56-58); 12 terminology ledger (P, p3:70-75); 13 human handoff (P, p3:76-80); 14 missing sample license blocks (P, p3:127-140); 15 tests not run (V, p3:143-145). |
| P4 | 01 pending/future files (V, p4:23-24); 02 chart/diagram/artwork split (P, p4:12-17,27-29); 03 native route through adapter (U, p4:30-31); 04 nature/Orchestra PPTX QA claim (U, p4:32-36); 05 Anthropic proprietary boundary (V-record, p4:36); 06 visualization references scope (P, p4:37-38); 07 provider/license gate (P, p4:39-40); 08 truth mapping (P, p4:46-49); 09 no unsourced chart mark (P, p4:52-54); 10 artifact-kind routing (P, p4:58-59); 11 chart raw values/uncertainty (P, p4:64-65); 12 illustrative artwork label (P, p4:66-67); 13 native+render QA (P, p4:68-70); 14 denied egress/unclear rights (P, p4:120-129); 15 visual tests not passed (V, p4:132-134). |
| P5 | 01 pending/future files (V, p5:23-24); 02 no implementation proof (V, p5:12-17); 03 matched baselines (P, p5:28-31); 04 holdout isolation (P, p5:32-33); 05 fault suite (P, p5:34-36); 06 candidate/hash closure (P, p5:37-40); 07 status vocabulary (P, p5:41-42); 08 eval disclosure (P, p5:56-59); 09 manifest redaction (P, p5:60-62); 10 human/external/license gates (P, p5:66-67); 11 safe-egress measurement (P, p5:68-69); 12 no publish/install/commit (P, p5:112-115); 13 notices/hash/link validation (P, p5:112-113); 14 package matrix (P, p5:125-142); 15 rollback behavior (P, p5:156-160). |

### Sampling counts and limits

- P1: 4 V, 0 F, 0 U, 11 P. P2: 2 V, 0 F, 1 U, 12 P. P3: 2 V, 0 F, 0 U, 13 P. P4: 3 V, 0 F, 2 U, 10 P. P5: 2 V, 0 F, 0 U, 13 P.
- Total: 13 V, 0 F, 3 U, 59 P = 75 sampled claims. `P` is a planned control, never proof that it exists or works.
- Current workspace check found blueprint (1,368 lines), plan/reports, and no `research-skill-kit/`; this matches the plan's CREATE-future declaration. No behavioral benchmark, human gold, provider run or package receipt was available to verify.

## Unresolved questions

- Ai is the authorization principal for cook, and where are approval expiry/revocation and egress scope persisted?
- What exact Windows host interface can invoke a skill/worker, and how are filesystem/network capabilities sandboxed per worker?
- What is the trusted source/signature policy for upstream skill/dependency candidates, and what retention/ACL applies to receipts and reviewer data?

Status: DONE_WITH_CONCERNS
Summary: Review hoàn tất với 9 findings (7 High, 2 Medium, đếm theo SEC-01 đến SEC-09); report chỉ đọc và không sửa sáu plan files.
Concerns/Blockers: SEC-01–SEC-07 nên được adjudicate trước implementation; chưa có live/provider/package evidence.
