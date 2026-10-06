# Snapshot tham khảo

Các thư mục dưới `resources/` là nguồn tham khảo được tải về workspace, không
phải toàn bộ dependency của kit. Resource được chọn cho package có owner tại
[registry](../nckh-kit/core/registry/catalog/resources.json), kèm provenance và
license trong source được pin.

| Snapshot công khai | Quyền và ghi công |
|---|---|
| [Humanizer](../resources/humanizer-main/) | [LICENSE](../resources/humanizer-main/LICENSE) |
| [LanguageTool](../resources/languagetool-master/) | [COPYING](../resources/languagetool-master/COPYING.txt), cùng notices của từng module |
| [Nature Skills](../resources/nature-skills-main/) | [LICENSE](../resources/nature-skills-main/LICENSE) |
| [Scientific Agent Skills](../resources/scientific-agent-skills-main/) | [LICENSE](../resources/scientific-agent-skills-main/LICENSE.md) |
| [Skills snapshot](../resources/skills-main/) | [Third-party notices](../resources/skills-main/THIRD_PARTY_NOTICES.md), cùng license của từng skill |

Không gán một giấy phép chung cho các snapshot. Nội dung tải về là snapshot
lịch sử; source lock của kit chỉ xác nhận các file được chọn trong kit, không
xác nhận toàn bộ snapshot vẫn tương đương upstream hiện tại.

## ClaudeKit giữ local

Chủ sở hữu chọn giữ hai snapshot ClaudeKit local vì license của nguồn ghi
proprietary/confidential và hạn chế phân phối. Repository chỉ lưu
[license Engineer](reference-notices/claudekit-engineer-main/LICENSE) và
[license Marketing](reference-notices/claudekit-marketing-main/LICENSE).

Các snapshot ở workspace lần lượt mang tên `resources/claudekit-engineer-main/`
và `resources/claudekit-marketing-main/`; nội dung của chúng không được đưa vào
Git. License thuộc ClaudeKit; các file này ghi nhận giới hạn của nguồn, không
cấp quyền dùng hay phân phối snapshot.

Thông tin nguồn được snapshot Engineer chỉ tới
[ClaudeKit](https://github.com/claudekit/claudekit) và
[ClaudeKit Marketing](https://github.com/claudekit/claudekit-marketing).
Snapshot Marketing cũng dẫn tới
[ClaudeKit Engineer](https://github.com/claudekit/claudekit-engineer).
Đây là locator ghi trong README của snapshot, không phải xác nhận quyền truy cập
hoặc trạng thái repo upstream hiện tại.

## Skill tài liệu có giới hạn phân phối

Các thư mục `docx`, `pdf`, `pptx`, `xlsx` trong snapshot Skills cũng được giữ
local: license của từng thư mục ghi all rights reserved và cấm phân phối cho bên
thứ ba. Theo lựa chọn giữ local đối với nguồn hạn chế phân phối, repository chỉ
đăng [license docx](reference-notices/anthropic/docx/LICENSE.txt),
[license pdf](reference-notices/anthropic/pdf/LICENSE.txt),
[license pptx](reference-notices/anthropic/pptx/LICENSE.txt) và
[license xlsx](reference-notices/anthropic/xlsx/LICENSE.txt).
