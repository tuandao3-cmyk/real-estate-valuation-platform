# MODEL APPROVAL COMMITTEE

_Document initialized automatically._

# MODEL APPROVAL COMMITTEE POLICY

## Chính sách Hội đồng Phê duyệt & Quản trị Vòng đời Mô hình

_(Advanced AVM – Hybrid AI + Thẩm định thủ công)_

---

## 1. Mục đích tài liệu

Tài liệu này quy định **cơ chế phê duyệt, giám sát và loại bỏ mô hình** trong hệ thống Advanced AVM, nhằm:

- Đảm bảo quản trị rủi ro mô hình phù hợp chuẩn ngân hàng
- Xác định rõ:
  - Ai có thẩm quyền phê duyệt mô hình
  - Khi nào mô hình được đưa vào sử dụng
  - Khi nào cần thay đổi, hiệu chỉnh
  - Khi nào phải loại bỏ (decommission)
- Làm căn cứ cho:
  - Hồ sơ phê duyệt nội bộ
  - Kiểm toán nội bộ / kiểm toán độc lập
  - Thanh tra giám sát

---

## 2. Phạm vi áp dụng

Chính sách này áp dụng cho:

- Tất cả mô hình thuộc hệ thống Advanced AVM, bao gồm:
  - AVM Core Models
  - Mô hình trung gian, mô hình phụ trợ
  - Mô hình giám sát, cảnh báo
  - LLM hỗ trợ quy trình
- Tất cả đơn vị tham gia:
  - Khối thẩm định giá
  - Khối rủi ro
  - Khối CNTT / dữ liệu
  - Khối tuân thủ

Không áp dụng cho:

- Ý kiến chuyên môn của thẩm định viên
- Quyết định tín dụng cuối cùng

---

## 3. Nguyên tắc quản trị vòng đời mô hình

---

### 3.1 Nguyên tắc trách nhiệm cuối cùng

- **Mô hình không chịu trách nhiệm**
- Trách nhiệm cuối cùng thuộc về:
  - Hội đồng phê duyệt
  - Đơn vị sử dụng
  - Cá nhân phê duyệt kết quả định giá

---

### 3.2 Nguyên tắc phân quyền theo rủi ro

- Mức độ phê duyệt phụ thuộc vào **Model Risk Classification**
- Không áp dụng một cơ chế cho tất cả mô hình

---

### 3.3 Nguyên tắc kiểm soát độc lập

- Phát triển ≠ Thẩm định ≠ Phê duyệt
- High Risk Models phải có kiểm soát độc lập

---

### 3.4 Nguyên tắc truy vết & tái lập

- Mọi quyết định liên quan đến mô hình phải:
  - Có hồ sơ
  - Có biên bản
  - Có thể truy vết và tái lập

---

## 4. Hội đồng Phê duyệt Mô hình (Model Approval Committee – MAC)

---

## 4.1 Vai trò

Model Approval Committee (MAC) là cơ quan chịu trách nhiệm:

- Phê duyệt đưa mô hình vào sử dụng
- Phê duyệt thay đổi trọng yếu
- Quyết định loại bỏ mô hình
- Giám sát rủi ro mô hình cấp cao

---

## 4.2 Thành phần MAC

MAC tối thiểu bao gồm:

- Đại diện Khối Thẩm định giá
- Đại diện Khối Quản trị Rủi ro
- Đại diện Khối Tuân thủ
- Đại diện CNTT / Dữ liệu (không giữ vai trò quyết định đơn lẻ)

Tùy theo cấp rủi ro, có thể bổ sung:

- Kiểm toán nội bộ
- Pháp chế

---

## 4.3 Nguyên tắc hoạt động của MAC

- Hoạt động theo nguyên tắc tập thể
- Quyết định dựa trên hồ sơ, không dựa trên niềm tin vào công nghệ
- Biên bản họp là tài liệu bắt buộc lưu trữ

---

## 5. Vòng đời mô hình (Model Lifecycle)

---

### 5.1 Các giai đoạn vòng đời

Mỗi mô hình phải trải qua đầy đủ các giai đoạn:

1. Đề xuất (Initiation)
2. Phát triển / Cấu hình
3. Thẩm định độc lập (Validation)
4. Phê duyệt
5. Triển khai vận hành
6. Giám sát
7. Hiệu chỉnh / Thay thế
8. Loại bỏ (Decommission)

---

## 6. Giai đoạn Đề xuất mô hình

---

### 6.1 Khi nào cần đề xuất mô hình mới

- Nhu cầu nghiệp vụ mới
- Thay đổi thị trường đáng kể
- Mô hình hiện tại không còn phù hợp
- Yêu cầu từ kiểm toán / thanh tra

---

### 6.2 Hồ sơ đề xuất tối thiểu

- Mục đích sử dụng
- Phân loại rủi ro dự kiến (Low / Medium / High)
- Phạm vi ảnh hưởng
- Vai trò của con người trong quy trình
- Rủi ro tiềm ẩn

---

## 7. Giai đoạn Thẩm định & Validation

---

### 7.1 Nguyên tắc validation

