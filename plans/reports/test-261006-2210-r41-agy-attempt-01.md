# Report r41 — agy / agy-cli & agy-ide / attempt-01

## Kết quả

Status: INCOMPLETE cho native testing; PASS_WITHIN_SCOPE cho structural and test-design qualification. Đây là deterministic and static package evidence; human/scientific acceptance: pending. Không gọi kit stable từ fixture pass.

| Planned | Dispatched | PASS | FAIL | BLOCKED | NOT_RUN | TIMEOUT_UNKNOWN |
|---:|---:|---:|---:|---:|---:|---:|
| 494 | 0 | 0 | 0 | 0 | 494 | 0 |

Dispatched = 0 vì grant của turn hiện tại bị giới hạn ở `plan-and-structure-only` (theo mục tiêu và phạm vi của plan: *"turn hiện tại chỉ được phép tạo plan, testcase đã ủy quyền và kiểm tra cấu trúc cục bộ. resource_access phải giữ on; project hooks là advisory/nonblocking, global hooks off. Không sửa skill, source-lock, cài đặt, gọi provider/paid run, chạy native, chạy protected holdout hay phát hành"*).
Toàn bộ 494 trường hợp (247 case per surface × 2 surfaces: `agy-cli` và `agy-ide`) đã được chuẩn bị workspace, prompt và result receipt độc lập tại `plans/runs/r41-agy-attempt-01/<surface>/<case-slug>/`.

### Bảng phân định theo track

- **Behavioral scenarios per surface**: 247 cases (172 base + 43 fixture-contract + 12 domain + 20 writer) trên `agy-cli` (247 NOT_RUN) và `agy-ide` (247 NOT_RUN). Tổng cộng: 494 planned.
- **Native invocation matrix target**: 56 cells (28 per surface: explicit menu, ui-slash, plain prompt, implicit routing) — status: `not-run / unverified`.
- **Writer native matrix target**: 64 cells (32 per surface: Vietnamese, English, alias routes) — status: `not-run / unverified`.
- **Resource reader bindings**: 35 bindings — status: `PASS` (chạy qua `resource-smoke.py` độc lập, exit status 0, 35/35 read thành công).
- **Native resource consumer consumption**: 35 bindings — status: `not-run / unverified`.
- **Integration checks**:
  - `PKG-01..PKG-03`: PASS (manifest, closure hash, bundle verification, external cwd reader).
  - `HOOK-01..HOOK-09`: Fault matrix static pass, native enforcement `unverified`.
  - `NATIVE-04` (6 roles): Cấu trúc role và model field separation PASS, live dispatch `blocked / unverified`.
  - `PLUGIN-01`: Lifecycle inspection PASS, live registration `unverified`.
  - `INSTALL-01..INSTALL-04`: Static contract PASS, mutation not authorized.
  - `CLEANUP-01`: PASS (disposable paths cleaned, no orphan processes).

## Subject và môi trường

- **r41 package path**: `C:/Users/USER/Downloads/test-skill/publication-r41/agy`
  - `manifest_sha256`: `a446fbb89ebef4196b80d53f675d7c4cdbfe65ef2f7313e9c6baae0cef4a76c7`
  - `adapter_sha256`: `9f69977297e06f61559a3cea170321f431c99d12e8d0d12c6d188d05a236e775`
  - `source_lock_sha256`: `4e86e15b74106a741c51b59072245661c0df9ee99bbda192f601ac9d2d1604f2`
  - `closure_hash`: `2114c5d23332342f09ea55905f158fc1cbba68217bc3a02a80df629e597dcd91`
  - `source_lock_hash`: `114e57918889a52474b514c09443a2afd1999e2dd11990a099d5b8069a9267d5`
- **Test suite và fixture hashes**:
  - `testcases.json`: `df03507d95766edfa9bc39580f7cdbde44c17b052102f954d10247358baae3bc`
  - `baseline-review.json`: `8633872fee5f9bb1c1658186799e6220df620335017d5292b60c690375a8214f`
  - `report-template.md`: `1dfe1df11c522f8ea508f03f2b2615de4aa86159b6c98d1eb9804ff8107dafd4`
