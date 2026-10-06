# Review installer/build hiện tại

## Phạm vi

- Đọc: `nckh-kit/core/install.py`, `nckh-kit/core/build.py`, `nckh-kit/core/paths.py`.
- Đối chiếu: `plans/260930-1910-nckh-portable-skill-kit/installer-evaluation-migration.md`, catalog/schema và test transaction hiện có.
- Review tĩnh trên source hiện tại; không chạy install, provider, host mutation hay process kill. Một lần probe build vào thư mục tạm bị sandbox từ chối quyền ghi trước khi build chạy, nên các kết luận dưới đây dựa trên control flow và fixture logic, không ghi nhận runtime pass giả.

## Kết luận

Bản hiện tại đã có các cải thiện đáng kể: lock theo physical target được truyền vào commit/uninstall, journal uninstall, deep copy của `index_before`, kiểm tra target thay đổi và kiểm tra volume lexical trước commit. Tuy vậy P6 chưa đủ an toàn để promote: có một đường path traversal từ manifest metadata đi thẳng tới `plan_install`, một đường ghi ngoài target root từ plan không được xác thực ở commit boundary, và các recovery/concurrency window có thể làm mất ownership hoặc làm state lệch với filesystem.

## Findings

### 1. Critical — skill ID trong manifest có thể thoát bundle và target root

**Vị trí:** `nckh-kit/core/build.py:186-205`; `nckh-kit/core/install.py:115-132`.

`verify_bundle()` chỉ kiểm tra `manifest["files"]`, file hashes và local links. Nó không validate `manifest["skills"]`, không yêu cầu skill ID là một path component an toàn, và không đối chiếu `skills[*].id`/`tree_hash` với các record trong `files`. Sau đó `plan_install()` dùng metadata đó trực tiếp:

```python
source = Path(target["bundle"]) / "skills" / skill
path = Path(target["root"]) / skill
```

Không có `contained()` hoặc guard `..`, `/`, `\\`, `:` cho `skill`. Một bundle có `manifest.json` hợp lệ theo các kiểm tra hiện tại nhưng chứa `id: "../../outside"` có thể khiến `tree_hash(source)` đọc thư mục ngoài bundle và `physical_path` trỏ ngoài root. Khi entry là `create`, `commit_install()` vẫn có thể `mkdir` parent và `os.replace()` stage vào path đó; `safe_remove_owned()` chỉ xuất hiện trong rollback, sau destructive write, và không bảo vệ success path.

**Tác động:** bundle metadata lỗi/tamper có thể làm installer copy một cây thư mục ngoài package vào vị trí ngoài `.agents/skills`/host root. Đây vi phạm trực tiếp yêu cầu path traversal/symlink escape phải fail trước destructive write và có thể ghi đè dữ liệu user nếu path ngoài root đã tồn tại dưới một plan phù hợp.

**Repro logic:** giữ nguyên `manifest["files"]` và `closure_hash`, thêm một skill record được chọn bởi kit với `id="../../victim"` và tree hash của cây source tương ứng; `verify_bundle()` không chặn, `plan_install()` tạo `physical_path = <target-root>/../../victim`, rồi commit không kiểm tra containment theo từng entry.

**Khuyến nghị:** validate manifest bằng schema riêng trước khi dùng; skill ID phải là tên đơn không chứa separator, `.`, `..`, drive/colon và phải đối chiếu với record file. Ở cả `plan_install()` lẫn `commit_install()`, dùng `contained(bundle, "skills/" + skill)` và `contained(target_root, skill)`, rồi yêu cầu kết quả là directory có tree hash đúng. Commit boundary không được tin plan đã tạo ở bước trước.

### 2. High — commit boundary không xác thực `physical_path` theo roots được cấp

**Vị trí:** `nckh-kit/core/install.py:269-317`.

`commit_install()` kiểm tra `plan["roots"]` cho volume, tạo lock cho các root đó, nhưng trong vòng commit chỉ lấy `target = Path(entry["physical_path"])`. Không có kiểm tra `target.parent` phải là một root được cấp, không có `contained(root, entry["skill"])`, và không có kiểm tra tên child trước `target.parent.mkdir()`/`os.replace()`.

