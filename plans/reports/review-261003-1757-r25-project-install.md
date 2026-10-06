# Review cài đặt r25 trong dự án

Thời điểm kiểm tra: 2026-10-03T11:05:34.321151+00:00 (UTC; Asia/Saigon = UTC+07:00).

## Kết luận trong phạm vi

PASS cho cập nhật cục bộ codex-desktop, project, copy, balanced. Không phát hiện sai lệch trong các điều kiện cài đặt được giao. Không chạy lại installer, package build, full tests, model, provider hoặc UI. Chỉ đọc dữ liệu hiện tại và tạo báo cáo này.

## Các điều kiện kiểm tra

| Điều kiện | Kết quả |
|---|---|
| preview | PASS |
| update | PASS |
| journal | PASS |
| target_hash | PASS |
| backup_hash | PASS |
| source_tree_hash | PASS |
| identity_preserved | PASS |
| doctor | PASS |
| post_preview | PASS |
| candidate_lineage | PASS |
| candidate_receipt | PASS |
| binding_cursor | PASS |
| binding_agy | PASS |
| binding_codex | PASS |

Install ID giữ nguyên: `d5811d724fe29cb5016c7c3a`. Transaction: `7f2ef90a08ad4fd6b3d44b79a739f5ba`, committed; một thay đổi đã written. Preview 1 replace nckh-visuals / 42 unchanged, 0 conflict; update exit 0, installed; doctor 43 current; post-preview 43 unchanged, 0 conflict. Ba biên nhận binding từ bước kiểm tra bản đã cài có integrity-verified và hash binding khớp tệp gốc.

Hash thư mục hiện tại và nguồn candidate: `fe0403204d22a2aa5e5b1dc587bd959cbb340d7784109e359c8de3eccc5116e0`. Hash backup: `926c745ec2c504abf67aeccd9b0591bf82f57422f90fbd47f6c24b4e59b0b43f`; đường dẫn backup: `C:/Users/USER\Downloads\test-skill\.nckh-state\transactions\7f2ef90a08ad4fd6b3d44b79a739f5ba\backup-34`. Cách tính theo tree_hash tại nckh-kit/core/install.py:26 và digest_record tại nckh-kit/core/paths.py:24: SHA256 của danh sách path/sha256 sắp xếp, JSON canonical. Candidate receipt hash khớp evidence; manifest canonical hash, closure và source-lock hash khớp provenance. Đây là kiểm tra lineage và integrity, không chạy lại các phép thử được receipt mô tả.

## Các cổng độc lập

| Cổng | Trạng thái thực tế |
|---|---|
| Cài đặt và ownership cục bộ | PASS |
| Candidate deterministic evidence/lineage | PASS trong phạm vi receipt đã xác minh |
| Binding integrity | PASS; không xác thực thực thi hay cấp quyền |
| Native smoke và model/effort thực tế | not-run / unknown / applied unverified |
| Hook enforcement | unverified |
| Native open/render, editability, accessibility, ý nghĩa khoa học | Chưa được chứng minh bởi cài đặt |
| Owner acceptance | pending-personal-review |

Model trong policy native là inherit, effective unknown; không suy ra GPT 6.1 Sol, Grok 4.7 Extra High hay Gemini 3.8 Flash High đã được các IDE chạy từ biên nhận cài đặt.

## Giới hạn chẩn đoán khóa

Receipt 10:58:57 UTC khai báo controller-escalated: READ_ATTRIBUTES và DELETE open thành công; Restart Manager start/register/get_list/end đều 0, 21 tài nguyên tệp, danh sách process rỗng. Điều này cùng việc update thành công sau khi người dùng đóng Cursor hỗ trợ kết luận trở ngại đổi tên đã hết tại lần chạy này. Không đủ bằng chứng để khẳng định Cursor là nguyên nhân duy nhất hoặc loại trừ mọi directory handle/filter; context do caller khai báo, token không được đối chiếu.

## Hash biên nhận và nguồn đã đọc

| Tệp dự án | SHA256 bytes |
|---|---|
| `plans/evaluation/personal-use/install-r25-after-cursor-close-01/preview/stdout.json` | `20dca8797239cc91b6d1f83b391fc7f0589e3d41af92afb20fded3ec5df13709` |
| `plans/evaluation/personal-use/install-r25-after-cursor-close-01/preview/command-receipt.json` | `e4932a7c794915c021c1521f500282dde35afeef30fc54b52f9a30c4a1de860b` |
| `plans/evaluation/personal-use/install-r25-after-cursor-close-01/update/stdout.json` | `8dd22cfc42fc2b078b610b242f91b6e6cd2d5dc148fc392043800fdc0b6b0847` |
| `plans/evaluation/personal-use/install-r25-after-cursor-close-01/update/command-receipt.json` | `891c5c9c7ce75d3b32f01a7b7ef2d055c969241f53663b7b9f577ddcaa2b8c7e` |
| `plans/evaluation/personal-use/install-r25-after-cursor-close-01/doctor.json` | `d8c9603132357766edd7a796ac7523c715fa5ab43f82f8eb7fb9472069180170` |
| `plans/evaluation/personal-use/install-r25-after-cursor-close-01/post-preview/stdout.json` | `65b5f78a8f80ab5468dccf24289e48a37e7666dc0d50fec657f127a84a52aae1` |
| `plans/evaluation/personal-use/install-r25-after-cursor-close-01/binding-cursor.json` | `23367ac20cd82b2aac01887c0bff4ffa0ad1e3508df5ef759d50f57dc6350da7` |
| `plans/evaluation/personal-use/install-r25-after-cursor-close-01/binding-agy.json` | `be0de3de6f78b42d85ae300531dabd40f66cc3dc04dba9b218bce0405789cb66` |
| `plans/evaluation/personal-use/install-r25-after-cursor-close-01/binding-codex.json` | `90a0cbf5cdbd58abc30c12abe3c5e2420eeaf2222145058f46d1efd30975eb92` |
| `.nckh-state/journal.json` | `a667b3d4740759aa593f7b41db5faa68ca67da45b248be58dc9cf7a1e5821fba` |
| `.nckh-state/ownership.json` | `4751266952d2c7fd6bd406900f51437a5c3cfc9895038933ff7b66f672f8b3c8` |
| `plans/evaluation/personal-use/candidate-r25-attempt-02/candidate-evidence.json` | `44a052b935d05b442ad0f3b8cd538ad5ed096fe2a8557afa0edbbe0355b7f300` |
| `plans/evaluation/personal-use/candidate-r25-attempt-02/candidate-check-receipt.json` | `7412566bd53220e9770e9532d8ef6f59005e27d8cc7429cab630fcbf21621798` |
| `plans/evaluation/personal-use/candidate-r25-attempt-02/bundles/on/codex/manifest.json` | `eb541b93aacb1f10baf7bb5bc6f3eabf448d5fcece04bbcf34d48c9601be013e` |
| `plans/evaluation/personal-use/candidate-r25-attempt-02/bundles/on/codex/source-lock.json` | `570458f6d49e0653b72bedd6819afccf88a3b612ce3f5fa7d55202784db68cf4` |
| `plans/evaluation/personal-use/diagnose-r25-20261003-105857-20649ab6.json` | `ce152c91a2edfe789deda3d012b50b8d963604d5aeb4da3406d52e76209dd648` |

## Vấn đề cần xử lý

Không có finding chặn cài đặt trong phạm vi kiểm tra. Các cổng native/owner giữ nguyên trạng thái chưa xác minh; báo cáo không chấp nhận thay người dùng.
