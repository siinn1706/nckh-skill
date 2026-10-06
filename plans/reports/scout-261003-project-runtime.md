# Scout nguồn và runtime dự án NCKH

Ngày: 2026-10-03, Asia/Saigon. Phạm vi: chỉ đọc nguồn/metadata/trợ giúp lệnh; không chạy prompt/model, không đăng nhập, không đọc credentials, không sửa cài đặt hay cấu hình toàn cục. Báo cáo là ảnh chụp lúc scout; source có thể đổi khi controller triển khai.

## 1. Trạng thái xác định được

| Hạng mục | Quan sát |
|---|---|
| Source hiện tại | `nckh-kit/core/registry/source-lock/source-lock.json`, revision `22`, 215 source pins |
| Hash lock theo canonical record | `5aa333170906f909a374f256a7093702a399f9038421856bd7589066a0a6917d`, đối chiếu `plans/evaluation/resource-quality/final-freeze.json` |
| Hash bytes của file lock | `66e3a07e8a6d3a14051d99e779942a5ca0ec74bfe7db380a70a0f7b05aaf2bb2`, đọc trực tiếp trong scout |
| Installed ownership | `.nckh-state/ownership.json`: install ID `d5811d724fe29cb5016c7c3a`, `codex-desktop`, project scope, copy, core/engineer/marketing, 37 skill folders + 6 native agent files |
| Installed source identity | Revision 14 lock `2c98d9edad4db63b1b3b8db620d947e6e9e5182ddbfa24ede5a90d27ea6fde03`; closure `3715cf7f083aac9f8d458a3cabd8018ba33c4e3e039c388ed41c8ec9da187a5a` |
| Installed roots | `C:/Users/USER/Downloads/test-skill/.agents/skills` và `.codex/agents`; không có Cursor/Antigravity install identity trong ownership hiện tại |
| Build lịch sử r22 | `nckh-kit/dist-resource-quality-r22/on` và `/off`; receipts trong `plans/evaluation/resource-quality/verification-artifacts-r22.json` |
| Qualification lịch sử | `final-freeze.json` giữ 147 pass/1 fail/0 pending của exposed development subject r14; package/native r22 chưa chạy; không dùng để chứng nhận source sửa sau r22 |

Không đọc nội dung credential/config riêng của host. Không bắt đầu hoặc dừng các tiến trình IDE đã có của người dùng.

## 2. Source/resource owners chính xác

| Contract/flow | File và symbol sở hữu | Caller/kiểm tra liên quan |
|---|---|---|
| Resource declaration | `nckh-kit/core/registry/catalog/resources.json` | `core/resources.py:15 registry()` đọc và validate `resource-registry` |
| Resource schema, quyền và provenance | `core/contracts/resource-registry.schema.json`, `resource-provenance.schema.json`; `core/resources.py:77 resource_provenance()`, `:96 verify_provenance()` | `core/build.py:60 freeze_sources()`, `:90 verify_source_lock()`, `:344 verify_bundle()` |
| Resource members/closure | `core/resources.py:63 resource_members()`, `:68 resource_edges()` | `core/build.py:41 source_members()`, `:137 closure()`, `:218 _materialize_host()` |
| Consumer thực đọc bytes | `scripts/search-resource.py:39 lookup()` | `main():120`; bốn nhánh resource ID cố định; kiểm hash bytes/licence/notice trước output |
| Portability observation | `scripts/resource-smoke.py:25 smoke()` | `tests/resource/test_extracted_smoke.py:19` kiểm reader sau extraction ngoài repo bằng isolated Python |
| Reader behavior tests | `tests/resource/test_consumers.py` | UI lookup, reporting applicability, publisher warnings, consumer/locale/genre mismatch, Nature advice, off không đọc |
| Closure/rights tests | `tests/resource/test_closure.py` | Unlisted data, rights/hash drift, dependency cycles/private paths, v2 shared verifier, on/off cùng source |
| Source cards và evidence | `core/contracts/source.schema.json`, `evidence.schema.json`; `core/guards.py:33 check_claim_bundle()` | Source supports owned/cleared/read-only/unknown, metadata/abstract/full-text/user-supplied, edition/translator; bindings không chứng nhận semantic support |

