# So sánh capability debug qua nckh-xia --compare

## Kết quả

Giữ `nckh-debug` làm chủ đầu ra chẩn đoán của NCKH. Hai nguồn cùng yêu cầu điều tra nguyên nhân trước khi sửa và xác minh bằng chứng trước khi kết luận. `ak-debug` cung cấp thủ tục chi tiết hơn cho CI, log, database, hiệu năng và frontend; `nckh-debug` nêu rõ giới hạn chẩn đoán, bảo toàn thay đổi có sẵn và giao việc sửa cho `fix` trong trạng thái thực thi do `cook` quản lý. Khuyến nghị chính là **EXTENSION có điều kiện** cho các nhánh chuyên biệt khi đề bài cần đến chúng. Chưa có căn cứ cho việc port toàn bộ hoặc kết luận một capability sửa lỗi tốt hơn capability còn lại.

Đây là kết quả chạy tác vụ phân tích của agent trong vòng phát triển. Không phải kiểm thử khám phá skill qua giao diện host, không phải đánh giá bằng nhãn chuẩn của con người, và không chứng nhận toàn bộ NCKH kit.

- Yêu cầu được thực hiện: dùng đường dẫn `nckh-xia/SKILL.md` đã giao để so sánh snapshot `ak-debug` được cài cục bộ với `nckh-debug` hiện có, chế độ `--compare`.
- Ngôn ngữ: tiếng Việt. Múi giờ: `Asia/Saigon` (`UTC+07:00`). Mốc thu nguồn: `2026-10-01T15:47:57+07:00`.
- Tham chiếu công việc: tác vụ `/root/forward_xia`, đề bài ban đầu của lượt kiểm thử này. Phạm vi được giao là đọc nguồn được chỉ định và ghi duy nhất báo cáo này; tham chiếu đó không phải giấy cấp quyền gọi provider hay xuất bản.
- Output được sở hữu: `C:/Users/USER/Downloads/test-skill/plans/reports/forward-test-261001-1501-xia.md`.
- Chế độ `--compare` tạo báo cáo; các khuyến nghị dưới đây không phải kế hoạch chuyển thể hay lệnh triển khai. Căn cứ: nckh-xia, dòng 28–36 (historical evidence path: `C:/Users/USER/Downloads/test-skill/nckh-kit/skills/tooling/nckh-xia/SKILL.md:28`; unavailable in the cleaned checkout).

## Nguồn, revision và độ sâu kiểm tra

| Nguồn | Origin được quan sát | Phiên bản được nguồn tự khai | Ref dùng cho so sánh | Độ sâu thực sự |
|---|---|---|---|---|
| Bộ so sánh `nckh-xia` | Tệp trong workspace ở đường dẫn được đề bài chỉ định | `0.1.0`, `experimental` | Đường dẫn tuyệt đối và SHA-256 trong manifest | Đọc toàn bộ SKILL, disposition, bốn policy và các workflow liên quan |
| `ak-debug` | Snapshot được cài tại `C:/Users/USER/.agents/skills/ak-debug/` | `4.2.0`; author tự khai `agentkit` | Đường dẫn tuyệt đối và SHA-256 từng tệp | Đọc toàn bộ SKILL, mười reference trong capability, protocol ultra được liên kết và mã script `find-polluter.sh`; chỉ phân tích tĩnh |
| `nckh-debug` | Tệp trong workspace NCKH được đề bài chỉ định | `0.1.0`, `experimental` | Đường dẫn tuyệt đối và SHA-256 từng tệp | Đọc toàn bộ SKILL, policy và các workflow được liên kết có liên quan |

Không có origin GitHub, commit/tag upstream hay sổ đăng ký alias được quan sát. `agentkit` là attribution tự khai trong metadata; không dùng nó để suy ra một repository. Hash khóa nội dung cục bộ đã đọc, không chứng minh snapshot mới nhất so với upstream. Đã đọc nội dung hướng dẫn và một script thực, vượt quá mức đọc metadata; chưa kiểm tra khả năng thực thi của các công cụ, các capability phụ được nêu tên hay toàn bộ closure phụ thuộc. `advisory-supervision.md` được protocol ultra nhắc đến nhưng không đọc vì không chạy ultra hoặc giải quyết định tuyến model ở lượt này.

