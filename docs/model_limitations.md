# MODEL LIMITATIONS

_Document initialized automatically._

# GIỚI HẠN MÔ HÌNH & PHẠM VI ĐỘ TIN CẬY

_(Advanced AVM – Hệ thống định giá kết hợp AI và thẩm định thủ công)_

---

## 1. MỤC ĐÍCH TÀI LIỆU

Tài liệu này quy định **các giới hạn, điều kiện kém tin cậy và phạm vi sử dụng hợp lệ** của Hệ thống Định giá Tự động Nâng cao (Advanced AVM).

Mục tiêu của tài liệu:

- Ngăn chặn việc sử dụng sai hoặc lạm dụng kết quả AI
- Cung cấp minh bạch cho ngân hàng, kiểm toán và cơ quan quản lý
- Xác định rõ các trường hợp **bắt buộc can thiệp của con người**
- Làm tài liệu chính thức trong khuôn khổ **Quản trị rủi ro mô hình (Model Risk Management – MRM)**

Tài liệu này là **bắt buộc** đối với:

- Bộ phận tín dụng
- Hội đồng phê duyệt mô hình
- Bộ phận quản trị rủi ro
- Kiểm toán nội bộ
- Kiểm toán độc lập
- Hội đồng thẩm định giá

---

## 2. NGUYÊN TẮC NỀN TẢNG

Hệ thống Advanced AVM được xây dựng trên các nguyên tắc không thay đổi sau:

- AI **không thay thế thẩm định viên**
- Kết quả mô hình **chỉ mang tính hỗ trợ**
- Kết luận định giá cuối cùng **thuộc trách nhiệm con người**
- Mức độ không chắc chắn **phải được công bố rõ ràng**
- Không được che giấu hoặc làm mờ rủi ro mô hình

Hệ thống **chủ động loại trừ** các quan niệm sau:

- “Định giá hoàn toàn tự động”
- “AI quyết định giá trị tài sản”
- “Giá do model sinh ra là giá trị pháp lý”

---

## 3. PHẠM VI ÁP DỤNG

Tài liệu này áp dụng cho **toàn bộ hệ sinh thái mô hình**, bao gồm nhưng không giới hạn:

- Nhóm mô hình đánh giá độ tin cậy & gian lận
- Nhóm mô hình trích xuất đặc trưng
- Nhóm mô hình định giá lõi (Hedonic, So sánh, Chi phí, Thu nhập)
- Nhóm mô hình tổng hợp & ensemble
- Nhóm mô hình rủi ro
- Nhóm mô hình ước lượng độ tin cậy (confidence)

**Các thành phần LLM không tham gia định giá** và được điều chỉnh riêng theo `llm_usage_policy.md`.

---

## 4. GIỚI HẠN TỔNG QUÁT CỦA HỆ THỐNG

Hệ thống AVM có độ tin cậy suy giảm đáng kể trong các điều kiện sau:

- Dữ liệu giao dịch khan hiếm hoặc chất lượng thấp
- Thị trường xảy ra đứt gãy cấu trúc
- Bất ổn pháp lý hoặc quy hoạch
- Biến động thị trường cực đoan
- Tài sản nằm ngoài phạm vi dữ liệu huấn luyện

Trong các trường hợp này:

- Kết quả mô hình **không được xem là kết luận**
- Chỉ được sử dụng như **chỉ báo tham khảo ban đầu**

---

## 5. GIỚI HẠN LIÊN QUAN ĐẾN DỮ LIỆU

### 5.1 Dữ liệu giao dịch

Hệ thống định giá dựa chủ yếu vào dữ liệu giao dịch lịch sử.

Độ tin cậy giảm mạnh khi:

- Có ít hơn 3 giao dịch so sánh phù hợp
- Giao dịch quá cũ so với thời điểm định giá
- Giao dịch không mang tính thị trường
- Giá giao dịch không minh bạch

Hệ quả:

- Mô hình so sánh bị sai lệch
- Hệ số hedonic không ổn định
- Confidence score bắt buộc phải giảm

---

### 5.2 Dữ liệu tin rao

Dữ liệu tin rao tiềm ẩn nhiều rủi ro:

- Giá chào không phản ánh giá giao dịch
- Trùng lặp tin
- Mô tả sai sự thật
- Thông tin bị thổi phồng

Mô hình kiểm soát chỉ **giảm thiểu**, không thể loại bỏ hoàn toàn.

**Tin rao không bao giờ được coi là giao dịch.**

---

### 5.3 Dữ liệu pháp lý

Mô hình kém tin cậy khi:

- Pháp lý chưa rõ ràng
- Quy hoạch chưa ổn định
- Hồ sơ sở hữu không đầy đủ

Hệ thống **không thay thế thẩm tra pháp lý**.

---

### 5.4 Dữ liệu hình ảnh

Hạn chế chính:

- Ảnh không phản ánh toàn bộ tài sản
- Góc chụp có chọn lọc
- Không thể thay thế khảo sát thực địa

Điểm condition chỉ mang tính **ước lượng sơ bộ**.

---

## 6. GIỚI HẠN THEO CẤU TRÚC THỊ TRƯỜNG

