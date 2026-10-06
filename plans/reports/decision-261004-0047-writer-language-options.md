# Quyết định language options cho hai writer

Ngày: 04/10/2026, Asia/Saigon. Status: **design selected under user-delegated authority; plan-only**. User hỏi nên dùng `--en`/`--vi` hay bốn skill có hậu tố locale và giao quyền tự cân nhắc/chọn. Quyết định này không phê duyệt chín red-team amendments hay triển khai.

## Quyết định

Giữ hai identity `nckh-paperwrite`, `nckh-humanwrite`; mỗi skill nhận một trong `--en`, `--vi`. Không tạo `paperwrite-en`, `paperwrite-vi`, `humanwrite-en`, `humanwrite-vi` hoặc alias identity tương đương. Target catalog: 37 hiện tại + 2 mới = 39; source hiện hành vẫn 37.

Lý do: nhiệm vụ quyết định owner, ngôn ngữ quyết định cách diễn đạt. Evidence/factual preservation, scope NCKH và reader không thay identity theo locale. Bốn entrypoint sẽ nhân đôi routing/closure/evals và làm các policy dễ lệch. Tách style/reference theo language bên trong skill đáp ứng khác biệt VI/EN mà không lặp toàn workflow. Source hiện có `core/profiles/style/en.md` và `vi.md` riêng, brief schema đã có `language = vi|en|bilingual` (`nckh-kit/core/contracts/brief.schema.json:21-27`).

## Giao diện dự kiến — chưa cài

```text
nckh-paperwrite --en <scientific writing brief>
nckh-paperwrite --vi <brief viết khoa học>
nckh-humanwrite --en <text và editing brief>
nckh-humanwrite --vi <văn bản và yêu cầu biên tập>
```

Đây là đối số ở giao diện skill, không khẳng định native slash command hay CLI parser đã có. Hai entrypoint và `nckh-write` router phải normalize đúng khi triển khai.

## Hợp đồng

1. Flag chọn **ngôn ngữ đầu ra**, không suy từ ngôn ngữ tài liệu đầu vào. `--en` có thể xử lý input VI và ngược lại, theo đúng nhiệm vụ biên tập/viết/dịch được giao.
2. Chỉ một flag ngôn ngữ: có cả `--en` và `--vi` là lỗi xung đột; không chọn cờ cuối, không tạo/sửa artifact.
3. Thứ tự lựa chọn: flag rõ ràng > target language user nói trong yêu cầu > `brief.language` > ngôn ngữ chính của draft. Nếu các nguồn thiếu/mixed không xác định được target thì hỏi một câu, không mặc định mọi paper thành English. Flag rõ ràng có thể thu hẹp brief bilingual thành một output locale.
4. Không flag là hợp lệ khi target đã rõ. Giữ route bilingual đã có cho yêu cầu song ngữ; không thêm `--bilingual` hoặc skill mới ngoài scope này. Router truyền action và locale sang đúng owner, không route chỉ vì input chứa chữ paper.
5. Nạp style VI/EN có chọn lọc; shared factual preservation/evidence rules không nhân bản. Tiếng Việt không dùng blacklist dịch máy từ English; paperwrite cả hai ngôn ngữ vẫn scientific-only, humanwrite vẫn language editing.
6. Output language và source/resource locale là hai chiều riêng. `search-resource.py:220-223` kiểm locale/genre theo resource; `paperwrite --vi` không được ép tham số đọc PMC English sang `locale=vi`. Ghi output language trong brief/artifact và resource locale thật trong read receipt.
7. Giữ số, units, phủ định, certainty, citations, glossary và protected spans qua thay đổi ngôn ngữ. Dịch không cấp quyền thêm claim; phần trích nguyên văn cần giữ/mô tả đúng brief, không giả bản dịch là quote gốc.

## Acceptance để đưa vào P1/P4

Cả hai writer × hai locale; conflict flags/no mutation; no-flag resolution; VI→EN/EN→VI fidelity; EN resource với VI output; bilingual compatibility; `nckh-write` truyền locale; host invocation không làm rơi flag. Các ca này là supplemental route/locale tests, không đổi identity hoặc nhân đôi base case ID. Static flag parsing chưa chứng minh chất lượng văn phong VI/EN; personal owner review vẫn riêng.

Không sửa skill/source/install/config trong quyết định này. Red-team gate, implementation authority và hook trust/runtime gates vẫn pending.