## Ma trận cấu trúc và hành vi

| Khía cạnh | `ak-debug` được đọc | `nckh-debug` được đọc | Kết luận trong phạm vi nguồn |
|---|---|---|---|
| Đầu vào | Bug, test/build/integration failure; server, CI, hiệu năng, database, log. SKILL dòng 25–29 (historical evidence path: `C:/Users/USER/.agents/skills/ak-debug/SKILL.md:25`; unavailable in the cleaned checkout) | Triệu chứng, hành vi kỳ vọng, tái hiện, môi trường và quyền đọc repository/log có giới hạn. SKILL dòng 11–15 (historical evidence path: `C:/Users/USER/Downloads/test-skill/nckh-kit/skills/engineer/nckh-debug/SKILL.md:11`; unavailable in the cleaned checkout) | Cùng lõi chẩn đoán; AK liệt kê thêm các nhánh hệ thống cụ thể |
| Quy trình nguyên nhân | Bốn bước điều tra, đối chiếu pattern, kiểm định giả thuyết, triển khai; đọc lỗi, tái hiện và trace data qua các component. systematic-debugging dòng 13–54 (historical evidence path: `C:/Users/USER/.agents/skills/ak-debug/references/systematic-debugging.md:13`; unavailable in the cleaned checkout) | Xác định kỳ vọng và ranh giới an toàn; đọc owner, caller, test, lỗi; tái hiện hẹp khi được phép và trace nguyên nhân. SKILL dòng 28–30 (historical evidence path: `C:/Users/USER/Downloads/test-skill/nckh-kit/skills/engineer/nckh-debug/SKILL.md:28`; unavailable in the cleaned checkout) | NCKH đã bao phủ invariant chính; chưa cần một chủ sở hữu quy trình thứ hai |
| Giả thuyết đối lập | Điều tra hệ thống yêu cầu xếp và loại giả thuyết bằng evidence. investigation-methodology dòng 73–83 (historical evidence path: `C:/Users/USER/.agents/skills/ak-debug/references/investigation-methodology.md:73`; unavailable in the cleaned checkout) | Đầu ra có counter-hypotheses; kiểm tra giả thuyết cạnh tranh khi cần, test không liên quan không đủ. SKILL dòng 15, 30 (historical evidence path: `C:/Users/USER/Downloads/test-skill/nckh-kit/skills/engineer/nckh-debug/SKILL.md:30`; unavailable in the cleaned checkout) | Có coverage trùng nhau về kiểm định nguyên nhân |
| Điểm dừng và owner sửa | Reference có bước implementation; phần workflow positioning cũng nêu `ak:fix` thường theo sau debug. systematic-debugging dòng 48–62 (historical evidence path: `C:/Users/USER/.agents/skills/ak-debug/references/systematic-debugging.md:48`; unavailable in the cleaned checkout), SKILL dòng 132–136 (historical evidence path: `C:/Users/USER/.agents/skills/ak-debug/SKILL.md:132`; unavailable in the cleaned checkout) | Chẩn đoán thuần dừng trước product edits; khi được yêu cầu sửa, giao nguyên nhân đã chứng minh cho `fix`, `cook` sở hữu trạng thái. SKILL dòng 32 (historical evidence path: `C:/Users/USER/Downloads/test-skill/nckh-kit/skills/engineer/nckh-debug/SKILL.md:32`; unavailable in the cleaned checkout) | Khi chuyển ý tưởng sang NCKH cần giữ owner và điểm dừng NCKH; không nhập nguyên trạng bước implementation của AK |
| Xác minh và receipt | Yêu cầu xác minh mới, đọc exit code/output; red–green và test triệu chứng gốc. verification dòng 19–45 (historical evidence path: `C:/Users/USER/.agents/skills/ak-debug/references/verification.md:19`; unavailable in the cleaned checkout) | Receipt phải có command, môi trường, output, input hashes; tách tái hiện xác định, runtime và suy luận chưa xác minh; không giấu check lỗi. SKILL dòng 28–30 (historical evidence path: `C:/Users/USER/Downloads/test-skill/nckh-kit/skills/engineer/nckh-debug/SKILL.md:28`; unavailable in the cleaned checkout) | Đều yêu cầu evidence; NCKH nêu rõ khóa input và cấp độ evidence trong contract |
| Retry thất bại | Sau ba lần sửa thất bại phải dừng và bàn lại kiến trúc với người dùng. systematic-debugging dòng 55–62 (historical evidence path: `C:/Users/USER/.agents/skills/ak-debug/references/systematic-debugging.md:55`; unavailable in the cleaned checkout) | SKILL debug đã đọc không có bộ đếm retry sửa; core acceptance giới hạn ba vòng phát triển đánh giá. acceptance dòng 17–19 (historical evidence path: `C:/Users/USER/Downloads/test-skill/nckh-kit/core/policies/acceptance-policy.md:17`; unavailable in the cleaned checkout) | Hai giới hạn này khác nghĩa. Chưa đọc source `fix`/`cook`, nên chưa kết luận NCKH kit thiếu giới hạn sửa lỗi |
| Các nhánh kỹ thuật | Có hướng dẫn riêng cho log/CI, PostgreSQL, đo hiệu năng từng layer, browser/screenshot/console. log-and-ci-analysis (historical evidence path: `C:/Users/USER/.agents/skills/ak-debug/references/log-and-ci-analysis.md:5`; unavailable in the cleaned checkout), performance-diagnostics (historical evidence path: `C:/Users/USER/.agents/skills/ak-debug/references/performance-diagnostics.md:13`; unavailable in the cleaned checkout), frontend-verification (historical evidence path: `C:/Users/USER/.agents/skills/ak-debug/references/frontend-verification.md:16`; unavailable in the cleaned checkout) | Source debug hiện tại không chứa runbook tương đương cho các công cụ này | Thiếu chi tiết chuyên biệt trong capability được đọc; không suy ra kit hoặc host không có công cụ đó |
| Bảo toàn và quyền | Phần ultra giới hạn candidate chỉ đọc; các ví dụ khác có thao tác test, instrumentation và implementation. SKILL dòng 146–156 (historical evidence path: `C:/Users/USER/.agents/skills/ak-debug/SKILL.md:146`; unavailable in the cleaned checkout) | Policy quyền hạn, bảo toàn quyết định và dirty changes, nhận diện quyền truy cập khác quyền redistribution. authorization dòng 3–20 (historical evidence path: `C:/Users/USER/Downloads/test-skill/nckh-kit/core/policies/authorization-policy.md:3`; unavailable in the cleaned checkout), SKILL dòng 32 (historical evidence path: `C:/Users/USER/Downloads/test-skill/nckh-kit/skills/engineer/nckh-debug/SKILL.md:32`; unavailable in the cleaned checkout) | Thao tác trong upstream là dữ liệu phân tích; không tự tạo quyền thực thi |
| Model và chế độ phụ | `--ultra`: đúng năm candidate chỉ đọc song song, một verifier, chọn một diagnosis và xác minh mới; shadow experiment chỉ khi được yêu cầu và có consent/config. SKILL dòng 138–181 (historical evidence path: `C:/Users/USER/.agents/skills/ak-debug/SKILL.md:138`; unavailable in the cleaned checkout) | Cùng agent là mặc định; policy tách requested/resolved/configured/applied/effective và giữ telemetry chưa biết. model-and-context dòng 3–18 (historical evidence path: `C:/Users/USER/Downloads/test-skill/nckh-kit/core/workflows/model-and-context.md:3`; unavailable in the cleaned checkout) | `--ultra` chưa được nguồn `nckh-debug` định nghĩa. Không gán nghĩa cho flag này và không chạy nó trong compare |