### Resources đã tồn tại

| ID | Bytes | Consumers | Output |
|---|---|---|---|
| `R-reporting-lookup` | `core/profiles/resources/reporting-guidelines.json` | `nckh-method`, `nckh-write` | Reporting selection theo clinical/health design; không áp vào CS mặc định |
| `R-publisher-profile` | `core/profiles/resources/publisher-profiles.json` | `nckh-visuals` | Profile snapshot, yêu cầu venue/year/track/article-type/stage; exact applicability chưa xác nhận |
| `R-ui-lookup` | `core/profiles/resources/ux-guidelines.csv` | `nckh-frontend` | Bounded UI findings theo query; code examples là dữ liệu |
| `R-nature-reference` | `core/profiles/resources/english-writing-advice.md` | `nckh-write`, `nckh-taste` | English advice fragment; không phải prose corpus/human gold |

Consumer references nằm ở `skills/core/nckh-write/references/resource-lookup.md`, `skills/core/nckh-taste/references/resource-lookup.md`, các reference tương ứng của method/visuals/frontend. Catalog skill paths ở `core/registry/catalog/skills.json`: `skills/core/nckh-research`, `nckh-method`, `nckh-write`, `nckh-taste`, `nckh-visuals`.

### Giới hạn cần tính đến khi thêm source pack thật

Registry hiện chỉ chấp nhận `locale: en`, `source_kind: copied-upstream`, `copied_vs_reauthored: verbatim-upstream`, MIT/Apache-2.0, commit upstream đủ 40 ký tự và redistribution `permitted-with-notices`. `core/resources.registry()` lặp lại các kiểm tra commit/hash/member; reader `lookup()` chỉ có bốn ID nêu trên. Vì vậy corpus VI, owner-supplied hoặc public-domain không thể được thêm bằng một row JSON rồi tuyên bố đã có consumer. Cần contract và reader khớp loại nguồn thực, consumer reference, artifact output và test của loại nguồn đó. Scout không chọn architecture thay controller.

`source_members()` tự include các file `.md/.json/.yaml/.toml/.py/.ps1/.sh` trong source areas; CSV/JSONL/SVG cần resource declaration. `core/profiles/resources/` từ chối mọi file chưa đăng ký. Evaluation/private material không được đóng gói qua namespace này.

## 3. Acceptance/profile owners

| Nhu cầu | Owner hiện tại |
|---|---|
| Required gates và phạm vi | `core/policies/acceptance-policy.md` |
| Aggregate pass/fail/pending gắn revision | `core/state.py:66 aggregate()`; không có required gate => pending; required fail => failed |
| Invalidation và quyết định owner | `core/state.py:79 invalidate()`, `:104 review_boundary()`, `:117 feedback()` |
| Human/scientific protocol lịch sử | `evals/protocols/qualification.json`; `core/evaluation.py:59 validate_protocol()`, `:127 development_round()` |
| VI/EN style | `core/profiles/style/vi.md`, `en.md`; `skills/core/nckh-write/SKILL.md`, `nckh-taste/SKILL.md`, `nckh-taste/references/human-taste.md` |
| Typed receipt | `core/contracts/receipt.schema.json` |
| Installer accepted check scope | `installer/schemas/candidate-evidence.schema.json`, `check-receipt.schema.json`; `core/install.py:300 validate_candidate_evidence()` |

Hiện chưa có personal-use acceptance lane/default acceptance profile. `profile.schema.json` có kind venue/style/glossary, không phải acceptance. Protocol lịch sử vẫn yêu cầu reviewer/sample/threshold/economics freeze và giữ pending. Việc người dùng tự chấm cuối và loại external reviewers khỏi delivery blockers phải được thể hiện bằng lane mới có scope cụ thể; không sửa verdict/receipt lịch sử thành pass. Model critique vẫn không được ghi thành human labels.

## 4. Runtime đã quan sát

### Controller supplied live UI observations

Controller xác nhận Computer Use đã đọc:

- Cursor Agents: project `test-skill`, `This PC`, model button `Grok 4.7 Extra High`.
- Antigravity: project `test-skill`, `Local`, model button `Gemini 3.8 Flash High`.

Đây là configured UI labels. Không suy ra provider ID, resolved/effective model, effective effort hay completed test. Controller cho biết desktop ChatGPT automation bị Computer Use skill cấm; browser route có thể dùng nếu có tab phù hợp. Scout không thao tác UI.

### Local tooling observations

| Route | Quan sát trực tiếp | Khả năng và điều kiện |
|---|---|---|
| Cursor IDE | `Cursor.exe` metadata 3.23.12; có các tiến trình Cursor đang mở | Controller có live UI access; chưa có native test receipt |
| Cursor Agent CLI | `C:/Users/USER/AppData/Local/cursor-agent/versions/2026.09.15-d2fe57e/node.exe` + `index.js`; `--version` trả `2026.09.15-d2fe57e`; `--help` exit 0 | Literal executable/JS bridge có thể pin. Help có `--workspace`, `--model`, `--print`, `--output-format json/stream-json`, `--sandbox enabled`, `--auto-review`; parameterized model ví dụ `[effort=high]` không chứng minh ID Grok hoặc effort Extra High |
| Cursor CLI catalogue | `--list-models` exit 1, `Authentication required` | Chưa có CLI account inventory/ID. Không login, đọc token hay dùng API key. UI label không bị phủ định bởi CLI auth thiếu |
| Antigravity IDE | `Antigravity.exe` metadata 2.19.1/2.19.1.0; processes đang mở | Controller có live UI access; requested label được configured trong UI |
| Antigravity CLI | `Get-Command antigravity` không có; package chỉ inventory thấy `resources/app.asar`, `resources/bin/language_server.exe`, `webm_encoder.exe` | Chưa chứng minh native CLI route. Không dùng language server làm giả CLI |
| Google Gemini CLI | `gemini.ps1` trỏ `@google/gemini-cli/bundle/gemini.js` | Route khác Antigravity. Direct Node `--help` exit 1 `Failed to relaunch... spawn EPERM`; không retry elevation, không run prompt |
| ChatGPT | Không có `ChatGPT` command; processes `ChatGPT.exe` thuộc `OpenAI.Codex_26.930.2377.0` | Tên process không phải ChatGPT model catalogue. `@ChatGPT all models` cần snapshot picker/account scope thực qua route được phép |
| Codex CLI | Có `codex.ps1`, native Codex binaries/processes | Không thay thế target ChatGPT; không dùng như fallback cho yêu cầu all ChatGPT models |
| Python | `Python312/python.exe`, tooling cục bộ giúp build/install | Reader và installer `--help` exit 0; installer chỉ có 8 surfaces hiện tại |

Không gọi Cursor force/yolo/trust/approve-mcps, không gọi status/whoami/login, không chạy models/provider prompt.

## 5. Runner/build/install owners và bước cụ thể khả thi

### Runner

`evals/run-evals.py:18 main()` có validate/deterministic/prepare-agent/run-agent. `core/agent_runs.py:54 prepare_agent_run()` kiểm closed recipe, exact executable/bridge/interface hashes, source/cases/freeze; `:173 run_agent_cases()` dispatch qua `core/processes.run_owned_command()`.

Các surfaces lấy từ `core/install.py:22 SURFACE_HOST`: claude-code, codex desktop/cli/ide, cursor ide/cli, agy ide/cli. **ChatGPT chưa có surface/binding**. Existing generic runner không tự điều khiển UI; explicit native executable/bridge vẫn phải được quan sát. Raw store phải ngoài `nckh-kit`, project root và workspace; mỗi case 1–900 giây, rounds 1–3, sáu freeze refs; exit 0 chỉ completed-unreviewed.

`plans/evaluation/direct-skill-tests/run-native-suite.py` là harness lịch sử riêng: hardcode old Codex executable, version 0.159.2 và config hints gpt-6.1-sol/max, private store nằm trong project. Không dùng nó để chứng nhận Cursor/ChatGPT/Antigravity hay source mới. `append-controller-review.py` và `summarize-development-results.py` thuộc historical direct lane; giữ originals.

