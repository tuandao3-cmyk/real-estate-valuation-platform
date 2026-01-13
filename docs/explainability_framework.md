# EXPLAINABILITY FRAMEWORK

## Khung giải thích & truy xuất quyết định định giá

_(Advanced AVM – Hybrid AI + Thẩm định thủ công)_

---

## 1. Mục đích tài liệu

Tài liệu này mô tả **khung Explainability (Giải thích)** áp dụng cho hệ thống Advanced AVM – Hybrid AI + Thẩm định thủ công, nhằm:

- Đảm bảo **ngân hàng, quỹ, kiểm toán** có thể:
  - Hiểu được **AI đã làm gì**
  - Hiểu được **AI không làm gì**
  - Truy vết được **nguồn gốc từng kết quả**
- Đảm bảo **quyết định giá cuối cùng**:
  - Có thể giải trình
  - Có thể kiểm toán
  - Có thể bảo vệ pháp lý

Tài liệu này **không**:

- Giải thích chi tiết thuật toán toán học
- Cam kết độ chính xác tuyệt đối
- Thay thế báo cáo thẩm định hoặc ý kiến thẩm định viên

---

## 2. Định nghĩa Explainability trong định giá bất động sản

### 2.1 Explainability là gì

Trong bối cảnh định giá bất động sản, **Explainability** được hiểu là:

> Khả năng mô tả, diễn giải và chứng minh một cách hợp lý  
> cách hệ thống AI hỗ trợ quá trình hình thành kết quả định giá.

Explainability **không đồng nghĩa** với:

- Giải thích chi tiết công thức
- Mở toàn bộ mô hình
- Cho phép người dùng can thiệp vào thuật toán

Explainability **tập trung vào**:

- Logic nghiệp vụ
- Vai trò từng lớp mô hình
- Quan hệ giữa dữ liệu – mô hình – kết quả

---

### 2.2 Explainability khác gì so với Transparency

| Khái niệm      | Ý nghĩa              |
| -------------- | -------------------- |
| Transparency   | Mở cấu trúc mô hình  |
| Explainability | Giải thích kết quả   |
| Auditability   | Truy vết & tái lập   |
| Accountability | Xác định trách nhiệm |

Hệ thống **ưu tiên Explainability & Auditability**,  
không yêu cầu full transparency thuật toán.

---

## 3. Nguyên tắc Explainability của hệ thống

### 3.1 Nguyên tắc 1: AI không phải người ra quyết định

- AI **không ký giá**
- AI **không chấp thuận hồ sơ**
- AI **không override thẩm định viên**

Explainability tập trung vào **vai trò hỗ trợ**.

---

### 3.2 Nguyên tắc 2: Giải thích theo tầng (Layered Explanation)

Hệ thống áp dụng **giải thích nhiều tầng**:

1. Tầng dữ liệu
2. Tầng mô hình đơn lẻ
3. Tầng hợp nhất (ensemble)
4. Tầng quy tắc nghiệp vụ
5. Tầng quyết định cuối cùng

---

### 3.3 Nguyên tắc 3: Phù hợp đối tượng đọc

| Đối tượng         | Mức giải thích         |
| ----------------- | ---------------------- |
| Hội đồng tín dụng | Tổng hợp, rủi ro       |
| Thẩm định viên    | Logic nghiệp vụ        |
| Kiểm toán         | Truy vết, bằng chứng   |
| Pháp chế          | Trách nhiệm & giới hạn |

---

## 4. Phạm vi Explainability áp dụng

Explainability áp dụng cho:

- Kết quả trung gian
- Cảnh báo rủi ro
- Quyết định kích hoạt / không kích hoạt model
- Lý do yêu cầu thẩm định thủ công
- Lý do override (nếu có)

Explainability **không áp dụng** cho:

- Trọng số nội bộ chi tiết
- Tham số huấn luyện
- Intellectual property của mô hình

---

## 5. Phân loại mô hình theo khả năng giải thích

### 5.1 Nhóm A – Mô hình giải thích trực tiếp