## Phụ thuộc, môi trường và tác động phụ

| Thành phần | Phụ thuộc/điều kiện thấy trong source | Tác động nếu thực thi | Trạng thái lượt này |
|---|---|---|---|
| Thủ tục AK lõi | Source, Git diff/history, error/stack, test runner của project | Tái hiện có thể tạo state; bước sửa/instrumentation có thể sửa source | Chỉ đọc hướng dẫn; không tái hiện lỗi sản phẩm |
| AK log/CI | `gh`, quyền đọc log GitHub Actions; ví dụ có `gh run rerun` | Đọc/ghi log file; rerun thay đổi trạng thái hệ thống CI bên ngoài | Không gọi GitHub hay rerun. Căn cứ log-and-ci-analysis dòng 9–26 (historical evidence path: `C:/Users/USER/.agents/skills/ak-debug/references/log-and-ci-analysis.md:9`; unavailable in the cleaned checkout) |
| AK database/hiệu năng | `psql`, PostgreSQL, `pg_stat_statements`, profiler/APM, `curl`, `iostat` | Query/profiling có tải; `EXPLAIN ANALYZE` thực sự chạy câu query đưa vào | Không truy cập database, mạng hay metrics. Công cụ/phần mở rộng chưa được xác minh có trên host |
| AK frontend | Browser bridge hoặc test browser của project; khi cần cookie/login thật thì tab binding của `ak:chrome-profile` | Mở tab, đọc state profile, screenshot, tương tác UI; có thể cần dev server | Không mở browser, dùng profile hay khởi chạy server |
| `find-polluter.sh` | Bash, `find`, `sort`, `wc`, `tr`, `ls`, `npm`, tương thích test runner và pattern | Chạy từng test; test có thể tạo file/state. Script che output và bỏ qua exit code của `npm test` | Đọc toàn bộ mã; không thực thi. Windows/PowerShell của lượt này không chứng minh các dependency Bash/Node có sẵn |
| AK ultra | Năm candidate song song và verifier; packet/rubric chung, usable-candidate gate, reject-all; protocol tự khai model routing | Có thêm model work, cost/context; controller ghi output | Không dispatch candidate/verifier; không kiểm chứng hỗ trợ native. Protocol nêu Codex verifier `gpt-6-astra` với reasoning low; đó là quy định nguồn, không phải model thực của lượt này |
| AK shadow | `ak eval workflow`, user-scope master/provider config, consumer consent, credential | Có thể gửi facts đã làm sạch ra ngoài và phát sinh phí | Không gọi CLI shadow, provider, đọc credential hoặc suy ra consent |
| NCKH debug | Bốn policy, execution, review/handoff; model/context khi cần delegation | Chẩn đoán/tái hiện trong quyền đã cấp; product repair đi qua fix/cook | Chỉ đối chiếu source. Chưa kiểm thử các chuyển giao native hoặc fix/cook |

