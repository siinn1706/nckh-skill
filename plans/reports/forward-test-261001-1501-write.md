# Forward test — nckh-write — polish nhẹ tiếng Việt

## Phạm vi và thiết lập quan sát

- Yêu cầu: polish nhẹ một đoạn tiếng Việt, giữ nguyên thông tin và câu trích dẫn.
- Đầu vào: văn bản phát triển tổng hợp do người dùng viết, được controller cung cấp; các số liệu dưới đây không phải kết quả khoa học thực đã xác minh.
- Bối cảnh làm việc: `C:/Users/USER/Downloads/test-skill`; múi giờ `Asia/Saigon`.
- Mốc thời gian đọc từ máy: `2026-10-01T15:46:21.8954213+07:00`.
- Skill: `nckh-write`, metadata `version: 0.1.0`, `status: experimental`.
- Chế độ: tiếng Việt, chỉnh sửa phong cách tối thiểu cho đoạn trình bày kết quả khoa học; giữ giọng dè dặt của đầu vào.
- Thực thi: một agent, tải tường minh skill và tài liệu bắt buộc; không có agent con.
- Model identifier, reasoning effort, temperature, seed, tổng token, cửa sổ ngữ cảnh và chi phí suy luận thực tế: không được cung cấp trong lần thử; để unknown.
- Chỉ tạo báo cáo này. Không gọi nghiên cứu/provider, không cài đặt, không sửa sản phẩm.

## Đầu vào nguyên văn

Trong thử nghiệm này, 12 trong số 80 người tham gia báo cáo cải thiện sau 6 tuần. Kết quả có thể liên quan đến can thiệp, nhưng chưa đủ để kết luận quan hệ nhân quả. Tác giả viết: "Không ghi nhận khác biệt có ý nghĩa thống kê."

## Văn bản hoàn chỉnh

:::writing{variant="standard" id="58437"}
Trong thử nghiệm này, 12 trong số 80 người tham gia báo cáo có cải thiện sau 6 tuần. Kết quả này có thể liên quan đến can thiệp, nhưng chưa đủ để kết luận về quan hệ nhân quả. Tác giả viết: "Không ghi nhận khác biệt có ý nghĩa thống kê."
:::

## Trace đọc và hành động thực tế

1. Đọc toàn bộ `SKILL.md` bằng `Get-Content -Raw -LiteralPath`.
2. Đọc đủ bốn shared contracts và hai tài liệu áp dụng cho chế độ này. Sáu lượt đọc chạy song song; mọi lượt trả exit code `0`, không bị cắt nội dung.
3. Kiểm tra đường dẫn báo cáo: kết quả `REPORT_ABSENT`. Đọc thời gian máy bằng `Get-Date -Format o`.
4. Tạo bản chỉnh sửa bằng ba phép thêm từ bên ngoài câu trích dẫn, dựa trên đầu vào thực tế.
5. Chạy so sánh chuỗi ordinal, so sánh số và SHA-256 với PowerShell/.NET; lấy SHA-256 của bảy tệp đã đọc. Kết quả cụ thể ở phần kiểm tra dưới đây.
6. Lưu đầu vào, văn bản hoàn chỉnh, trace và các giới hạn vào báo cáo này bằng `apply_patch`.
7. Đọc lại báo cáo đã lưu, trích xuất đoạn văn trong writing block và tính SHA-256: `90ab9595891731eb92d8be2e30563d2b0043e284e9da20e7b4d694d7df12b0da`; khớp bản đã kiểm tra (`persistedArtifactMatchesValidatedDraft: true`). Sau đó bổ sung kết quả kiểm tra này vào báo cáo.

Các tệp đã đọc và SHA-256 tại thời điểm kiểm tra:

| Tệp trong `nckh-kit/` | SHA-256 |
| --- | --- |
| `skills/core/nckh-write/SKILL.md` | `305201B519BAE88A50115710103659C31DD27C03A454B59F47D764D4CEACB051` |
| `core/policies/authorization-policy.md` | `2ACD9B1FCE80C8545EDB866313A4E1E172D5B002ED1851A21FF36EFF4C5F1F21` |
| `core/policies/evidence-policy.md` | `1D698D443E57B7BA6E1BE8FE5B0D5BAB4FDF514006838E18D80F011367A53CEA` |
| `core/policies/preservation-policy.md` | `6C1704D13E54A39A2D913172C30F053427F28D36E436519F6A17B1F4C244DDD0` |
| `core/policies/acceptance-policy.md` | `8012873DC7D98B352FCF8BB6BE63C4EC459C52A1C1E534EFDFD2F0BE6D9FAAD2` |
| `core/profiles/style/vi.md` | `9867A0D24649AAD9C334A51BA81777358C871060E09D6A3B8953D84DDCB8C8D2` |
| `skills/core/nckh-write/references/fidelity-and-glossary.md` | `E3EF9EFC7844B0B6FADF9D0F947F5468AA2D453DEDC57D0D2A471ED8A9E561B0` |

Không đọc profile tiếng Anh vì yêu cầu chỉ dùng tiếng Việt. Không đọc tài liệu sản phẩm hoặc nguồn nghiên cứu khác.

## Thay đổi và kiểm tra factual delta

Ba thay đổi thực tế:

