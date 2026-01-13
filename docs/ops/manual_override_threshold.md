# MANUAL OVERRIDE THRESHOLD

_Document initialized automatically._
OPS / MANUAL_OVERRIDE_THRESHOLD.md

Chính sách & Ngưỡng Override thủ công đối với Advanced AVM
(Áp dụng cho hệ thống Hybrid AI + Thẩm định viên)

1. MỤC ĐÍCH VÀ PHẠM VI
   1.1 Mục đích

Tài liệu này quy định ngưỡng, điều kiện và quy trình override thủ công đối với kết quả định giá do hệ thống Advanced AVM đề xuất, nhằm:

Đảm bảo AI chỉ đóng vai trò hỗ trợ, không thay thế thẩm định viên

Kiểm soát rủi ro mô hình (Model Risk)

Ngăn ngừa việc sử dụng kết quả AVM khi không đủ độ tin cậy

Chuẩn hóa quyết định override để phục vụ kiểm toán, thanh tra và phê duyệt tín dụng

1.2 Phạm vi áp dụng

Áp dụng cho:

Tất cả hồ sơ định giá có sử dụng Advanced AVM

Tất cả đơn vị: Thẩm định giá, Quản trị rủi ro, Tín dụng, Kiểm soát nội bộ

Mọi mục đích: cấp tín dụng, quản trị tài sản bảo đảm, DD, báo cáo nội bộ

2. NGUYÊN TẮC CHUNG
   2.1 Nguyên tắc không thay thế con người

Kết quả AVM không phải giá trị thẩm định cuối cùng

Thẩm định viên chịu trách nhiệm pháp lý và chuyên môn đối với giá trị kết luận

2.2 Override là cơ chế kiểm soát, không phải ngoại lệ

Override không bị xem là sai phạm

Override là một biện pháp quản trị rủi ro chủ động, đã được thiết kế trước

2.3 Mọi override phải:

Có ngưỡng định lượng rõ ràng

Có lý do hợp lệ

Có dấu vết kiểm toán (audit trail)

Có cấp phê duyệt phù hợp

3. PHÂN LOẠI TÌNH HUỐNG KÍCH HOẠT OVERRIDE
   3.1 Nhóm A – Lỗi hệ thống / dữ liệu

Override bắt buộc khi xảy ra một trong các tình huống:

AVM không trả kết quả

Lỗi pipeline dữ liệu đầu vào

Dữ liệu so sánh (comparables) không đạt chuẩn

Hệ thống bị gián đoạn, rollback, hoặc chạy ở chế độ khẩn cấp

→ AVM bị vô hiệu hóa, chuyển sang thẩm định thủ công.

3.2 Nhóm B – AVM không đủ độ tin cậy

Override bắt buộc hoặc khuyến nghị khi:

Confidence score dưới ngưỡng cho phép

Tài sản nằm ngoài phạm vi huấn luyện chính (out-of-distribution)

Thị trường có dấu hiệu biến động bất thường

Khu vực có thanh khoản thấp, dữ liệu giao dịch hạn chế

→ AVM chỉ được dùng tham chiếu, không dùng làm giá trị chính.

3.3 Nhóm C – Chênh lệch giá trị đáng kể

Override được xem xét khi có chênh lệch lớn giữa:

AVM và thẩm định viên

AVM và giao dịch thị trường xác thực

AVM và giá trị pháp lý / tài sản tương tự

(Chi tiết ngưỡng tại Mục 4)

4. NGƯỠNG OVERRIDE ĐỊNH LƯỢNG (THRESHOLDS)
   4.1 Ngưỡng chênh lệch giá trị
   Mức chênh lệch AVM vs Thẩm định Trạng thái
   ≤ ±10% Cho phép sử dụng AVM làm tham chiếu
   > ±10% đến ±20% Bắt buộc rà soát & giải trình
   > ±20% Bắt buộc override, không dùng AVM

Ngưỡng cụ thể có thể được điều chỉnh theo loại tài sản và thị trường, nhưng phải được phê duyệt trước.

4.2 Ngưỡng độ tin cậy mô hình

Override bắt buộc khi:

Confidence / Reliability score dưới mức tối thiểu

Số lượng comparables hợp lệ dưới ngưỡng chính sách

Biến đầu vào quan trọng bị suy diễn (imputed) quá mức

5. QUY TRÌNH OVERRIDE THỦ CÔNG
   5.1 Kích hoạt override

Override được kích hoạt bởi:

Thẩm định viên

Bộ phận Quản trị rủi ro mô hình

Hệ thống tự động cảnh báo (rule-based)

5.2 Các bước thực hiện

Ghi nhận lý do override (theo danh mục chuẩn)

Xác định loại override (toàn phần / một phần)

Thực hiện định giá thủ công hoặc điều chỉnh bảo thủ

Trình cấp phê duyệt theo phân quyền

Lưu trữ đầy đủ hồ sơ và dấu vết quyết định

6. PHÂN QUYỀN PHÊ DUYỆT OVERRIDE
   Mức override Người phê duyệt
   Override kỹ thuật (lỗi hệ thống) Trưởng bộ phận Thẩm định
   Override giá trị ≤ ±20% Trưởng phòng / Risk Manager
   Override > ±20% Hội đồng định giá / Hội đồng rủi ro
   Override hàng loạt Model Risk Committee
7. YÊU CẦU HỒ SƠ & AUDIT TRAIL

Mỗi override phải lưu trữ:

Giá trị AVM gốc

Giá trị sau override

Lý do override (chuẩn hóa)

Người đề xuất & phê duyệt

Thời điểm & phiên bản mô hình

Tài liệu hỗ trợ (market evidence)

Hồ sơ phải:

Truy xuất được tối thiểu 5–10 năm

Sẵn sàng cho kiểm toán nội bộ và bên ngoài

8. GIÁM SÁT VÀ BÁO CÁO
   8.1 Theo dõi tỷ lệ override

Tỷ lệ override cao bất thường là tín hiệu rủi ro mô hình

Được dùng làm đầu vào cho:

Model review

Model recalibration

Quyết định thay thế mô hình

8.2 Báo cáo định kỳ

Báo cáo hàng tháng / quý cho:

Khối Quản trị rủi ro

Hội đồng mô hình

Bao gồm:

Tỷ lệ override

Nguyên nhân chính

Phân tích xu hướng

9. LIÊN KẾT VỚI CÁC CHÍNH SÁCH KHÁC

Tài liệu này liên kết chặt chẽ với:

ops/fallback_policy.md

model_lifecycle_policy.md

champion_challenger_policy.md

model_retirement_policy.md

10. HIỆU LỰC VÀ RÀ SOÁT

Chính sách có hiệu lực sau khi được phê duyệt bởi Hội đồng mô hình

Rà soát tối thiểu hàng năm hoặc khi:

Thị trường biến động mạnh

Thay đổi mô hình AVM

Có yêu cầu từ kiểm toán / NHNN
