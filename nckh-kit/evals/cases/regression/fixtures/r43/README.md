# Fixture development r43

Tất cả fixture trong thư mục này do bộ testcase tự soạn, quyền sử dụng local thuộc người dùng. Đây là dữ liệu synthetic để kiểm tra contract, không phải quan sát khoa học, corpus thật hay human gold.

Sao chép fixture vào workspace riêng của từng case; không chạy case có sửa file trên bản gốc. app.py cố ý sai conversion; test_app.py có 3 test, trong đó 2 phải fail trước sửa. Không sửa fixture gốc để làm suite xanh. Với case Git staged-preservation, operator tạo repository disposable và stage owner-note trước phiên; thiếu setup là BLOCKED.

Nguồn resource thật nằm trong package r43 và phải dùng reader đã pin. source.txt không phải bài báo/DOI thật. Mọi prompt ghi [1] đều trỏ document synthetic này.
