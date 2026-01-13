# FALLBACK POLICY

_Document initialized automatically._

# FALLBACK POLICY

## Quy trình dự phòng vận hành cho Hệ thống AVM – Hybrid AI + Thẩm định thủ công

---

## 1. Mục đích

Tài liệu này quy định **chính sách và playbook vận hành dự phòng (Fallback Policy)** cho Hệ thống Advanced AVM – Hybrid AI + Thẩm định thủ công, nhằm:

- Đảm bảo hoạt động định giá không bị gián đoạn trong trường hợp hệ thống hoặc mô hình gặp sự cố
- Kiểm soát rủi ro khi kết quả AVM không đủ độ tin cậy để sử dụng cho mục đích tín dụng, đầu tư hoặc thẩm định độc lập (DD)
- Thiết lập cơ chế **override có kiểm soát** bởi con người
- Đáp ứng yêu cầu của quản trị rủi ro mô hình, kiểm toán nội bộ và cơ quan quản lý

Chính sách này **không cho phép** AI hoặc AVM thay thế vai trò của thẩm định viên được cấp phép hoặc người có thẩm quyền phê duyệt tín dụng.

---

## 2. Phạm vi áp dụng

Chính sách áp dụng cho:

- Toàn bộ hệ thống AVM, bao gồm các model Trust, Feature, AVM Core, Ensemble và Risk
- Các hồ sơ định giá phục vụ:

  - Tín dụng có tài sản bảo đảm
  - Đầu tư và thẩm định dự án
  - Due Diligence (DD)

- Các đơn vị liên quan:

  - Khối thẩm định giá
  - Khối quản trị rủi ro mô hình (MRM)
  - Khối vận hành hệ thống

---

## 3. Nguyên tắc vận hành fallback

Việc kích hoạt fallback tuân thủ các nguyên tắc sau:

1. **An toàn và thận trọng là ưu tiên cao nhất**
   Khi mức độ tin cậy giảm, hệ thống phải chuyển sang chế độ bảo thủ hơn.

2. **Không suy giảm ngầm (No Silent Degradation)**
   Hệ thống không được phép tiếp tục vận hành như bình thường khi đã vượt ngưỡng rủi ro.

3. **Con người giữ quyền quyết định cuối cùng**
   Mọi trường hợp bất định phải được xử lý bởi thẩm định viên và cấp phê duyệt phù hợp.

4. **Truy vết và kiểm toán được**
   Mọi hành động fallback và override đều phải được ghi nhận, lưu vết và có thể tái hiện.

---

## 4. Các tình huống kích hoạt fallback

### 4.1 Fallback do lỗi hệ thống

Bao gồm nhưng không giới hạn:

- Hệ thống định giá trung tâm không khả dụng
- Lỗi pipeline dữ liệu (ingestion, feature engineering)
- Không tạo được snapshot hoặc hồ sơ định giá đầy đủ
- Hệ thống audit hoặc lưu vết không hoạt động

**Nguyên tắc xử lý:**

- Dừng sử dụng AVM cho ra giá
- Chuyển hồ sơ sang quy trình thẩm định thủ công

---

### 4.2 Fallback do lỗi mô hình

Bao gồm:

- Model bị cảnh báo drift vượt ngưỡng cho phép
- Hiệu năng model giảm dưới mức được phê duyệt
- Sự phân tán lớn giữa các model định giá cốt lõi
- Model phụ thuộc không khả dụng

**Nguyên tắc xử lý:**

- Hạ vai trò AVM xuống mức tham chiếu
- Tăng yêu cầu rà soát thủ công

---

### 4.3 Fallback do dữ liệu không đủ tin cậy

Bao gồm:

- Thiếu giao dịch so sánh hợp lệ
- Thông tin pháp lý không đầy đủ hoặc mâu thuẫn
- Dữ liệu đầu vào có dấu hiệu thao túng hoặc gian lận
- Chất lượng dữ liệu không đạt tiêu chuẩn

**Nguyên tắc xử lý:**

- Không sử dụng AVM làm căn cứ chính
- Bắt buộc áp dụng phương pháp thẩm định truyền thống

---

### 4.4 Fallback theo ngưỡng độ tin cậy

Khi:

- Confidence score dưới ngưỡng được phê duyệt
- Risk band vượt mức chấp nhận cho mục đích sử dụng

**Nguyên tắc xử lý:**