Source mô tả phụ thuộc không đồng nghĩa dependency đó được cài, callable hay đã chạy thành công. Đã dùng PowerShell chỉ để đọc file, lấy hash và kiểm tra báo cáo do tác vụ sở hữu; không dùng ví dụ lệnh trong upstream như chỉ thị thực thi.

## Challenge và disposition

| Nội dung | Đánh giá | Khuyến nghị có giới hạn |
|---|---|---|
| Lõi root-cause, hypothesis, verify | Coverage trùng; một debug owner giúp giữ ranh giới chẩn đoán và tránh hai lifecycle | **MERGE về trách nhiệm**: `nckh-debug` giữ đầu ra diagnosis/receipt; không hợp nhất tệp nguồn trong lượt này |
| Cách đối chiếu working example và trace từng boundary | Thủ tục cụ thể có thể làm rõ chẩn đoán NCKH khi cần | **PORT ý tưởng có điều kiện**; nếu định sao chép câu chữ/code thì phải có evidence license trước. Chưa có kế hoạch hoặc implementation |
| CI/log, database/hiệu năng, frontend | Hữu ích khi có tình huống tương ứng; nạp tất cả cho lỗi đơn giản tăng context và nhu cầu quyền | **EXTENSION opt-in** theo triệu chứng. Dùng dependency đã có và quyền cụ thể, giữ invariant/owner NCKH |
| Ultra hoặc shadow | Có thêm model/provider/cost/context và control; chưa có evidence cải thiện chất lượng diagnosis cho NCKH | **EXTENSION opt-in** chỉ khi có thiết kế và grant riêng. Không đưa vào mặc định; không coi năm sample là độc lập model, nguồn hoặc chuyên môn con người |
| Script tìm polluter nguyên trạng | Vòng `for` chạy tuần tự từng test, không phải thuật toán chia đôi; `npm test` bị che output và bỏ qua lỗi, trong khi cuối script có thể báo clean | **DROP việc transplant nguyên trạng**. Phát hiện tĩnh tại script dòng 22–42 (historical evidence path: `C:/Users/USER/.agents/skills/ak-debug/scripts/find-polluter.sh:22`; unavailable in the cleaned checkout), script dòng 61–63 (historical evidence path: `C:/Users/USER/.agents/skills/ak-debug/scripts/find-polluter.sh:61`; unavailable in the cleaned checkout). Không tìm thấy file ô nhiễm không chứng minh test pass hoặc đã chạy được; chưa chạy script để đo hành vi |
| Validation tại mọi layer | SKILL chính AK giới hạn check vào nơi phân biệt nguyên nhân hoặc bảo vệ contract; reference lại yêu cầu mọi layer. Đây là khác biệt hướng dẫn quan sát được | **DROP yêu cầu blanket khi chuyển thể**; giữ check có căn cứ. Căn cứ SKILL dòng 45–49 (historical evidence path: `C:/Users/USER/.agents/skills/ak-debug/SKILL.md:45`; unavailable in the cleaned checkout), defense-in-depth dòng 89–96 (historical evidence path: `C:/Users/USER/.agents/skills/ak-debug/references/defense-in-depth.md:89`; unavailable in the cleaned checkout) |
| Tuyên bố hiệu quả của thủ tục AK | Reference có con số thời gian/tỷ lệ thành công, nhưng các tệp đã đọc không cung cấp tập đánh giá, protocol hay receipt chứng minh | Không dùng các con số đó làm bằng chứng ưu thế hay KPI cho NCKH. systematic-debugging dòng 96–102 (historical evidence path: `C:/Users/USER/.agents/skills/ak-debug/references/systematic-debugging.md:96`; unavailable in the cleaned checkout) |
| Clone/alias và sở hữu trùng | Có owner NCKH hiện hữu; compare không cấp quyền triển khai hoặc ghi đè skill được cài | **DROP clone toàn bộ và alias gây shadow**. Không sửa `ak-debug`, `ak-xia` hoặc bất kỳ source NCKH nào |