- Validation độc lập với đội phát triển
- Không chỉ kiểm tra kỹ thuật
- Bắt buộc kiểm tra:
  - Giả định nghiệp vụ
  - Phù hợp mục đích sử dụng
  - Giới hạn mô hình

---

### 7.2 Mức độ validation theo rủi ro

| Cấp rủi ro | Yêu cầu Validation |
| ---------- | ------------------ |
| Low        | Nghiệp vụ          |
| Medium     | Nghiệp vụ + rủi ro |
| High       | Độc lập đầy đủ     |

---

## 8. Giai đoạn Phê duyệt mô hình

---

### 8.1 Thẩm quyền phê duyệt

| Cấp rủi ro | Cơ quan phê duyệt               |
| ---------- | ------------------------------- |
| Low        | Quản lý đơn vị                  |
| Medium     | MAC                             |
| High       | MAC + cấp có thẩm quyền cao hơn |

---

### 8.2 Nội dung phê duyệt

MAC xem xét và phê duyệt dựa trên:

- Mục đích sử dụng rõ ràng
- Giới hạn mô hình được xác định
- Vai trò con người được giữ nguyên
- Cơ chế giám sát đầy đủ
- Kế hoạch xử lý sự cố

---

### 8.3 Điều kiện phê duyệt có điều kiện

MAC có thể phê duyệt có điều kiện, bao gồm:

- Giới hạn phạm vi sử dụng
- Yêu cầu giám sát tăng cường
- Thời gian thử nghiệm (pilot)

---

## 9. Triển khai & vận hành mô hình

---

### 9.1 Nguyên tắc triển khai

- Chỉ triển khai mô hình đã được phê duyệt
- Không tự ý thay đổi logic sau phê duyệt
- Mọi thay đổi phải được ghi nhận

---

### 9.2 Tài liệu bắt buộc

- Model Description
- User Guideline
- Limitation & Assumption
- Escalation Procedure

---

## 10. Giám sát mô hình

---

### 10.1 Mục tiêu giám sát

- Phát hiện suy giảm hiệu năng
- Phát hiện drift
- Phát hiện sử dụng sai mục đích

---

### 10.2 Trách nhiệm giám sát

- Đơn vị vận hành: giám sát thường xuyên
- Khối rủi ro: giám sát độc lập

---

## 11. Khi nào cần thay đổi mô hình

---

### 11.1 Các trường hợp bắt buộc xem xét thay đổi

- Thị trường biến động mạnh
- Sai lệch định giá lặp lại
- Phát hiện giả định không còn phù hợp
- Yêu cầu từ kiểm toán / thanh tra

---

### 11.2 Phân loại thay đổi

- Thay đổi không trọng yếu: cấu hình, tham số nhỏ
- Thay đổi trọng yếu: logic, dữ liệu, mục đích sử dụng

Thay đổi trọng yếu phải trình MAC phê duyệt lại.

---

## 12. Khi nào phải loại bỏ mô hình (Decommission)

---

### 12.1 Các trường hợp bắt buộc loại bỏ

- Mô hình không còn đáp ứng mục đích
- Rủi ro vượt mức chấp nhận
- Không thể khắc phục sai lệch
- Thay thế bằng mô hình mới được phê duyệt

---

### 12.2 Quy trình loại bỏ

- Đề xuất loại bỏ
- Đánh giá tác động
- Phê duyệt của MAC
- Lưu trữ hồ sơ mô hình cũ

---

## 13. Quản lý LLM trong vòng đời mô hình

---

### 13.1 Vai trò LLM

- Chỉ hỗ trợ diễn giải, tổng hợp
- Không ra quyết định
- Không sinh giá

---

### 13.2 Điều kiện duy trì

- Nếu LLM thay đổi vai trò → phải tái phân loại rủi ro
- Có thể bị tạm dừng ngay nếu vi phạm nguyên tắc

---

## 14. Lưu trữ & Audit Trail

---

### 14.1 Hồ sơ bắt buộc lưu trữ

- Hồ sơ phê duyệt
- Biên bản MAC
- Báo cáo validation
- Nhật ký thay đổi

---

### 14.2 Thời gian lưu trữ

- Theo quy định nội bộ ngân hàng
- Tối thiểu đáp ứng yêu cầu kiểm toán

---

## 15. Trách nhiệm & tuân thủ

---

- Đơn vị sử dụng chịu trách nhiệm sử dụng đúng mục đích
- Vi phạm quy trình quản trị mô hình được xem là vi phạm kiểm soát nội bộ
- Chính sách này là tài liệu bắt buộc tuân thủ

---

## 16. Kết luận

Chính sách Hội đồng Phê duyệt Mô hình của Advanced AVM nhằm:

- Đặt mô hình dưới sự kiểm soát, không phải ngược lại
- Đảm bảo AI là **công cụ hỗ trợ**, không phải người ra quyết định
- Bảo vệ ngân hàng trước rủi ro mô hình, rủi ro tuân thủ và rủi ro danh tiếng

Quản trị mô hình không nhằm tối đa hóa tự động hóa,  
mà nhằm **tối đa hóa kiểm soát và trách nhiệm**.

---
