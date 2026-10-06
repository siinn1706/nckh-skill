# Rà soát sửa đổi tích hợp r29

Status: source review complete; full deterministic and local packaged delivery PASS.

Controller `/root` dùng `ak-code-review` và acceptance của plan
`261004-0047-nckh-research-data-hooks-writing`. Bản r27 đã được review riêng tại
[checkpoint trước freeze](review-261004-1037-pre-freeze.md); record đó giữ nguyên.
Không có Git checkout, nên phạm vi bổ sung lấy từ source-lock history và
[delta r27/r28 → r29](../runs/nckh-writing-hooks-261004-1037-attempt-03/review-delta.json).

## Phạm vi và kết quả

| File thay đổi sau r27 | Vấn đề đã quan sát / sửa đổi | Evidence và giới hạn |
|---|---|---|
| `core/build.py` | Promotion staging gặp Windows access/sharing conflict; retry tối đa 6 lần cho staging owned, cùng parent và destination chưa tồn tại. Mỗi lần kiểm lại no-links và trạng thái destination. | Không đổi ACL, không overwrite destination xuất hiện đồng thời. Nguyên nhân holder của lỗi r27 chưa được xác định. |
| `tests/build/test_closure.py` | Kiểm retry sau lỗi sharing và preserve destination đã có. | Test có lỗi filesystem giả lập để kiểm nhánh recovery; không gọi đây là native lock/host qualification. |
| `evals/run-evals.py` | Discovery cần `-t .` để `tests/hooks` không shadow package `hooks`. | Giữ toàn bộ test pattern và failure handling; không bỏ suite hoặc nới oracle. |
| `tests/installer/test_transactions.py` | Core tăng từ 10 lên 12; failure injection tính vị trí native-agent write từ plan. Lượt r28 chọn nhầm kind `agent`; sửa về kind thực `native-agent`. | Hai regression tests trên frozen r29 (historical evidence path: `../runs/nckh-writing-hooks-261004-1037-attempt-03/installer-frozen.stderr`; unavailable in the cleaned checkout) PASS; [process receipt](../runs/nckh-writing-hooks-261004-1037-attempt-03/installer-frozen.process.json) ghi source unchanged và owned group cleanup. |

Chỉ file test installer đổi giữa r28 và r29. Không có source member bị xóa.
Writer entrypoints và linked writing policies không đổi trong các repair này;
giữ [four-case independent forward test](reviewer-261004-1037-writer-forward-test.md)
ở evidence class local agent trial. Core visual guards đã được sửa trước r27;
không suy semantic fidelity từ equality của các factual slots.

Không phát hiện defect mới trong bốn file sửa đổi được đọc.
[Full deterministic r29](../runs/nckh-writing-hooks-261004-1037-attempt-03/deterministic.json)
đã chạy 181 tests trong 806.511 giây, `OK (skipped=1)`. Một test real-symlink
giữ skip do quyền tạo symlink trên Windows; không đổi test để che limitation.
[Process receipt](../runs/nckh-writing-hooks-261004-1037-attempt-03/deterministic-frozen.process.json)
ghi source unchanged và owned process group đã đóng. [Integration record](delivery-261004-1037-r29-local-candidate.md)
đã reconcile 16 built/archive/extracted bundles, 216 actual resource reads,
48 disabled/no-read writer observations, 24 primary/reference hook projections,
8 installer previews và 509 protected hashes không đổi. Các kết quả này là local
technical evidence; native/owner/scientific gates vẫn riêng.

## Failure preservation và revision

- r27: full deterministic failure và Windows promotion failure giữ tại
  [attempt 01](../runs/nckh-writing-hooks-261004-1037-attempt-01/).
- r28: installer regression failure (historical evidence path: `../runs/nckh-writing-hooks-261004-1037-attempt-02/installer-repair-tests.log`; unavailable in the cleaned checkout)
  giữ nguyên. On standalone reproducibility/build đã chạy xong; off standalone
  reproducibility được controller dừng để sửa test và freeze revision tiếp theo.
  Không gán việc dừng có chủ đích thành lỗi chức năng của builder.
- Lần thử test trước freeze r29 bị source-lock verifier từ chối đúng vì pinned
  test bytes đã đổi: log riêng (historical evidence path: `../runs/nckh-writing-hooks-261004-1037-attempt-03/installer-repair-tests.log`; unavailable in the cleaned checkout).
  Không bypass verifier; sau freeze, cùng regression tests đã PASS.
- [Pre-freeze r29](../runs/nckh-writing-hooks-261004-1037-attempt-03/pre-freeze-state.json)
  kiểm 509 protected hashes, exact identity/case sets, 72 Python files, 25 schemas
  và 469 Markdown links. [Static evaluation r29](../runs/nckh-writing-hooks-261004-1037-attempt-03/validate.json)
  xác nhận 281 pins, 39 identities, 156 base cases, 19 families, 224 historical
  cells và supplemental writer 256 native cells/20 scenarios, vẫn unobserved.

Source-lock history giữ r26/r27/r28; `/root` là freeze owner cho r29.
Canonical source-lock hash r29:
`6fbdf13a4ba296b3e492b89beaf7fc8299c926d73a02a0ffcd9ea16a88d16248`.

## Gate còn riêng

Native deny/malformed/timeout/crash/coverage/trust phải được quan sát đúng
host/version/surface/event sau grant. Installation hiện có chưa được cập nhật.
Owner feedback, rights cho release, human taste và scientific acceptance vẫn
pending. Không có full transcript, raw draft, provider/network hay native host
activation trong review này. Conditional Git simplifier không chạy vì không có
Git live diff; không tạo tín hiệu giả để kích hoạt nó.