**Tác động:** bất kỳ caller nào đưa plan đã deserialize, cache cũ, hoặc plan bị sửa có thể ghi thành công ra path ngoài target roots. Guard rollback không cứu được success path; transaction sẽ ghi ownership cho path ngoài nếu phần còn lại thành công. Đây là một failure độc lập với finding 1: ngay cả manifest an toàn cũng không làm `commit_install()` trở thành API boundary an toàn.

**Repro logic:** tạo plan có `roots=[<safe-root>]`, `conflicts=[]`, entry `physical_path=<safe-root-parent>/victim/nckh-x` hoặc một thư mục hoàn toàn ngoài root, `before_hash=None`, `mode="copy"` và source là cây bundle hợp lệ. Commit hiện tại khóa safe root nhưng vẫn tạo parent và rename stage vào path trong entry.

**Khuyến nghị:** chuẩn hóa và validate toàn bộ entry trước khi tạo journal hoặc stage: canonical target phải nằm đúng trong một root, parent phải đúng root trực tiếp, skill name phải là tên được phép, target/source đều phải qua `no_links()`. Nếu có entry không đạt, dừng trước mọi write.

### 3. High — stale uninstall snapshot có thể xoá shared target và làm mất owner mới

**Vị trí:** `nckh-kit/core/install.py:338-387`.

`uninstall()` đọc `ownership.json`, tìm `install`, tính toàn bộ `actions` và hash trước khi lấy `target_lock()` ở dòng 355. Sau khi lock được lấy, code chỉ gọi `recover_outstanding()` rồi tiếp tục dùng `index`, `install` và `actions` cũ; không đọc lại ownership manifest hoặc re-plan theo state dưới lock.

**Repro logic:**

1. State có item `nckh-plan` với owner A, hash hiện tại còn nguyên.
2. Process U gọi `uninstall(A)` và tính action `remove`, nhưng bị dừng ngay trước `target_lock()`.
3. Process I lấy cùng target lock, cài owner B (cùng bytes là đủ), ghi `ownership.json` với owners A+B, rồi unlock.
4. U lấy lock, vẫn dùng snapshot A-only, `os.replace(entry["path"], backup)` và ghi snapshot cũ sau khi loại A.

Kết quả là target shared bị chuyển khỏi host dù B còn owner; ownership của B cũng bị mất trong manifest state. Lock physical root hiện tại chỉ bảo vệ đoạn mutation, không bảo vệ khoảng cách giữa discover/plan và commit của uninstall.

**Khuyến nghị:** với uninstall thật, lấy target/state lock trước khi đọc index và tính actions; đọc lại index dưới lock, kiểm tra `install_id`, owners, current hash và target roots rồi mới journal/commit. Dry-run có thể chạy ngoài lock nhưng phải yêu cầu re-preview khi commit nếu snapshot đã stale.

### 4. High — lock có ownership nhưng crash để lại lock vĩnh viễn, chặn recovery

**Vị trí:** `nckh-kit/core/install.py:179-215` (`exclusive_lock()` và `target_lock()`), `:269-276` và `:355-357`.

`exclusive_lock()` tạo file bằng `O_EXCL`, ghi PID/nonce rồi chỉ unlink trong `finally`. Nếu process bị kill/crash sau `os.open()` hoặc trong bất kỳ đoạn commit/uninstall nào, `finally` không chạy. Lần chạy sau chỉ gặp `FileExistsError` và báo “inspect its owner and journal”; không có code nào kiểm tra PID chết, nonce/journal hợp lệ, hay gọi `recover_outstanding()` trước khi cần lock. Vì `recover_outstanding()` chỉ được gọi sau khi toàn bộ lock acquisition thành công, journal `committing` không thể tự phục hồi khi lock stale.

**Tác động:** một interruption đúng tại lock window khiến target và state bị kẹt vĩnh viễn cho đến khi người dùng tự xoá lock bằng thao tác ngoài contract. Điều này không đáp ứng yêu cầu re-run sau crash và recovery có ownership; cũng có thể khiến người dùng xoá lock nhầm khi owner thật còn chạy.

**Khuyến nghị:** ghi owner record theo protocol crash-safe, thêm một operation recovery/doctor có lock riêng để xác định PID/host còn sống và journal tương ứng, chỉ reclaim lock khi chứng minh owner đã chết hoặc có explicit recovery decision. Nếu không thể reclaim an toàn, báo pending có đường recovery được hỗ trợ thay vì để mọi operation fail vô hạn.