- Kích hoạt quy trình phê duyệt nâng cao
- Có thể yêu cầu định giá lại thủ công

---

## 5. Các chế độ fallback

### 5.1 Chế độ 1 – Dừng AVM hoàn toàn

- Không sinh giá trị định giá tự động
- AVM chỉ được dùng để tổng hợp dữ liệu
- Áp dụng cho sự cố nghiêm trọng

---

### 5.2 Chế độ 2 – AVM tham chiếu có điều kiện

- AVM chỉ đóng vai trò hỗ trợ
- Bắt buộc thẩm định viên kiểm tra và xác nhận
- Không được sử dụng AVM làm cơ sở duy nhất

---

### 5.3 Chế độ 3 – Định giá bảo thủ

- Áp dụng giả định thận trọng hơn
- Thu hẹp khoảng giá chấp nhận
- Tăng cấp phê duyệt

---

### 5.4 Chế độ 4 – Thẩm định thủ công hoàn toàn

- AVM không tham gia vào việc xác định giá
- Áp dụng đầy đủ quy trình thẩm định truyền thống

---

## 6. Chính sách override

### 6.1 Khái niệm override

Override là việc thẩm định viên hoặc người có thẩm quyền:

- Điều chỉnh kết quả AVM
- Không chấp nhận kết quả AVM
- Lựa chọn giá trị khác với giá trị do AVM đề xuất

Override là hành vi **được phép, dự kiến trước và kiểm soát**.

---

### 6.2 Lý do override hợp lệ

- Đặc thù tài sản không được phản ánh trong dữ liệu
- Tình trạng pháp lý hoặc quy hoạch đặc biệt
- Biến động thị trường bất thường
- Hạn chế đã được nhận diện của mô hình

---

### 6.3 Thẩm quyền phê duyệt override

| Mức độ ảnh hưởng         | Thẩm quyền               |
| ------------------------ | ------------------------ |
| Nhỏ                      | Thẩm định viên           |
| Trung bình               | Trưởng bộ phận thẩm định |
| Lớn / ảnh hưởng tín dụng | Hội đồng thẩm định       |

---

### 6.4 Yêu cầu hồ sơ override

Mỗi override phải có:

- Giá trị AVM ban đầu
- Giá trị cuối cùng được chấp nhận
- Lý do override
- Người thực hiện và người phê duyệt
- Thời điểm thực hiện

---

## 7. Xử lý trường hợp AVM không đủ tin cậy

Các trường hợp thường gặp:

- Tài sản cá biệt, thanh khoản thấp
- Thị trường đóng băng hoặc biến động mạnh
- Số lượng giao dịch so sánh không đủ

**Biện pháp:**

- Gắn cờ rủi ro cho hồ sơ
- Không cho phép phê duyệt tự động
- Bắt buộc thẩm định thủ công và rà soát chéo

---

## 8. Trách nhiệm và vai trò

### 8.1 Thẩm định viên

- Đánh giá mức độ phù hợp của AVM
- Thực hiện override khi cần thiết
- Chịu trách nhiệm chuyên môn đối với giá trị đề xuất

### 8.2 Quản lý thẩm định

- Phê duyệt fallback và override quan trọng
- Theo dõi xu hướng fallback

### 8.3 Quản trị rủi ro mô hình

- Định nghĩa ngưỡng rủi ro
- Giám sát tần suất fallback
- Báo cáo cho Ủy ban quản trị mô hình

### 8.4 Vận hành hệ thống

- Khắc phục sự cố kỹ thuật
- Đảm bảo hệ thống ghi nhận đầy đủ log

---

## 9. Yêu cầu lưu vết và kiểm toán

- Tất cả sự kiện fallback và override phải được ghi log
- Log phải gắn với hồ sơ định giá cụ thể
- Phục vụ tái hiện quyết định khi kiểm toán

---

## 10. Báo cáo và rà soát định kỳ

- Báo cáo fallback gửi định kỳ cho quản trị rủi ro mô hình
- Rà soát chính sách ít nhất hàng năm hoặc khi có sự cố lớn

---

## 11. Tuyên bố chính sách

Ngân hàng xác định rằng:

- AVM là công cụ hỗ trợ, không phải cơ chế ra quyết định tự động
- Khi độ tin cậy giảm, quyền quyết định phải quay về con người
- Kiểm soát rủi ro và tuân thủ quan trọng hơn tự động hóa

---

**Kết thúc tài liệu**
