# SYSTEM FAILURE PLAYBOOK

_Document initialized automatically._
Playbook Ứng phó sự cố hệ thống & mất độ tin cậy AVM
(Áp dụng cho Advanced AVM – Hybrid AI + Thẩm định thủ công)

1. MỤC ĐÍCH

Playbook này quy định cách nhận diện, phân loại, xử lý và kiểm soát các tình huống mà hệ thống Advanced AVM:

Gặp lỗi kỹ thuật

Không thể vận hành đúng thiết kế

Không đạt ngưỡng độ tin cậy để hỗ trợ định giá

Mục tiêu nhằm:

Đảm bảo tính liên tục hoạt động nghiệp vụ thẩm định

Ngăn ngừa rủi ro tín dụng và rủi ro mô hình

Đảm bảo tuân thủ kiểm toán, thanh tra và chuẩn quản trị nội bộ

2. PHẠM VI ÁP DỤNG

Áp dụng cho:

Tất cả hệ thống AVM và module liên quan

Toàn bộ hồ sơ định giá sử dụng AVM

Các đơn vị:

Thẩm định giá

Quản trị rủi ro mô hình

CNTT

Kiểm soát nội bộ

Tín dụng

3. NGUYÊN TẮC VẬN HÀNH CỐT LÕI
   3.1 Ưu tiên an toàn hơn tốc độ

Khi xảy ra sự cố:

Dừng sử dụng AVM được ưu tiên hơn tiếp tục vận hành không chắc chắn

Không vì áp lực tiến độ mà sử dụng kết quả không kiểm soát

3.2 Không để AVM quyết định giá

Trong mọi kịch bản sự cố:

AVM không được phép trở thành nguồn giá duy nhất

Quyết định cuối cùng luôn thuộc về thẩm định viên và cấp phê duyệt

3.3 Mọi sự cố đều phải để lại dấu vết

Không xử lý “ngầm”

Không bỏ qua bước ghi nhận và báo cáo

4. PHÂN LOẠI SỰ CỐ HỆ THỐNG
   4.1 Nhóm I – Sự cố kỹ thuật nghiêm trọng

Bao gồm:

Hệ thống không truy cập được

Lỗi pipeline dữ liệu

Lỗi đồng bộ dữ liệu thị trường

Lỗi version / deployment

Mất log hoặc audit trail

Mức độ: Cao
Hành động: Dừng AVM ngay lập tức

4.2 Nhóm II – Sự cố chức năng / độ tin cậy

Bao gồm:

AVM trả kết quả nhưng confidence thấp

Số lượng comparables không đạt chuẩn

Mô hình hoạt động ngoài phạm vi huấn luyện

Cảnh báo drift hoặc instability

Mức độ: Trung bình – Cao
Hành động: Hạn chế sử dụng, kích hoạt override

4.3 Nhóm III – Sự cố thị trường

Bao gồm:

Thị trường đóng băng giao dịch

Biến động giá bất thường

Sự kiện bất khả kháng (dịch bệnh, khủng hoảng, chính sách)

Mức độ: Trung bình
Hành động: Chuyển sang chế độ bảo thủ

5. QUY TRÌNH ỨNG PHÓ SỰ CỐ (END-TO-END)
   5.1 Nhận diện sự cố

Sự cố có thể được phát hiện bởi:

Cảnh báo hệ thống

Thẩm định viên

Bộ phận rủi ro

Kiểm toán nội bộ

5.2 Kích hoạt chế độ sự cố

Ngay khi xác định sự cố:

Gắn cờ hồ sơ là “AVM Unreliable / System Issue”

Tạm ngừng sử dụng kết quả AVM cho quyết định chính

5.3 Phân luồng xử lý
Loại sự cố Hướng xử lý
Kỹ thuật Fallback 100% thủ công
Độ tin cậy Override có kiểm soát
Thị trường Định giá bảo thủ 6. CƠ CHẾ FALLBACK & OVERRIDE
6.1 Fallback hoàn toàn

Áp dụng khi:

AVM không hoạt động

Không thể xác minh dữ liệu

Không có audit trail hợp lệ

→ AVM bị vô hiệu hóa hoàn toàn

6.2 Override có kiểm soát

Áp dụng khi:

AVM hoạt động nhưng không đáng tin cậy

Chênh lệch giá vượt ngưỡng chính sách

Thị trường biến động mạnh

→ AVM chỉ được dùng làm tham chiếu phụ

6.3 Chế độ định giá bảo thủ

Áp dụng khi:

Thiếu dữ liệu thị trường

Thanh khoản thấp

Rủi ro vĩ mô tăng cao

→ Áp dụng giả định thận trọng, có biên an toàn

7. PHÂN CÔNG TRÁCH NHIỆM
   7.1 Thẩm định viên

Phát hiện & báo cáo sự cố

Không sử dụng AVM khi bị cấm

Thực hiện định giá thủ công thay thế

7.2 Bộ phận CNTT

Khắc phục lỗi kỹ thuật

Báo cáo nguyên nhân gốc (RCA)

Đảm bảo log & dữ liệu được bảo toàn

7.3 Quản trị rủi ro mô hình

Đánh giá tác động sự cố

Quyết định phạm vi vô hiệu hóa AVM

Đề xuất recalibration hoặc retirement

8. GHI NHẬN & BÁO CÁO SỰ CỐ

Mỗi sự cố phải được ghi nhận:

Thời điểm phát sinh

Loại sự cố

Hồ sơ bị ảnh hưởng

Biện pháp xử lý

Người phê duyệt

Báo cáo:

Ngay lập tức đối với sự cố nghiêm trọng

Tổng hợp định kỳ cho Hội đồng mô hình

9. LIÊN KẾT VỚI QUẢN TRỊ VÒNG ĐỜI MODEL

Sự cố lặp lại hoặc nghiêm trọng là căn cứ để:

Đánh giá lại mô hình

Kích hoạt champion–challenger

Quyết định tạm dừng hoặc loại bỏ model

10. KIỂM TOÁN & TUÂN THỦ

Playbook này:

Là tài liệu bắt buộc trong audit AVM

Được sử dụng làm bằng chứng:

Không lạm dụng AI

Có kiểm soát rủi ro chủ động

Phải được rà soát tối thiểu hàng năm

11. HIỆU LỰC

Có hiệu lực sau khi được phê duyệt bởi:

Hội đồng quản trị rủi ro mô hình

Áp dụng thống nhất toàn hệ thống

📌 NGUYÊN TẮC KIỂM SOÁT CUỐI

Hệ thống AVM tốt không phải là hệ thống không bao giờ lỗi,
mà là hệ thống biết dừng đúng lúc và chuyển quyền cho con người.