Các mô hình có logic gần với nghiệp vụ thẩm định:

- Hedonic Regression
- Comparable Sales (KNN)
- Cost Approach
- Income Approach
- Tier-based Regression

Đặc điểm:

- Input dễ hiểu
- Output là giá trị kinh tế quen thuộc
- Có thể giải thích bằng ngôn ngữ nghiệp vụ

---

### 5.2 Nhóm B – Mô hình giải thích theo chỉ báo

Các mô hình không ra giá trực tiếp:

- Trust Score
- Fraud Detection
- Liquidity Score
- Volatility Index

Đặc điểm:

- Output là score / flag
- Không ảnh hưởng trực tiếp đến giá
- Ảnh hưởng đến **quy trình xử lý**

---

### 5.3 Nhóm C – Mô hình hỗ trợ kỹ thuật

- Image Analysis
- Text Embedding
- Drift Detection

Đặc điểm:

- Không trình bày cho khách hàng
- Chỉ trình bày cho kiểm toán khi cần

---

## 6. Explainability theo từng lớp hệ thống

---

## 6.1 Lớp dữ liệu (Data Explainability)

### 6.1.1 Nội dung giải thích

- Nguồn dữ liệu
- Thời điểm dữ liệu
- Loại dữ liệu (listing / transaction)
- Trạng thái làm sạch

---

### 6.1.2 Trình bày cho ngân hàng

Ví dụ:

> Dữ liệu so sánh được lấy từ  
> các giao dịch thành công trong 12 tháng gần nhất  
> trong cùng micro-market,  
> đã loại bỏ các listing không đáng tin cậy.

---

### 6.1.3 Truy vết kiểm toán

- Data provenance ID
- Snapshot thời điểm định giá
- Không sử dụng dữ liệu cập nhật sau đó

---

## 6.2 Lớp Trust & Fraud Models

### 6.2.1 Mục đích giải thích

- Tại sao dữ liệu được chấp nhận
- Tại sao dữ liệu bị giảm trọng số
- Tại sao cần xác minh thủ công

---

### 6.2.2 Cách giải thích

Không giải thích thuật toán, chỉ giải thích:

- Có dấu hiệu bất thường hay không
- Mức độ tin cậy tổng thể
- Ảnh hưởng đến quy trình

---

### 6.2.3 Ví dụ diễn giải

> Một số nguồn listing có mức độ tin cậy thấp hơn trung bình  
> do trùng lặp nội dung và sai lệch hình ảnh,  
> tuy nhiên chưa đủ nghiêm trọng để loại bỏ hoàn toàn.

---

## 6.3 Lớp Feature Engineering

### 6.3.1 Nội dung giải thích

- Feature nào được sử dụng
- Feature nào bị loại
- Lý do loại bỏ

---

### 6.3.2 Giới hạn giải thích

- Không giải thích embedding vector
- Chỉ giải thích vai trò nghiệp vụ

---

### 6.3.3 Ví dụ

> Đặc điểm vị trí được chuẩn hóa theo cụm thị trường nhỏ  
> nhằm tránh so sánh chéo giữa các khu vực không tương đồng.

---

## 6.4 Lớp AVM Core Models

### 6.4.1 Nguyên tắc giải thích

Mỗi model được giải thích như **một phương pháp thẩm định độc lập**.

---

### 6.4.2 Hedonic Model

Giải thích tập trung vào:

- Các yếu tố chính ảnh hưởng giá
- Xu hướng tăng/giảm
- Phù hợp với thị trường đại chúng

Ví dụ:

> Giá trị ước tính phản ánh ảnh hưởng tích cực  
> từ vị trí nội đô và mặt tiền,  
> được điều chỉnh giảm do diện tích nhỏ.

---

### 6.4.3 Comparable Sales Model

Giải thích tập trung vào:

- Số tài sản so sánh
- Mức độ tương đồng
- Phạm vi giá

---

### 6.4.4 Cost Approach

Giải thích tập trung vào:

- Giá trị đất
- Giá trị công trình còn lại
- Không phản ánh thanh khoản

