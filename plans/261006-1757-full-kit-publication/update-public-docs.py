from pathlib import Path

root = Path(__file__).resolve().parents[2] / 'github-publication'
readme = root / 'README.md'
text = readme.read_text(encoding='utf-8').replace('39', '43').replace('r38', 'r41')
text = text.replace('| Core | 12 |', '| Core | 16 |').replace('9 nhóm', '13 nhóm')
text = text.replace('nckh-kit/scripts/verify-public-package.py', 'scripts/verify-public-package.py')
text = text.replace('--models balanced --dry-run', '--models balanced --with-agents --hooks advisory --dry-run')
text += '''

## Source đầy đủ và rebuild

`nckh-kit/` chứa đầy đủ source được pin ở r41: skills, agents, adapters,
contracts, policies, workflows, profiles, data, hooks, installer, scripts,
test và protocol/case đánh giá. Bốn package có thêm plugin projection;
ứng dụng quản lý việc đăng ký, enable và trust plugin.

```text
python nckh-kit/scripts/build-artifacts.py --all --plugin --resource-access on --check
python nckh-kit/scripts/build-artifacts.py --all --plugin --resource-access on --output dist
```

Output build phải chưa tồn tại hoặc rỗng. Data nguồn dùng để rebuild nằm trong
`nckh-kit/core/profiles/resources/`, cùng registry, provenance, license và notices.
Bốn skill nghiên cứu mới là `nckh-dataset`, `nckh-statistics`, `nckh-telemetry`
và `nckh-aiops`. Xem [tài liệu kit](nckh-kit/docs/index.md) và
[ghi công data](docs/resource-attribution.md).
'''
readme.write_text(text, encoding='utf-8')
path = root / 'docs/public-edition.md'
text = path.read_text(encoding='utf-8').replace('revision 38', 'revision 41').replace('r38', 'r41').replace('39 skill', '43 skill').replace('Chín nhóm', 'Mười ba nhóm').replace('9 nhóm', '13 nhóm').replace('27\nbinding', '35\nbinding')
text = text.replace('Chỉ các resource đã đăng ký trong gói mới được phân phối.', 'Các resource đã đăng ký cùng source, test fixture và protocol/case đánh giá được phân phối; raw trace và kết quả chạy riêng vẫn nằm ngoài repository.')
text = text.replace('Nó không chứa toàn bộ development source để rebuild kit.\nCác chức năng build/freeze còn nằm trong module verifier nguyên bản không phải\nentrypoint được cung cấp cho bản này.', 'Nó chứa toàn bộ source được pin để rebuild kit, kèm scripts build/freeze, test và protocol/case đánh giá. Công cụ verifier public nằm riêng tại `scripts/verify-public-package.py` để giữ inventory source lock đúng. Rebuild mặc định bật resources; chế độ off trong source chỉ phục vụ so sánh nội bộ.')
text += '''

## Data nghiên cứu bổ sung và quyền chia sẻ source

Bản công khai r41 thêm bốn pack do chủ sở hữu tự biên soạn, gồm 14 record:
statistical recipes (3), telemetry fields (3), AIOps benchmark cards (3) và
evaluation recipes (5). Tám binding bổ sung thuộc registry. Pack chứa bản tóm
tắt và tham khảo có nguồn; dataset/pilot, gold labels, predictions và kết quả
đo thực tế thuộc từng project.

Chủ sở hữu cho phép xuất bản toàn bộ source kit và data cần thiết ngày
06/10/2026. Quyền chia sẻ này bổ sung cho phạm vi local ghi trong source lock
và rights record lịch sử, không thay hash hoặc gán giấy phép MIT/Apache cho
mã, instructions hay pack tự biên soạn. Các giấy phép và attribution upstream
tiếp tục áp dụng cho nội dung tương ứng. Xem
[ghi công tài nguyên](resource-attribution.md).
'''
path.write_text(text, encoding='utf-8')
path = root / 'docs/portable-hooks.md'
path.write_text(path.read_text(encoding='utf-8').replace('r38', 'r41').replace('revision 38', 'revision 41'), encoding='utf-8')
path = root / 'docs/resource-attribution.md'
text = path.read_text(encoding='utf-8').replace('r26', 'r41').replace('chín nhóm', 'mười ba nhóm')
text += '''

## Bốn pack tham khảo tự biên soạn

Statistical recipes, telemetry fields, AIOps benchmark cards và evaluation
recipes có 14 record, với tám binding đến consumer. Registry giữ metadata
nguồn, snapshot hash, phạm vi áp dụng và provenance của từng pack.
Xem [rights record](../nckh-kit/core/profiles/resources/research-packs-rights.md),
[attribution](../nckh-kit/core/profiles/resources/research-packs-attribution.md)
và [resource registry](../nckh-kit/core/registry/catalog/resources.json).
Quyền chia sẻ source/data do chủ sở hữu cấp cho lần xuất bản này được ghi tại
[phạm vi bản công khai](public-edition.md); nhãn quyền lịch sử vẫn được giữ nguyên.
'''
path.write_text(text, encoding='utf-8')
