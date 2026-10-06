# Rà soát tài nguyên skill: `nature-skills`, chuẩn Agent Skills và NCKH

**As-of:** 2026-10-02, Asia/Saigon. **Phạm vi:** review kiến trúc tài nguyên và kế hoạch chọn lọc; không triển khai, không cài upstream, không chạy provider.

## Kết luận

Tiền đề “skill NCKH chỉ có Markdown” chỉ đúng ở ba thư mục lõi đang so sánh: `SKILL.md` và `references/*.md` là phần hướng dẫn/routing. Toàn bộ kit NCKH không Markdown-only: đã có schema JSON, eval cases, rubric, runner và Python tests ở cấp kit. Khoảng trống chính là liên kết machine-readable giữa từng skill với input/output/gate; không phải thiếu CSV/JSON nói chung.

Khuyến nghị hạng 1: giữ `SKILL.md` mỏng và thêm tài nguyên chỉ khi có consumer, validator và gate rõ ràng. Hạng 2: bổ sung manifest/schema cho từng skill và nối chúng vào các contract/eval hiện hữu. Hạng 3: chỉ thêm CSV cho registry dạng bảng; chỉ thêm script cho kiểm tra quyết định được; không fork/copy nguyên bundle upstream.

## Nguồn, revision và độ tin cậy

| Nguồn | Revision/as-of | Bằng chứng đã đọc | Độ tin cậy và giới hạn |
|---|---|---|---|
| NCKH local | checkout hiện tại, 2026-10-02 | `nckh-kit/docs/research-and-writing.md`; ba `SKILL.md` và refs; `core/contracts/*.schema.json`; evals/tests | Primary cho kiến trúc local; không suy ra chất lượng khoa học từ test kỹ thuật |
| Nature Skills | GitHub API xác minh `main` = `84880815fb37317b3766bff2c2abba395b8993c3` (2026-10-02); LICENSE Git blob `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64`, manifest Git blob `f0e92576c732c710e154626216f00a161ac5f54c` | router, `manifest.yaml`, installer, figure QA, CI; raw-main samples đọc trước khi chốt SHA | Primary upstream; Git blob IDs không phải SHA-256; không coi crawl là release bất biến |
| Agent Skills spec | `https://agentskills.io/specification` | metadata, optional `scripts/`, `references/`, `assets/`, progressive disclosure, validator | Primary specification; không quy định chất lượng hành vi |
| Anthropic skills | `main`, 2026-10-02 | README, `skill-creator`, life-sciences | Maintainer/official ecosystem; license và provider phải xét theo thư mục |
| K-Dense scientific skills | `main`, 2026-10-02 | README, `scientific-writing`, `LICENSE.md` | Primary maintainer repo; đóng góp/community và tài nguyên bên thứ ba cần audit riêng |

Revision caveat: tại SHA đầy đủ đã xác minh, `LICENSE` là Apache-2.0; một snapshot lịch sử `86398bb` từng trả về MIT và nội dung cũ. Vì vậy mọi reuse phải pin full SHA, lưu Git object/hash đã quan sát và kiểm tra lại LICENSE/NOTICE theo đúng SHA; không dùng một nhãn license tổng quát cho mọi file.

## Mẫu tài nguyên đại diện