### 6.1 Thị trường thanh khoản thấp

Khi:

- Giao dịch thưa thớt
- Thời gian bán kéo dài
- Giá phụ thuộc đàm phán

Model dễ:

- Phản ứng quá mức
- Sai lệch do dữ liệu ít

Bắt buộc ưu tiên thẩm định thủ công.

---

### 6.2 Thị trường vi mô phức tạp

Trong khu nội đô:

- Mỗi ngõ, mỗi đoạn phố có giá khác nhau
- Yếu tố phi định lượng chi phối mạnh

Model không thể thay thế kinh nghiệm địa phương.

---

### 6.3 Thị trường biến động mạnh

Trong các giai đoạn:

- Sốt giá
- Đóng băng
- Can thiệp chính sách đột ngột

Dữ liệu lịch sử **mất hiệu lực tạm thời**.

---

## 7. GIỚI HẠN THEO LOẠI TÀI SẢN

### 7.1 Tài sản đặc thù

Model hoạt động kém với:

- Nhà thiết kế độc bản
- Tài sản pha trộn công năng
- Tài sản có tiềm năng phát triển chưa hiện thực

---

### 7.2 Tài sản phát triển trong tương lai

Hệ thống:

- Không dự báo giá sau phát triển
- Không định giá kỳ vọng đầu cơ
- Không mô phỏng xác suất duyệt quy hoạch

---

### 7.3 Tài sản cho thuê

Mô hình thu nhập không phù hợp khi:

- Giá thuê không minh bạch
- Hợp đồng thuê không ổn định
- Thị trường thuê phi chính thức

---

## 8. GIỚI HẠN THEO TỪNG NHÓM MÔ HÌNH

### 8.1 Mô hình Hedonic

Hạn chế:

- Phụ thuộc giả định tuyến tính
- Nhạy cảm với đa cộng tuyến
- Kém thích nghi khi dữ liệu ít

---

### 8.2 Mô hình so sánh

Hạn chế:

- Phụ thuộc chất lượng TSSS
- Trọng số điều chỉnh mang tính chủ quan

---

### 8.3 Mô hình chi phí

Hạn chế:

- Không phản ánh tâm lý thị trường
- Có thể làm cao giá trong thị trường suy giảm

---

### 8.4 Mô hình ensemble

Lưu ý:

- Ensemble không đảm bảo đúng
- Có thể che giấu lỗi mô hình con
- Chỉ cải thiện độ ổn định, không loại bỏ rủi ro

---

## 9. GIỚI HẠN CỦA CONFIDENCE SCORE

Confidence score:

- Không phải xác suất đúng
- Không phản ánh rủi ro pháp lý
- Không bao hàm sự kiện bất thường

Confidence cao ≠ đúng tuyệt đối  
Confidence thấp ≠ sai

---

## 10. GIỚI HẠN CỦA MÔ HÌNH RỦI RO

Mô hình rủi ro:

- Đánh giá tương đối, không tuyệt đối
- Không dự báo bán cưỡng bức
- Không mô phỏng khủng hoảng bất thường

---

## 11. TRƯỜNG HỢP BẮT BUỘC OVERRIDE THỦ CÔNG

Override bắt buộc khi:

- Confidence thấp hơn ngưỡng
- Pháp lý chưa rõ
- Thị trường bất thường
- Tài sản đặc thù
- Model và thẩm định viên lệch đáng kể
- Có cảnh báo kiểm toán / tuân thủ

Override phải:

- Có lý do rõ ràng
- Lưu vết
- Phê duyệt theo maker–checker

---

## 12. CÁC TRƯỜNG HỢP KHÔNG ĐƯỢC PHÉP SỬ DỤNG

Hệ thống **không dùng cho**:

- Tranh chấp pháp lý
- Tính thuế
- Bồi thường thu hồi đất
- Định giá phá sản
- Đầu cơ ngắn hạn
- Cam kết giá cho khách hàng

---

## 13. CÔNG BỐ BẮT BUỘC TRONG BÁO CÁO

Mọi báo cáo phải nêu rõ:

- Giới hạn mô hình
- Hạn chế dữ liệu
- Giả định
- Mức độ bất định

Che giấu giới hạn = vi phạm kiểm soát nội bộ.

---

## 14. TUYÊN BỐ TRÁCH NHIỆM

Trách nhiệm định giá thuộc về:

- Thẩm định viên
- Người phê duyệt
- Hội đồng tín dụng

AI **không chịu trách nhiệm pháp lý**.

---

## 15. RÀ SOÁT & CẬP NHẬT

Tài liệu này:

- Rà soát hàng năm
- Cập nhật khi thay đổi mô hình
- Phê duyệt bởi Hội đồng Quản trị Mô hình

---

## 16. KẾT LUẬN CUỐI

Hệ thống Advanced AVM nhằm:

- Giảm rủi ro vận hành
- Chuẩn hóa quy trình
- Hỗ trợ thẩm định viên

Không nhằm:

- Loại bỏ bất định
- Thay thế con người
- Tạo “giá đúng tuyệt đối”

Việc thừa nhận giới hạn là **biện pháp kiểm soát bắt buộc**, không phải điểm yếu.

---