Các disposition là khuyến nghị từ source, chưa phải quyết định người dùng hay evidence chấp nhận chuyển thể. Không có numeric benchmark hoặc tuyên bố chất lượng vượt trội.

## Quyền và giới hạn nguồn

| Quyền/bằng chứng | `ak-debug` | `nckh-debug`/`nckh-xia` |
|---|---|---|
| Đọc và phân tích cục bộ | Được đề bài kiểm thử chỉ định; đọc thành công | Được đề bài kiểm thử chỉ định; đọc thành công |
| Attribution thấy trong nguồn | Metadata khai `author: agentkit`, `version: 4.2.0` | Name/version/status tự khai; các tệp đã đọc không khai author |
| Giấy phép được quan sát | Không có điều khoản license trong các tệp đã đọc; không được giao phạm vi kiểm tra license khác | Không có điều khoản license trong các tệp đã đọc; không được suy từ vị trí workspace |
| Quyền evaluation/phân phối của upstream | Quyền chạy tác vụ phân tích này không xác lập giấy phép evaluation rộng hơn hoặc quyền redistribution | Tương tự; source thuộc workspace không tự xác lập quyền xuất bản |
| Sao chép, packaging, redistribution | **UNKNOWN; chặn việc sao chép/phân phối đến khi có license hoặc grant đủ phạm vi** | **UNKNOWN đối với phân phối ngoài scope** |