| Trước | Sau | Mục đích |
| --- | --- | --- |
| `báo cáo cải thiện` | `báo cáo có cải thiện` | Bổ sung từ nối cho cách diễn đạt; giữ sự cải thiện ở dạng người tham gia báo cáo. |
| `Kết quả có thể` | `Kết quả này có thể` | Làm rõ tham chiếu đến kết quả đang được mô tả. |
| `kết luận quan hệ nhân quả` | `kết luận về quan hệ nhân quả` | Bổ sung giới từ. |

Đối chiếu do agent thực hiện:

| Chiều thông tin | Trước → sau | Nhận xét giới hạn |
| --- | --- | --- |
| Số lượng và mẫu số | `12 trong số 80` → nguyên văn | Không chuyển thành tỷ lệ hay suy ra thêm số liệu. |
| Đối tượng | `người tham gia` → nguyên văn | Không thêm đặc điểm quần thể. |
| Thời gian và đơn vị | `sau 6 tuần` → nguyên văn | Không đổi mốc theo dõi. |
| Nguồn cải thiện | `báo cáo cải thiện` → `báo cáo có cải thiện` | Vẫn là thông tin được người tham gia báo cáo. |
| Modality và causal scope | `có thể liên quan đến can thiệp` → nguyên văn | Không nâng thành tác động hay quan hệ nhân quả đã chứng minh. |
| Giới hạn kết luận | `chưa đủ để kết luận` → nguyên văn | Giữ sự chưa đủ bằng chứng. |
| Phủ định và thống kê | `Không ghi nhận khác biệt có ý nghĩa thống kê.` → nguyên văn | Nằm trong trích dẫn được bảo vệ. |
| Thuật ngữ | `thử nghiệm`, `can thiệp`, `quan hệ nhân quả`, `ý nghĩa thống kê` → nguyên văn | Không có glossary do người dùng cung cấp; giữ nguyên thuật ngữ đầu vào. |
| Trích dẫn và dẫn nguồn | Toàn bộ câu trích dẫn → nguyên văn | Không thêm tác giả, tài liệu, DOI hay thông tin nguồn chưa được cung cấp. |

Kết quả kiểm tra chuỗi thực tế:

```json
{
  "onlyDeclaredInsertions": true,
  "protectedQuoteExact": true,
  "sourceNumbers": ["12", "80", "6"],
  "draftNumbers": ["12", "80", "6"],
  "numbersExact": true,
  "sourceTextSha256": "c59b5419e4e6e5baafb601bed978be7180a53e74ca9f43e27730ecd63ff49e00",
  "draftTextSha256": "90ab9595891731eb92d8be2e30563d2b0043e284e9da20e7b4d694d7df12b0da"
}
```

Hai text hash tính trên UTF-8 của chính chuỗi đoạn văn, không kèm BOM hoặc newline. `onlyDeclaredInsertions` được kiểm tra bằng cách đảo ba thay đổi đã liệt kê và so sánh toàn chuỗi ordinal với đầu vào; `protectedQuoteExact` so sánh nguyên văn đoạn nằm giữa dấu ngoặc kép. Đây là kiểm tra bảo toàn chuỗi cho mẫu này; bảng đối chiếu ngữ nghĩa do agent thực hiện không thay thế đánh giá của người có chuyên môn.

## Gate và giới hạn

| Gate trong phạm vi lần thử | Trạng thái | Bằng chứng |
| --- | --- | --- |
| Đọc tường minh skill và tài liệu áp dụng | PASS | Bảy lượt đọc thành công đã ghi ở trace. |
| Artifact đã lưu khớp bản đã kiểm tra | PASS | SHA-256 đoạn văn trích xuất từ báo cáo khớp draft hash. |
| Chỉnh sửa tối thiểu có thay đổi thực tế | PASS | Ba phép thêm từ; phép đảo thay đổi khôi phục toàn bộ đầu vào. |
| Giữ nguyên số và câu trích dẫn | PASS | So sánh chuỗi thực tế ở trên. |
| Đánh giá tính đúng đắn khoa học của số liệu | UNTESTED | Đầu vào tổng hợp; không có dữ liệu, phương pháp hay nguồn gốc nghiên cứu. |
| Human/domain fidelity và sở thích văn phong | PENDING | Chưa có người đánh giá độc lập. |
| Native discovery và host integration | UNTESTED | Skill được chỉ định bằng đường dẫn và tải tường minh. |

Quan sát này thuộc mức **agent behavior với explicit instruction loading** trên một đầu vào phát triển tổng hợp. Không suy ra chất lượng tiếng Việt được con người chấp nhận, độ đúng đắn khoa học, native discovery, khả năng khái quát trên văn bản khác hoặc stable eligibility của skill. Không có factual delta mới được agent ghi nhận; vẫn giữ gate human/domain fidelity độc lập.

Status: DONE

Summary: Đã tạo bản polish nhẹ tiếng Việt, giữ số liệu, mức độ dè dặt và nguyên văn trích dẫn; ghi lại đường đọc, hành động và kết quả kiểm tra thực tế.

Concerns/Blockers: Không có blocker cho việc tạo artifact và báo cáo. Native discovery, đánh giá con người/chuyên môn và tính hợp lệ khoa học chưa được kiểm tra.