| Loại | Ví dụ và ý nghĩa |
|---|---|
| Markdown router/instruction | [`nature-writing/SKILL.md`](https://raw.githubusercontent.com/Yuan1z0825/nature-skills/84880815fb37317b3766bff2c2abba395b8993c3/skills/nature-writing/SKILL.md) chỉ định đọc manifest, always-load core và refs theo điều kiện; đây là procedural guidance, không phải dữ liệu huấn luyện |
| Manifest/config | [`nature-writing/manifest.yaml`](https://raw.githubusercontent.com/Yuan1z0825/nature-skills/84880815fb37317b3766bff2c2abba395b8993c3/skills/nature-writing/manifest.yaml) v1.5.0 khai báo axis/path và on-demand references; cần version/hash nếu NCKH dùng pattern này |
| References/static | Manifest trỏ tới `static/core`, `static/fragments`, `references/` và `nature-shared`; progressive disclosure giảm context nhưng tạo dependency/closure cần kiểm tra |
| Script/requirements | [`update-codex-skills.sh`](https://raw.githubusercontent.com/Yuan1z0825/nature-skills/84880815fb37317b3766bff2c2abba395b8993c3/scripts/update-codex-skills.sh) sync toàn bộ thư mục và diff-check; pinned `nature-figure` listing có `validate_figure.py`, `audit_pdf_text.py`, `audit_figure_collisions.py`, `audit_panel_alignment.py` và các script figure khác |
| Assets/templates | K-Dense `scientific-writing` liệt kê và dùng các scaffold/template trong [`SKILL.md`](https://raw.githubusercontent.com/K-Dense-AI/scientific-agent-skills/main/skills/scientific-writing/SKILL.md); ví dụ [`claim_evidence_template.csv`](https://raw.githubusercontent.com/K-Dense-AI/scientific-agent-skills/main/skills/scientific-writing/assets/claim_evidence_template.csv) và [`source_manifest_template.json`](https://raw.githubusercontent.com/K-Dense-AI/scientific-agent-skills/main/skills/scientific-writing/assets/source_manifest_template.json). Không suy rộng thành quyền dùng figure/font/PPTX bên thứ ba |
| CSV/JSON | K-Dense có claim/evidence CSV và source-manifest JSON cụ thể ở trên; [`evidence_workflow.md`](https://raw.githubusercontent.com/K-Dense-AI/scientific-agent-skills/main/skills/scientific-writing/references/evidence_workflow.md) mô tả liên kết `E`/`C`, hash claim và human verification. JSON phù hợp contract/receipt; CSV phù hợp bảng claim/source/review, không phù hợp prose |
| Tests/evals | Nature có CI/self-tests; [Anthropic `skill-creator/SKILL.md`](https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md) yêu cầu vòng test with-skill/baseline và lưu `evals/evals.json`; [schemas.md](https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/references/schemas.md) định nghĩa JSON. Objective checks có thể script, taste/writing vẫn cần human review |

Official spec xác nhận chỉ `SKILL.md` là bắt buộc; `scripts/`, `references/`, `assets/` và file bổ sung là optional. Do đó Markdown-first của NCKH hiện tại là compliant, không phải thiếu chuẩn.

## Đối chiếu trade-off và adoption risk

| Lựa chọn | Performance/traceability | Complexity/maintenance | Cost/adoption risk | Fit với NCKH |
|---|---|---|---|---|
| Nature Skills | Router + manifest + scripts/QA mạnh; output phụ thuộc closure | Cao: static/shared/ref/provider, upstream đổi nhanh | License snapshot bất nhất; third-party assets; maturity không đồng nghĩa scientific validity | Tốt để mượn pattern, kém nếu copy nguyên bundle |
| Official spec + Anthropic | Progressive disclosure, eval discipline, separation human vs script | Vừa; cần tự xây contract/runner | Mixed licensing (một số thư mục source-available), external MCP/credentials | Tốt làm baseline governance và eval |
| K-Dense | Resource-rich, claim/evidence, scripts/tests, templates | Cao: nhiều skill, registry/community và dependency | MIT root nhưng contribution/asset rights phải kiểm riêng; review depth không đồng đều | Tốt để chọn riêng evidence/claim patterns |
| NCKH hiện tại | Core MD rõ; kit có contracts/evals/tests; 37 skill identities đã có development corpus 148 case | Thấp-vừa; thiếu direct per-skill manifest/validator | Latest development view 147 pass/1 fail, nhưng không có matched baseline, holdout hay human/domain gold | Fit cao nếu nối contract hiện có, không tạo kho tài nguyên lớn |

Local evidence: development corpus `plans/evaluation/direct-skill-tests/development-corpus.json` có 37 identities × 4 = 148 case; report ngày 2026-10-02 ghi latest 147 pass/1 fail. Đây là exposed development evaluation; không phải human acceptance, scientific validity, blind routing hay no-skill baseline.

## Kế hoạch chọn lọc cho NCKH

1. **Giữ cấu trúc:** `SKILL.md` chỉ giữ trigger, workflow, boundaries và output contract ngắn; hướng dẫn dài đưa vào `references/*.md` theo progressive disclosure.
2. **Nối contract trước khi thêm file:** mỗi skill có manifest nhỏ hoặc bảng mapping tới schema `brief/claim/evidence/source/receipt`; bắt buộc version, source hash, locator, status và human-gate state khi output machine-consumed.
3. **Script có điều kiện:** chỉ thêm validator deterministic cho invariant có thể kiểm được (schema, hash, locator, format, collision); không script hóa taste, scientific validity hoặc approval. Mọi network/provider action phải explicit và gated.
4. **CSV có lý do:** dùng cho claim/evidence rows, source inventory hoặc review extraction có schema/header/version; không dùng CSV làm knowledge dump hay thay cho Markdown rationale.
5. **Eval tái sử dụng corpus hiện hữu:** nối 148 development cases vào từng skill contract; giữ synthetic inputs, human gold, holdout, matched baseline và live/provider evidence là các tầng riêng. Không tạo lại corpus chỉ để bắt chước upstream.
6. **Acceptance gates:** thêm per-skill direct tests, malformed/negative cases, provenance/rights checks và human review queue; pass validator chỉ chứng minh cấu trúc/invariant.
7. **Release/licensing:** pin upstream SHA, lưu LICENSE/NOTICE/third-party inventory; clean-room reimplement ý tưởng mặc định, chỉ copy code/asset sau khi clearance từng file.

## Unknowns và giới hạn

- Chưa có benchmark matched no-skill/upstream, protected holdout, human/domain taste gold hoặc acceptance cho output khoa học Việt/Anh.
- Đã có full SHA `main` từ GitHub API, nhưng các URL raw `main` vẫn là đường dẫn mutable; dependency/reuse phải dùng SHA `84880815…` và re-check blob/license khi upstream thay đổi.
- Chưa audit hết mọi skill, dependency, font, figure, article excerpt, MCP/provider terms của ba hệ sinh thái.
- Không có kết luận rằng nhiều file hơn, nhiều script hơn hoặc nhiều skill hơn sẽ làm output tốt hơn.

Status: DONE_WITH_CONCERNS
Summary: Đã hoàn tất review nguồn và kế hoạch tài nguyên chọn lọc; NCKH nên nối machine-readable contracts/evals hiện hữu thay vì thêm file theo phong trào.
Concerns/Blockers: License/revision của upstream có snapshot mâu thuẫn; cần pin full SHA và clearance từng resource trước reuse, còn chất lượng hành vi/human acceptance vẫn chưa được chứng minh.