Không tìm upstream trên mạng, không đoán URL hoặc giấy phép. Báo cáo diễn giải nguồn để so sánh; không chép script hoặc body skill vào sản phẩm, không đóng gói và không cài dependency. Thiếu license không chặn phân tích cục bộ đã giao, nhưng giữ pending cho mọi chuyển thể cần sao chép và mọi phân phối.

## Model, context và chi phí

| Trường | Quan sát trong lượt này |
|---|---|
| Requested model/effort | Đề bài so sánh không chỉ định model ID hoặc effort; dùng agent hiện có |
| Resolved model/effort | **UNKNOWN**; không có receipt native giải quyết model được expose |
| Configured model/effort | Role được expose là `default`; không có concrete model ID/effort hoặc precedence receipt |
| Applied model/effort | Agent này không yêu cầu đổi model/effort và không spawn thêm agent; không có receipt applied settings |
| Effective model/effort | **UNKNOWN**; không suy từ tên role, self-description của hệ thống, danh mục model hay model được protocol upstream nêu |
| Context window/usage/compliance | **UNKNOWN**; số tệp và token count của output công cụ không thay thế telemetry context của native run |
| Total cost | **UNKNOWN**; không phát sinh lời gọi provider do agent chủ động, không suy thành tổng cost bằng 0 |
| Independence | Pass phân tích do agent được giao riêng thực hiện. Không có evidence độc lập model, độc lập source, verifier độc lập hay reviewer con người |

Các trường tách riêng theo model-and-context dòng 16–25 (historical evidence path: `C:/Users/USER/Downloads/test-skill/nckh-kit/core/workflows/model-and-context.md:16`; unavailable in the cleaned checkout). Không thử model trả phí hoặc đọc credential để suy ra availability.

## Manifest các tệp thực sự đã đọc

SHA-256 khóa bytes của 23 tệp đã đọc toàn bộ. Mỗi entry là một nguồn thực, không phải chỉ metadata của dependency. Các đường dẫn trong bảng là tuyệt đối.