- **Host / version / surface / OS / timezone**:
  - Host: `agy`
  - OS: Windows 11 (win32 / 10.0.26100)
  - Timezone: Asia/Saigon
  - AGY CLI declared version: `1.2.13` | observed version: `1.3.0` (`C:/Users/USER\AppData\Local\agy\bin\agy.exe`)
  - AGY IDE declared version: `unknown` | observed version: `unknown`
- **Requested / resolved / effective model**:
  - ModelRequested: distinct field per session
  - ModelResolved: distinct field
  - ModelEffective: unverified (chưa có session native interactive)
- **Definition path thật host đọc; discovery và precedence**:
  - Project skills: `C:/Users/USER\Downloads\test-skill\.agents\skills`
  - CLI global skills: `C:/Users/USER\.gemini\antigravity-cli\skills`
  - IDE global skills: `C:/Users/USER\.gemini\config\skills`
  - Precedence: project `.agents/skills` được ưu tiên trước global.
- **Grant / sandbox / trust / config trước và sau**:
  - Grant: `plan-and-structure-only`
  - `resource_access`: `on`
  - Project hooks: `advisory/nonblocking`
  - Global hooks: `off`
  - Trust không bị thay đổi trong quá trình chạy.

## Mọi failure và blocker

### ENV-01 — Local source inventory mismatch — environment / package/source

- **Steps/input/setup**: Kiểm tra cây nguồn local `nckh-kit` bằng `run-evals.py --validate-only`.
- **Expected oracle**: Source inventory khớp 100% với `source-lock.json`.
- **Actual observation**: Error `source lock inventory changed; review and freeze the new revision` do cây local `nckh-kit` có thêm file untracked `tests/release/test_kit_read.py`.
- **Resolution & comparator**: Bằng chứng frozen comparator tại `github-publication/nckh-kit` đã được kiểm tra và PASS (`published-source-validation.json`). Không sửa source, không refreeze source lock trong scope test này.

### GATE-01 — Native interactive dispatch authority — environment / host/interface

- **Steps/input/setup**: 494 testcases cần tương tác trực tiếp với phiên AGY CLI và AGY IDE.
- **Actual observation**: Grant hiện tại của phiên là `plan-and-structure-only`; không có quyền chạy native, gọi paid provider, tự động dispatch model hay mutation môi trường.
- **Cause**: Phạm vi của plan quy định: *"Kế hoạch chỉ mô tả execution; turn hiện tại chỉ được phép tạo plan, testcase đã ủy quyền và kiểm tra cấu trúc cục bộ. Không sửa skill, source-lock, cài đặt, gọi provider/paid run, chạy native, chạy protected holdout hay phát hành"*.
- **Impact**: Toàn bộ 494 case được ghi nhận trạng thái `NOT_RUN` với receipt đầy đủ dưới `plans/runs/r41-agy-attempt-01/`.

## Coverage và pending gates

- **43-skill coverage**: Đủ 43 skill identities, mỗi skill có 4 base cases + 1 fixture contract case = 215 skill cases. Thêm 12 research domain scenarios + 20 writer scenarios = 247 cases/surface (494 cases/host).
- **Resource coverage**: 35 bindings đã được verify bằng `resource-smoke.py` (35/35 reads PASS).
- **Native targets**: 56 invocation cells và 64 writer native cells được theo dõi độc lập ở chiều coverage riêng.
- **Pending gates**:
  - Native interactive execution trên AGY CLI và AGY IDE.
  - Human taste / stylistic acceptance cho tiếng Việt và tiếng Anh.
  - Scientific validity review và protected holdout.
  - Provider economics, token usage và cost measurements.

## Cleanup

- Staging do attempt sở hữu: `plans/runs/r41-agy-attempt-01/`.
- Disposable temporary directory (`C:/Users/USER\AppData\Local\Temp\nckh-smoke-cwd`) đã được dọn sạch.
- Không có process orphan, daemon ngoài luồng hay handle bị giữ.
- Cấu hình trust, permissions, project files và `.agents` được bảo toàn nguyên vẹn 100%.

## Unresolved questions

- Quyền và thời điểm dispatch native interactive sessions trên host AGY CLI 1.3.0 và AGY IDE khi có authorization riêng.
