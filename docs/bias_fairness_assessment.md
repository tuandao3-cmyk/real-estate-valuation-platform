# BIAS FAIRNESS ASSESSMENT

_Document initialized automatically._

# BIAS & FAIRNESS ASSESSMENT

## 1. Mục đích và phạm vi tài liệu

Tài liệu này xác định, phân tích và đánh giá các dạng **bias (thiên lệch)** và vấn đề **fairness (công bằng)** có thể phát sinh trong Hệ thống Advanced AVM – Hybrid AI + Thẩm định thủ công. Mục tiêu là:

- Nhận diện rõ ràng các nguồn sai lệch tiềm ẩn.
- Mô tả các cơ chế kiểm soát và giảm thiểu bias của hệ thống.
- Xác định vai trò bắt buộc của con người trong việc rà soát và quyết định cuối cùng.

Tài liệu này **không nhằm chứng minh hệ thống không có bias**, mà nhằm chứng minh rằng bias được **nhận diện, quản trị và kiểm soát có hệ thống**.

Phạm vi áp dụng:

- Toàn bộ các mô hình thuộc hệ sinh thái AVM.
- Các báo cáo định giá phục vụ ngân hàng, quỹ đầu tư, và hoạt động Due Diligence.

---

## 2. Nguyên tắc nền tảng về Bias & Fairness

### 2.1. Quan điểm chính thức của hệ thống

- Bias là **đặc tính không thể loại bỏ hoàn toàn** trong mọi mô hình định lượng.
- Mục tiêu của hệ thống **không phải loại bỏ bias**, mà là:

  - Nhận diện sớm
  - Định lượng mức độ
  - Kiểm soát tác động

- Fairness trong định giá không đồng nghĩa với "đối xử giống nhau", mà là:

  - Áp dụng phương pháp phù hợp với từng loại tài sản
  - Tránh thiên lệch mang tính hệ thống và không có cơ sở nghiệp vụ

### 2.2. Phân biệt bias hợp lệ và bias không chấp nhận

- **Bias hợp lệ**: xuất phát từ đặc thù thị trường, dữ liệu giao dịch, hoặc phân khúc tài sản.
- **Bias không chấp nhận**: phát sinh do dữ liệu thiếu đại diện, mô hình áp dụng sai mục đích, hoặc sử dụng kết quả ngoài phạm vi cho phép.

---

## 3. Các loại Bias có thể xảy ra

### 3.1. Bias dữ liệu (Data Bias)

#### 3.1.1. Bias do dữ liệu giao dịch không đầy đủ

- Giao dịch thực tế không được công bố đầy đủ.
- Giao dịch khai giá thấp để giảm thuế.
- Thiếu dữ liệu ở khu vực ngõ nhỏ, tài sản đặc thù.

Tác động:

- AVM có xu hướng bám vào nhóm tài sản có nhiều dữ liệu hơn.
- Giá ước tính có thể không phản ánh đầy đủ thị trường thực.

#### 3.1.2. Bias theo khu vực địa lý

- Khu vực trung tâm có mật độ dữ liệu cao.
- Khu vực ven đô, vùng mới phát triển thiếu dữ liệu lịch sử.

Tác động:

- Độ tin cậy giữa các khu vực không đồng đều.

---

### 3.2. Bias phân khúc (Segment Bias)

- Nhà ở riêng lẻ vs căn hộ chung cư.
- Tài sản cao cấp vs tài sản phổ thông.
- Tài sản có pháp lý phức tạp.

Nguy cơ:

- Mô hình học tốt ở phân khúc phổ biến nhưng kém hiệu quả ở phân khúc hiếm.

---

### 3.3. Bias thời điểm (Temporal Bias)

- Dữ liệu lịch sử không phản ánh biến động hiện tại.
- Thị trường đóng băng hoặc sốt nóng bất thường.

Nguy cơ:

- Mô hình phản ứng chậm với thay đổi đột ngột.

---

### 3.4. Bias thanh khoản (Liquidity Bias)

- Tài sản thanh khoản cao có nhiều giao dịch.
- Tài sản thanh khoản thấp ít được so sánh.

Nguy cơ:

- Định giá quá lạc quan cho tài sản khó bán.

---

### 3.5. Bias pháp lý và quy hoạch

- Tài sản có quy hoạch treo.
- Tài sản chưa hoàn thiện pháp lý.

Nguy cơ:

- Dữ liệu rao bán không phản ánh rủi ro pháp lý.

---

### 3.6. Bias do hành vi thị trường

- Thổi giá.
- Dìm giá.
- Giao dịch nội bộ.

Nguy cơ:

- AVM bị nhiễu bởi tín hiệu giả.

---

### 3.7. Bias từ cách sử dụng kết quả

- Dùng kết quả AVM làm giá chính thức.
- Bỏ qua cảnh báo confidence thấp.

Nguy cơ:

- Sai lệch không nằm ở mô hình mà ở con người.

---

## 4. Cơ chế giảm thiểu bias của hệ thống

### 4.1. Đa mô hình (Multi-model Approach)

- Không phụ thuộc vào một mô hình duy nhất.
- So sánh chéo giữa nhiều phương pháp định giá.

### 4.2. Phân vùng thị trường (Geo-clustering)

- Tránh so sánh tài sản không cùng thị trường con.

### 4.3. Kiểm soát chất lượng dữ liệu

- Loại bỏ outlier.
- Gắn cờ dữ liệu thiếu độ tin cậy.

### 4.4. Trust & Fraud Models

- Giảm ảnh hưởng của dữ liệu rác.
- Phát hiện hành vi thao túng.

### 4.5. Confidence Scoring

- Định lượng mức độ không chắc chắn.
- Kích hoạt human review khi confidence thấp.

---

## 5. Vai trò bắt buộc của Human Review

### 5.1. Nguyên tắc

- Không có báo cáo định giá nào được phát hành chỉ dựa trên AVM.
- Thẩm định viên chịu trách nhiệm cuối cùng.

### 5.2. Khi nào bắt buộc human review

- Confidence score dưới ngưỡng.
- Tài sản đặc thù.
- Dữ liệu thiếu hoặc mâu thuẫn.

### 5.3. Trách nhiệm của người rà soát

- Đánh giá tính hợp lý của kết quả.
- Áp dụng phương pháp so sánh truyền thống.
- Ghi nhận rõ lý do chấp nhận hoặc điều chỉnh.

---

## 6. Giới hạn về Fairness

- Hệ thống không nhằm đảm bảo công bằng xã hội.
- Fairness được hiểu trong phạm vi nghiệp vụ định giá.

---

## 7. Kiểm toán và truy vết

- Lưu vết toàn bộ input, output.
- Ghi nhận can thiệp thủ công.

---

## 8. Kết luận

Hệ thống Advanced AVM thừa nhận sự tồn tại của bias và coi việc quản trị bias là một phần bắt buộc của quản trị rủi ro mô hình. Fairness không đạt được bằng cách phủ nhận sai lệch, mà bằng cách **minh bạch, kiểm soát và gắn trách nhiệm con người vào quyết định cuối cùng**.