| ID | Đường dẫn | SHA-256 |
|---|---|---|
| S01 | `C:/Users/USER/Downloads/test-skill/nckh-kit/skills/tooling/nckh-xia/SKILL.md` | `497D63F8EB9F5DDC9FE88AA0860AF62C02503D63439446F6236E333F99B25D9A` |
| S02 | `C:/Users/USER/Downloads/test-skill/nckh-kit/skills/tooling/nckh-xia/references/source-disposition.md` | `C2CA59F3AAC804D4B570314628B61525A7ACB9298690B2BBC7ADC4D33894EA88` |
| S03 | `C:/Users/USER/.agents/skills/ak-debug/SKILL.md` | `BEAD05D76313566ABA051F54BB55FADA5993DE590A510109DA1C76DF8A01F720` |
| S04 | `C:/Users/USER/Downloads/test-skill/nckh-kit/skills/engineer/nckh-debug/SKILL.md` | `850ABFCEFD42FCC778D4AFD7A11F71B1B12B3947A7BDF6452DA792D15706CF51` |
| S05 | `C:/Users/USER/Downloads/test-skill/nckh-kit/core/policies/authorization-policy.md` | `2ACD9B1FCE80C8545EDB866313A4E1E172D5B002ED1851A21FF36EFF4C5F1F21` |
| S06 | `C:/Users/USER/Downloads/test-skill/nckh-kit/core/policies/evidence-policy.md` | `1D698D443E57B7BA6E1BE8FE5B0D5BAB4FDF514006838E18D80F011367A53CEA` |
| S07 | `C:/Users/USER/Downloads/test-skill/nckh-kit/core/policies/preservation-policy.md` | `6C1704D13E54A39A2D913172C30F053427F28D36E436519F6A17B1F4C244DDD0` |
| S08 | `C:/Users/USER/Downloads/test-skill/nckh-kit/core/policies/acceptance-policy.md` | `8012873DC7D98B352FCF8BB6BE63C4EC459C52A1C1E534EFDFD2F0BE6D9FAAD2` |
| S09 | `C:/Users/USER/Downloads/test-skill/nckh-kit/core/workflows/execution.md` | `412DC49B937A6BFF6501E841A586937BE1AA4309C9180D125307553073B45A7A` |
| S10 | `C:/Users/USER/Downloads/test-skill/nckh-kit/core/workflows/model-and-context.md` | `4EA0F35662D1171ECC3333EC194A615492626D25EFF5573E30DA3CAA8CA8B28F` |
| S11 | `C:/Users/USER/Downloads/test-skill/nckh-kit/core/workflows/review-and-handoff.md` | `91E10985995B8F6897A6605DCDD92B0E8C421637115C7C1AC7DA9B25275F4A6A` |
| S12 | `C:/Users/USER/.agents/skills/ak-debug/references/systematic-debugging.md` | `25206083F21454B6339B431FBC67EEB4785A2D1F55FDF12AE6F255E31CBD80CB` |
| S13 | `C:/Users/USER/.agents/skills/ak-debug/references/root-cause-tracing.md` | `4DF0E51B2D26A407D3E2FFBA19C7C0CF8D01698C1745009E667B69BA2C962100` |
| S14 | `C:/Users/USER/.agents/skills/ak-debug/references/defense-in-depth.md` | `1C156E07238851F52E729F086D97EA2C90C5DA19D31E333844216883BBDDBEB5` |
| S15 | `C:/Users/USER/.agents/skills/ak-debug/references/verification.md` | `AC56942520327EFAF29B415B27E6A4211D88386D0072C5D400FDEE39EBA8BBF3` |
| S16 | `C:/Users/USER/.agents/skills/ak-debug/references/investigation-methodology.md` | `FDC7DE8C841E93FBE5244E7EAB5B78856993009A7F3C7E47AA0ED18471AF0199` |
| S17 | `C:/Users/USER/.agents/skills/ak-debug/references/log-and-ci-analysis.md` | `B33C7C8C3F436A1AEC3D9842A8990EBFF6B731674866D7DD4FF0C75D6020DB73` |
| S18 | `C:/Users/USER/.agents/skills/ak-debug/references/performance-diagnostics.md` | `BE9BD0342D6BEF3ADBA741217BCF03BAA0E5781B18C7C70B07AF2F7B343E7936` |
| S19 | `C:/Users/USER/.agents/skills/ak-debug/references/reporting-standards.md` | `E92CB3DAA0CDA16CF54E8AAF06BFB32486D7648AAD659645C6AF87C29FD4D634` |
| S20 | `C:/Users/USER/.agents/skills/ak-debug/references/task-management-debugging.md` | `116726A6DB0320D1852650521826CF93FC3104E3A998CCFC40BE202A9C28A2E3` |
| S21 | `C:/Users/USER/.agents/skills/ak-debug/references/frontend-verification.md` | `430BC6137515B4565EE3ECC48821BBDA290C5B207B8E7FCA1C94010D81B97E5E` |
| S22 | `C:/Users/USER/.agents/skills/ak-debug/scripts/find-polluter.sh` | `F4DC594206175B17DE25464B5F60A0E011774A7C7843014B6442338A085EBA57` |
| S23 | `C:/Users/USER/.agents/skills/ak-brainstorm/references/ultra-verifier-mode.md` | `5498EEA1D371CBF9E965CAD5F517F488183F71DACCB8F3F98ABCFAC86A3B782A` |