---

### 6.4.5 Income Approach

- Chỉ kích hoạt khi có dữ liệu thuê ổn định
- Nếu không kích hoạt → phải giải thích lý do

---

## 6.5 Lớp Ensemble & Aggregation

### 6.5.1 Nguyên tắc

Ensemble **không phải trung bình máy móc**.

---

### 6.5.2 Nội dung giải thích

- Model nào được sử dụng
- Model nào bị giảm trọng số
- Lý do

---

### 6.5.3 Ví dụ diễn giải

> Kết quả cuối cùng được tổng hợp từ  
> các phương pháp so sánh và chi phí,  
> trong khi phương pháp thu nhập không được áp dụng  
> do tài sản không tạo dòng tiền ổn định.

---

## 6.6 Lớp Risk Adjustment

### 6.6.1 Mục đích

Giải thích **rủi ro của giá**, không thay đổi giá tùy tiện.

---

### 6.6.2 Nội dung giải thích

- Thanh khoản
- Biến động thị trường
- Rủi ro thao túng giá

---

### 6.6.3 Ví dụ

> Giá trị được đánh giá có mức rủi ro trung bình  
> do thanh khoản hạn chế của ngõ nhỏ.

---

## 6.7 Lớp Rule & Approval

### 6.7.1 Nội dung giải thích

- Tại sao hồ sơ được tự động chấp nhận
- Tại sao phải trình duyệt
- Tại sao bị từ chối

---

### 6.7.2 Nguyên tắc

- Rule **cố định**
- Có phiên bản
- Không bị model thay đổi

---

## 6.8 Lớp Human Override

### 6.8.1 Điều kiện giải thích

- Ai override
- Khi nào
- Vì sao
- Tác động

---

### 6.8.2 Trình bày

Override **không che giấu**  
mà được coi là một phần explainability.

---

## 6.9 Lớp LLM Explainability

### 6.9.1 Vai trò

LLM:

- Viết diễn giải
- Chuẩn hóa ngôn ngữ
- Không tạo ra quyết định mới

---

### 6.9.2 Nguyên tắc kiểm soát

- Không có quyền sửa số
- Không có quyền suy đoán ngoài dữ liệu
- Không có quyền kết luận thay con người

---

### 6.9.3 Nội dung LLM được phép viết

- Tóm tắt giả định
- Giải thích phương pháp
- Nêu hạn chế

---

## 7. Explainability trong báo cáo gửi ngân hàng

### 7.1 Cấu trúc trình bày khuyến nghị

1. Executive Summary
2. Kết quả định giá
3. Phương pháp sử dụng
4. Rủi ro & hạn chế
5. Vai trò AI
6. Vai trò thẩm định viên

---

### 7.2 Ngôn ngữ sử dụng

- Trung tính
- Không khẳng định tuyệt đối
- Không dùng thuật ngữ AI phức tạp

---

### 7.3 Ví dụ câu chuẩn

> Kết quả định giá được hỗ trợ bởi hệ thống AVM  
> kết hợp với rà soát và phê duyệt của thẩm định viên.

---

## 8. Explainability & Kiểm toán

### 8.1 Đáp ứng yêu cầu kiểm toán

- Tái lập kết quả
- Truy vết dữ liệu
- Log quyết định

---

### 8.2 Những gì kiểm toán có thể yêu cầu

- Snapshot hồ sơ
- Danh sách model kích hoạt
- Rule áp dụng
- Override log

---

## 9. Giới hạn của Explainability

- Không loại bỏ rủi ro thị trường
- Không thay thế thẩm định thực địa
- Không đảm bảo giá trị tương lai

---

## 10. Kết luận

Explainability trong hệ thống Advanced AVM:

- Không nhằm “làm AI thông minh hơn”
- Mà nhằm **làm quyết định an toàn hơn**
- Và **làm trách nhiệm rõ ràng hơn**

AI là công cụ hỗ trợ.  
Thẩm định viên là người chịu trách nhiệm cuối cùng.

---