### 5. High — rollback xoá target trước khi xác nhận backup tồn tại; conflict có thể làm mất cây đang có

**Vị trí:** `nckh-kit/core/install.py:228-261`.

Trong `rollback()`, khi `current` là `after_hash`, code gọi `safe_remove_owned(target, allowed_roots)` ở dòng 244 trước khi kiểm tra backup. Nếu `before_hash` khác `None` nhưng backup đã bị xoá/không còn tồn tại, nhánh sau chỉ append conflict ở dòng 251 rồi raise. Target `after_hash` đã bị xoá nhưng bản before không được phục hồi; nếu target đang là bản duy nhất còn đọc được thì rollback đã gây data loss trong lúc báo rằng nó đang bảo toàn conflict.

**Repro logic:** journal có một change với `before_hash=H_old`, `after_hash=H_new`, `backup="transactions/.../backup-0"`; đặt target về H_new và xoá backup; gọi `rollback()`. Hàm remove target, đặt status `rollback-conflict`, rồi raise. Không có bước khôi phục target hoặc giữ nguyên H_new khi backup không tồn tại.

**Khuyến nghị:** kiểm tra và hash-validate backup trước mọi remove. Nếu backup thiếu hoặc không khớp, giữ nguyên target hiện tại, ghi conflict/pending và không thực hiện destructive action. Chỉ remove target sau khi đã chứng minh có bản phục hồi hoặc target chắc chắn là file mới với `before_hash=None`.

### 6. High — rollback conflict có thể để ownership manifest ở trạng thái nửa cũ/nửa mới

**Vị trí:** `nckh-kit/core/install.py:252-261` và `:326-334`.

`rollback()` ghi `journal["status"] = "rollback-conflict"`, sau đó raise ngay nếu có conflict; chỉ khi không có conflict mới ghi `journal["index_before"]` trở lại `ownership.json` ở dòng 259. Có cửa sổ hợp lệ trong đó commit/uninstall đã ghi `ownership.json` mới nhưng process chết trước khi journal chuyển `committed`, rồi user chỉnh một target. Recovery gặp external edit, giữ target đó, rollback các target còn lại, nhưng không restore index cũ.

**Tác động:** filesystem có thể đã rollback một phần trong khi ownership vẫn quảng bá transaction mới; lần doctor/uninstall sau đó có thể dùng owner/hash không còn tương ứng, đặc biệt nguy hiểm khi một target đã bị giữ lại do user edit.

**Khuyến nghị:** khi conflict, ghi một state machine/pending record chứa index hiện tại và từng change; không để index mới được coi là committed. Hoặc restore `index_before` atomically trước khi trả trạng thái `rollback-conflict`, đồng thời lưu danh sách target conflict để user quyết định merge/keep/replace.

### 7. High — engine tự promote candidate khác content mà không có update authorization/provenance

**Vị trí:** `nckh-kit/core/install.py:72-75`, `:103-164`, `:326-334`.

`install_identity()` chỉ dựa trên surfaces, roots và scope. Khi item đã owned và current hash vẫn bằng hash cũ, `plan_install()` chọn action `replace` ngay khi `final_hash` khác (`current_hash == old["tree_hash"]` rồi rơi vào nhánh replace), không có trường `operation=update`, candidate ID, package/source/adapter version hay affected-eval receipt. `commit_install()` cũng chỉ kiểm `plan["conflicts"]`, nên một caller đang thực hiện `install` có thể đưa bundle mới vào và promote thẳng nội dung.

State sau commit chỉ lưu scope/surfaces/kits/roots/mode trong `index["installs"]`; nó không lưu package version, source-lock hash, adapter revision, closure hash hoặc provenance của candidate. Vì vậy lần chạy sau không thể chứng minh đây là update đã được user gọi/chọn hay candidate đến từ source/eval phù hợp.

**Repro logic:** install bundle A; gọi lại cùng flow với bundle B khác `closure_hash`/source nhưng cùng skill IDs, không truyền `replace_skills`, `keep_edited` hay cờ update. Plan trả `replace` cho mọi skill chưa bị edit và commit thay thế chúng.

**Tác động:** cài lần đầu và update bị trộn quyền; candidate mới có thể được promote mà không qua gate provenance/affected eval, trái yêu cầu “update không có quyền qua việc cài lần đầu” và “user gọi/chọn update rồi mới promote”.