## Hành động quan sát được và kiểm tra

- Đọc toàn bộ 23 tệp trong manifest bằng công cụ đọc cục bộ; các thao tác đọc đã trả exit code `0` và nội dung thật. Bốn policy được đọc trước khi đối chiếu hai source debug.
- Lấy SHA-256 bằng `Get-FileHash`; hiển thị hash dài bằng JSON để tránh cột PowerShell bị rút gọn. Hash đầu tiên của `nckh-debug` từng bị rút gọn khi hiển thị bảng; manifest dùng hash đầy đủ đã lấy lại, không đoán phần còn thiếu.
- Kiểm tra đường dẫn báo cáo trước khi viết, kết quả `REPORT_NOT_CREATED`; tạo duy nhất báo cáo này.
- Không chạy script upstream, test suite, CLI `ak`, GitHub, provider, browser, installer hoặc dev process. Không tạo implementation plan, cài alias, sửa product hay gửi tin nhắn.
- Check sau khi ghi chạy lúc `2026-10-01T15:54:35+07:00`, trả exit code `0`: có đúng 23 entry nguồn; cả 23 SHA-256 khớp nội dung hiện tại; 29 link source đều tồn tại và locator dòng không vượt số dòng của tệp. Đã đọc lại toàn bộ nội dung báo cáo. Đây là check tính toàn vẹn/locator, không phải kiểm thử diagnosis runtime hay chất lượng được con người chấp nhận.

| Gate | Trạng thái và phạm vi |
|---|---|
| Đọc actual source, locale, compare/report boundary | **PASS** cho lượt agent này; bằng chứng là tool output đọc file và artifact báo cáo |
| Hash nguồn và link/locator báo cáo | **PASS** lúc `15:54:35+07:00`: `source_count=23`, `hash_mismatches=[]`, `link_count=29`, `link_or_line_issues=[]`, exit code `0` |
| So sánh cấu trúc, dependency, side effect và disposition | **PASS trong phạm vi source được đọc**; không xác lập hiệu quả runtime |
| Upstream revision, license và copying/redistribution | **UNVERIFIED**; cần license/origin evidence và grant phù hợp nếu chuyển sang sao chép hoặc phân phối |
| Runtime diagnosis/fix và native skill discovery | **NOT RUN**; đề bài này không kiểm thử hai capability trên một bug hay tự động discover skill |
| Effective model/cost/context | **UNKNOWN**; chưa expose receipt native |
| Human gold, acceptance khoa học/con người, stable eligibility | **NOT ESTABLISHED**; pass phát triển này không chứng nhận toàn kit hoặc một badge stable |

## Câu hỏi còn mở

- Giấy phép, origin và revision upstream nào áp dụng cho snapshot AK hiện tại? Owner nguồn cần cung cấp bằng chứng trước sao chép/phân phối.
- Project NCKH thực tế cần nhánh CI, database, frontend hoặc ultra nào? Yêu cầu sử dụng cụ thể mới quyết định có mở extension hay không.
- Host có expose native receipt về effective model/cost/context và discovery hay không? Chưa kiểm chứng trong phạm vi được giao.

Status: DONE_WITH_CONCERNS
Summary: Đã trả báo cáo so sánh dùng được từ actual local source, với manifest, ma trận hành vi, dependency/tác động phụ, giới hạn quyền và model tách riêng. Khuyến nghị giữ nckh-debug làm chủ chẩn đoán, chỉ mở extension theo nhu cầu.
Concerns/Blockers: License và upstream revision chưa xác minh; runtime/native discovery/human gold chưa chạy. Các giới hạn này không chặn báo cáo compare đã giao, nhưng chặn suy luận sang sao chép, chất lượng runtime hoặc chấp nhận toàn kit.
