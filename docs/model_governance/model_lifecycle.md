# MODEL LIFECYCLE

_Document initialized automatically._

# MODEL LIFECYCLE MANAGEMENT POLICY

## Chính sách Quản trị Vòng đời Mô hình

_(Advanced AVM – Hybrid AI + Thẩm định thủ công)_

---

## 1. Mục đích tài liệu

Tài liệu này quy định **khung quản trị vòng đời mô hình (Model Lifecycle Management – MLM)** áp dụng cho hệ thống Advanced AVM, nhằm:

- Đảm bảo mọi mô hình được:
  - Đề xuất
  - Phê duyệt
  - Vận hành
  - Giám sát
  - Thay đổi
  - Loại bỏ  
    theo quy trình kiểm soát thống nhất
- Giảm thiểu rủi ro mô hình, rủi ro tuân thủ và rủi ro vận hành
- Làm căn cứ cho:
  - Hồ sơ phê duyệt nội bộ
  - Kiểm toán nội bộ / kiểm toán độc lập
  - Thanh tra, giám sát ngân hàng

---

## 2. Phạm vi áp dụng

Chính sách này áp dụng cho:

- Toàn bộ mô hình trong hệ thống Advanced AVM, bao gồm:
  - Mô hình định giá (AVM core)
  - Mô hình hỗ trợ (filter, scoring, segmentation)
  - Mô hình giám sát và cảnh báo
  - Mô hình AI/ML và mô hình quy tắc
  - LLM sử dụng cho mục đích hỗ trợ diễn giải
- Tất cả đơn vị liên quan:
  - Khối Thẩm định giá
  - Khối Quản trị rủi ro
  - Khối CNTT / Dữ liệu
  - Khối Tuân thủ
  - Kiểm toán nội bộ

Không áp dụng cho:

- Ý kiến chuyên môn độc lập của thẩm định viên
- Quyết định tín dụng cuối cùng

---

## 3. Nguyên tắc quản trị vòng đời mô hình

---

### 3.1 Nguyên tắc trách nhiệm cuối cùng

- Mô hình không phải chủ thể chịu trách nhiệm
- Trách nhiệm cuối cùng thuộc về:
  - Đơn vị sử dụng mô hình
  - Cá nhân phê duyệt kết quả định giá
  - Hội đồng phê duyệt mô hình (nếu áp dụng)

---

### 3.2 Nguyên tắc kiểm soát theo rủi ro

- Mức độ kiểm soát phụ thuộc vào:
  - Phân loại rủi ro mô hình
  - Mục đích sử dụng
  - Mức độ ảnh hưởng tín dụng
- Không áp dụng cơ chế “một khuôn cho tất cả”

---

### 3.3 Nguyên tắc độc lập chức năng

- Phát triển ≠ Validation ≠ Phê duyệt ≠ Vận hành
- Các vai trò phải được tách biệt phù hợp quy mô tổ chức

---

### 3.4 Nguyên tắc minh bạch & truy vết

- Mọi giai đoạn trong vòng đời mô hình phải:
  - Có tài liệu
  - Có hồ sơ phê duyệt
  - Có khả năng truy vết và tái lập

---

## 4. Định nghĩa vòng đời mô hình

Vòng đời mô hình trong Advanced AVM bao gồm các giai đoạn:

1. Khởi tạo & Đề xuất
2. Thiết kế & Phát triển
3. Thẩm định độc lập (Model Validation)
4. Phê duyệt đưa vào sử dụng
5. Triển khai & vận hành
6. Giám sát & đánh giá định kỳ
7. Thay đổi / hiệu chỉnh
8. Tạm dừng / loại bỏ (Decommission)

---

## 5. Giai đoạn 1 – Khởi tạo & Đề xuất mô hình

---

### 5.1 Khi nào cần đề xuất mô hình

Mô hình mới được đề xuất trong các trường hợp:

- Nhu cầu nghiệp vụ mới
- Mở rộng phạm vi sử dụng AVM
- Thay đổi đáng kể của thị trường bất động sản
- Yêu cầu từ kiểm toán, thanh tra
- Mô hình hiện tại không còn phù hợp

---

### 5.2 Hồ sơ đề xuất tối thiểu

Hồ sơ đề xuất phải bao gồm:

- Mục đích sử dụng cụ thể
- Phạm vi áp dụng
- Đối tượng tài sản
- Vai trò của mô hình trong quy trình định giá
- Phân loại rủi ro dự kiến
- Rủi ro tiềm ẩn và biện pháp kiểm soát

---

### 5.3 Trách nhiệm

- Đơn vị đề xuất chịu trách nhiệm:
  - Tính cần thiết của mô hình
  - Phù hợp với chiến lược quản trị rủi ro

---

## 6. Giai đoạn 2 – Thiết kế & Phát triển

---

### 6.1 Nguyên tắc phát triển

- Phát triển phù hợp mục đích đã được phê duyệt
- Không mở rộng chức năng ngoài phạm vi đề xuất
- Không thiết kế mô hình thay thế vai trò thẩm định viên

---

### 6.2 Tài liệu bắt buộc

- Mô tả mô hình
- Giả định chính
- Giới hạn mô hình
- Dữ liệu sử dụng (ở mức khái niệm)
- Cách sử dụng dự kiến

---

## 7. Giai đoạn 3 – Thẩm định độc lập (Model Validation)

---

### 7.1 Mục tiêu validation

- Đánh giá mức độ phù hợp với mục đích sử dụng
- Đánh giá rủi ro mô hình
- Xác định giới hạn và điều kiện sử dụng an toàn

---

### 7.2 Nguyên tắc validation

- Độc lập với đội phát triển
- Không chỉ tập trung vào kết quả
- Đánh giá toàn diện:
  - Giả định
  - Phạm vi áp dụng
  - Rủi ro tiềm ẩn

---

### 7.3 Mức độ validation theo rủi ro

| Cấp rủi ro | Mức độ validation             |
| ---------- | ----------------------------- |
| Low        | Validation nghiệp vụ          |
| Medium     | Validation nghiệp vụ + rủi ro |
| High       | Validation độc lập đầy đủ     |

---

## 8. Giai đoạn 4 – Phê duyệt đưa vào sử dụng

---

### 8.1 Thẩm quyền phê duyệt

- Phụ thuộc vào phân loại rủi ro mô hình
- Có thể bao gồm:
  - Quản lý đơn vị
  - Hội đồng phê duyệt mô hình
  - Cấp có thẩm quyền cao hơn

---

### 8.2 Nội dung phê duyệt

- Mục đích sử dụng rõ ràng
- Phạm vi và giới hạn sử dụng
- Điều kiện vận hành
- Cơ chế giám sát
- Điều kiện tạm dừng hoặc loại bỏ

---

### 8.3 Phê duyệt có điều kiện

- Có thể áp dụng giới hạn:
  - Thời gian
  - Phạm vi
  - Tăng cường giám sát

---

## 9. Giai đoạn 5 – Triển khai & Vận hành

---

### 9.1 Nguyên tắc triển khai

- Chỉ triển khai mô hình đã được phê duyệt
- Không thay đổi logic cốt lõi
- Mọi cấu hình phải được ghi nhận

---

### 9.2 Trách nhiệm vận hành

- Đơn vị sử dụng:
  - Sử dụng đúng mục đích
  - Không lạm dụng mô hình
- Khối rủi ro:
  - Giám sát độc lập

---

## 10. Giai đoạn 6 – Giám sát & Đánh giá định kỳ

---

### 10.1 Mục tiêu giám sát

- Phát hiện suy giảm hiệu quả
- Phát hiện sai lệch hệ thống
- Phát hiện sử dụng sai mục đích