**Khuyến nghị:** thêm operation/authorization vào plan và commit; `install` phải reject changed owned content, còn `update` mới được tiếp tục sau preview xác nhận. Persist package/source-lock/adapter/closure hashes và candidate receipt trong install manifest để kiểm tra nguồn và stale candidate.

### 8. Medium — kiểm tra khác volume hiện chỉ dùng drive anchor; Unix khác mount vẫn vỡ ở `os.replace()`

**Vị trí:** `nckh-kit/core/install.py:269-276`, `:307-312`, và uninstall `:372-378`.

Commit mới kiểm tra `Path(root).anchor` với `state_dir.anchor`. Trên Linux/macOS, mọi absolute path thường có anchor `/` dù state và project nằm trên hai filesystem/mount khác nhau; trên Windows, cùng drive letter cũng không đảm bảo cùng volume/reparse boundary. Sau đó stage/backup vẫn dùng `os.replace()` giữa `state_dir/transactions/...` và target.

**Tác động:** create/update hoặc uninstall có thể fail với `EXDEV` sau khi journal đã bắt đầu. Với commit, lỗi thường rollback an toàn; với uninstall không có preflight tương đương và lỗi xảy ra trong transaction. Đây là failure có thể tái hiện bằng state trên một mount và project trên mount khác, trái yêu cầu installer project/global chạy được trên các OS.

**Khuyến nghị:** so sánh `st_dev`/volume thực của state và từng target trước journal; nếu khác thì stage/backup cạnh target trên cùng filesystem hoặc fail rõ trong dry-run trước mọi mutation. Áp dụng cùng preflight cho uninstall.

### 9. Medium — build ghi trực tiếp vào output; lỗi giữa chừng để lại candidate rác chặn mọi lần build sau

**Vị trí:** `nckh-kit/core/build.py:125-183`.

`build_host()` chỉ kiểm tra output rỗng ở đầu, rồi `mkdir` và ghi từng file bằng `destination.write_bytes()` trước khi ghi manifest cuối. Không có temporary output sibling, journal, rollback hoặc cleanup khi closure/secret/link/hash check ném exception giữa vòng lặp. Output partial trở thành non-empty; lần gọi lại cùng path dừng ngay ở dòng 127 với “build destination must be empty”, dù candidate trước đó chưa từng là artifact verified.

**Tác động:** interruption hoặc một file lỗi giữa build làm release candidate bị kẹt và buộc caller tự dọn thư mục; nếu wrapper nhìn thấy directory này như candidate thì dễ nhầm artifact chưa được verify với bundle usable.

**Khuyến nghị:** build vào thư mục tạm cùng volume, verify đầy đủ, rồi rename atomically vào output chỉ khi output còn trống; nếu lỗi thì dọn temp theo owner. Giữ candidate cũ nguyên vẹn và phân biệt rõ partial/pending với verified artifact.

## Những điểm đã kiểm tra và không ghi là finding

- `keep_edited` hiện giữ lại baseline hash cũ trong record; uninstall sẽ thấy hash user edit khác baseline và giữ residue, nên không quy kết lỗi xoá edit ở nhánh này.
- Lock theo physical root và `deepcopy(index)` là cải thiện đúng hướng; vấn đề còn lại là acquisition/recovery và stale snapshot nêu trên.
- `safe_remove_owned()` có kiểm tra exact parent, tên `nckh-` và link/junction cho rollback; kiểm tra tương tự vẫn chưa được áp dụng ở success path của `commit_install()` và uninstall.

## Câu hỏi còn mở

- Wrapper có đảm bảo package manifest chỉ đến từ build local đã được xác thực nguồn, hay người dùng có thể chọn/forward một bundle directory bất kỳ? Nếu có bundle ngoài trust boundary, finding 1 phải được xử lý như blocker trước mọi install.
- State directory có được chọn cùng volume với từng project/global target trong UX không? Nếu có, cần chứng minh bằng resolved device/volume, không chỉ drive anchor.

Status: DONE_WITH_CONCERNS
Summary: Review độc lập hoàn tất; hiện còn hai đường path-safety có thể ghi ngoài root, recovery lock/rollback chưa crash-safe, uninstall có stale snapshot race, và build output không transactional.
Concerns/Blockers: Source còn đang được root chỉnh đồng thời; line evidence là bản đọc tại thời điểm review. Native host/model/OS acceptance chưa được thực hiện theo phạm vi được giao.