### Build/source freeze

1. Sau khi source/consumer/profile edits được review: `scripts/freeze-source-lock.py --write` gọi `core/build.freeze_sources()`; tự archive lock cũ và tăng revision nếu bytes/inspiration đổi. Không sửa hash r22 để reuse pass.
2. `scripts/build-artifacts.py --all --check` hoặc `--all --plugin --check` kiểm hai isolated builds; `--output` cần root chưa có hoặc rỗng. Host choices claude/codex/cursor/agy; không có ChatGPT build target.
3. Dùng output mới mang source revision, giữ `dist` r14 và `dist-resource-quality-r22` nguyên. Registry/closure/on-off wiring đã có sẵn; thêm reader smoke cases cho source pack thực trước khi gọi packaging accepted.
4. `scripts/resource-smoke.py --bundle EXTRACTED --cwd OUTSIDE --unset-pythonpath --output RECEIPT` là portable read check; không chứng nhận model quality.

### Project installation/update

Entrypoint `installer/nckh-installer.py:37 main()`; target resolution `core/install.py:61 resolve_targets()`, transaction preview `:124 plan_install()`, candidate receipts `:300 validate_candidate_evidence()`, doctor tại cùng engine. `install` không promote changed owned files. Existing `codex-desktop` target phải dùng `update --package NEW_BUILD_ROOT --runtime codex-desktop --scope project --project C:/Users/USER/Downloads/test-skill --kits core engineer marketing --mode copy --models balanced --candidate-evidence EXACT_RECEIPT --dry-run`; `--with-agents` scope inherited từ existing ownership. Sau khi review preview và user authority khớp, `--yes` commit không bypass edit conflicts.

Cursor chưa có ownership: `install --package NEW_BUILD_ROOT --runtime cursor-ide --scope project --project ... --kits core engineer marketing --mode copy --models balanced --dry-run` là tuyến preview hợp lệ. CLI/IDE surfaces khác nhau; không ghi cả hai đã qualified chỉ vì chung bytes.

Antigravity IDE và Codex cùng dùng project `.agents/skills`. `plan_install():166–171` yêu cầu actual neutral/dedup qualification khi thêm visible surface vào shared physical path; differing projections hoặc shared owners khác hash bị reject trước write. Do đó không giả `qualified_neutral_consumers` để thêm agy ownership. Cần quan sát route thực hoặc preview/scope phù hợp do controller quyết định. Cursor dùng `.cursor/skills` riêng.

`config-models` chỉ native agent files, cần observed per-host mappings, không thay parent/session model. `core/native.encode_agent()` chỉ hỗ trợ Antigravity aliases inherit/flash/pro và reject effort; UI Gemini 3.8 Flash High của main agent không chứng minh subagent effort override. Cursor encoder ghi bracket effort nhưng exact model ID/eligibility vẫn cần observed mapping.

## 6. Còn thiếu cho mục tiêu đích

- CLI account catalogue và ID/effort binding cho Grok 4.7 Extra High; UI configured label đã quan sát.
- ChatGPT picker/model snapshot toàn bộ tài khoản và browser/native route được phép; hiện kit không có ChatGPT surface.
- Antigravity main-agent native run receipt và effective telemetry; không có callable CLI được scout xác nhận.
- New personal-use lane source/profile/schema/runner wiring, owner final scoring event gắn revision/artifact; không reuse external-review gate lịch sử.
- Current new source freeze/build/check receipts và project transaction preview; r14/r22 receipts chỉ chứng nhận subject lịch sử tương ứng.

Status: DONE_WITH_CONCERNS
Summary: Đã xác định source/resource/acceptance/build/installer/runner owners và local runtime routes; controller UI labels được giữ riêng khỏi effective model evidence.
Concerns/Blockers: Cursor CLI cần auth riêng; ChatGPT chưa có surface; Antigravity CLI chưa xác nhận; source-pack registry hiện EN copied-upstream-only; shared `.agents/skills` có neutral/dedup gate thật.