---

### 10.2 Tần suất giám sát

- Theo phân loại rủi ro:
  - Low: định kỳ
  - Medium: tăng cường
  - High: liên tục hoặc bán liên tục

---

### 10.3 Báo cáo giám sát

- Báo cáo nội bộ
- Báo cáo cho MAC (nếu áp dụng)
- Lưu trữ phục vụ kiểm toán

---

## 11. Giai đoạn 7 – Thay đổi & Hiệu chỉnh mô hình

---

### 11.1 Khi nào cần thay đổi mô hình

- Thị trường biến động mạnh
- Kết quả định giá lệch có hệ thống
- Giả định không còn phù hợp
- Yêu cầu từ kiểm toán / thanh tra

---

### 11.2 Phân loại thay đổi

- Thay đổi không trọng yếu:
  - Cấu hình nhỏ
  - Điều chỉnh ngưỡng
- Thay đổi trọng yếu:
  - Logic
  - Phạm vi
  - Mục đích sử dụng

---

### 11.3 Quy trình phê duyệt thay đổi

- Thay đổi không trọng yếu:
  - Ghi nhận và báo cáo
- Thay đổi trọng yếu:
  - Validation lại
  - Phê duyệt lại theo cấp rủi ro

---

## 12. Giai đoạn 8 – Tạm dừng & Loại bỏ mô hình (Decommission)

---

### 12.1 Các trường hợp phải xem xét loại bỏ

- Mô hình không còn phù hợp
- Rủi ro vượt mức chấp nhận
- Không thể khắc phục sai lệch
- Có mô hình thay thế được phê duyệt

---

### 12.2 Quy trình loại bỏ

- Đề xuất loại bỏ
- Đánh giá tác động
- Phê duyệt của cấp có thẩm quyền
- Tắt mô hình trong hệ thống
- Lưu trữ toàn bộ hồ sơ

---

### 12.3 Nguyên tắc lưu trữ

- Không xóa lịch sử
- Phục vụ truy vết và kiểm toán

---

## 13. Quản trị vòng đời LLM trong Advanced AVM

---

### 13.1 Vị trí LLM trong vòng đời

- LLM được coi là mô hình hỗ trợ
- Không có quyền:
  - Ra giá
  - Điều chỉnh giá
  - Phê duyệt kết quả

---

### 13.2 Điều kiện duy trì LLM

- Nếu thay đổi vai trò → phải tái phân loại rủi ro
- Có thể tạm dừng ngay nếu vi phạm nguyên tắc

---

## 14. Lưu trữ hồ sơ & Audit Trail

---

### 14.1 Hồ sơ bắt buộc

- Hồ sơ đề xuất
- Báo cáo validation
- Quyết định phê duyệt
- Báo cáo giám sát
- Biên bản thay đổi / loại bỏ

---

### 14.2 Thời gian lưu trữ

- Theo quy định nội bộ ngân hàng
- Đáp ứng yêu cầu kiểm toán và pháp lý

---

## 15. Trách nhiệm & Tuân thủ

---

- Đơn vị sử dụng chịu trách nhiệm tuân thủ chính sách
- Vi phạm quy trình quản trị vòng đời mô hình được coi là vi phạm kiểm soát nội bộ
- Chính sách này là tài liệu bắt buộc trong hệ thống quản trị rủi ro mô hình

---

## 16. Kết luận

Quản trị vòng đời mô hình trong Advanced AVM nhằm:

- Đảm bảo mô hình phục vụ con người, không thay thế con người
- Đặt AI dưới kiểm soát quản trị rủi ro
- Bảo vệ ngân hàng trước rủi ro mô hình, rủi ro pháp lý và rủi ro danh tiếng

Vòng đời mô hình không kết thúc khi mô hình chạy tốt,  
mà chỉ kết thúc khi mô hình được **loại bỏ có kiểm soát và có trách nhiệm**.

---
