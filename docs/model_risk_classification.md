# MODEL RISK CLASSIFICATION FRAMEWORK

## Khung Phân loại Rủi ro Mô hình

_(Advanced AVM – Hybrid AI + Thẩm định thủ công)_

---

## 1. Mục đích tài liệu

Tài liệu này thiết lập **Khung phân loại rủi ro mô hình (Model Risk Classification)** cho hệ thống Advanced AVM – Hybrid AI + Thẩm định thủ công, nhằm:

- Phân loại toàn bộ mô hình sử dụng trong hệ thống theo **mức độ rủi ro**
- Xác định **mức kiểm soát tương ứng** với từng loại mô hình
- Làm căn cứ cho:
  - Phê duyệt mô hình
  - Giám sát vận hành
  - Kiểm toán nội bộ / bên ngoài
  - Tuân thủ chuẩn quản trị rủi ro mô hình ngân hàng

Tài liệu này được thiết kế để:

- Ngân hàng đọc hiểu
- Kiểm toán soi được
- Có thể đưa trực tiếp vào **hồ sơ phê duyệt nội bộ**

---

## 2. Phạm vi áp dụng

Khung phân loại này áp dụng cho:

- Tất cả mô hình ML, thống kê, rule-based
- Tất cả mô hình phụ trợ (feature, trust, risk)
- LLM hỗ trợ diễn giải
- Các mô hình hiện tại và mô hình phát triển trong tương lai

Không áp dụng cho:

- Quyết định tín dụng cuối cùng
- Ý kiến thẩm định viên mang tính nghề nghiệp
- Phán quyết pháp lý

---

## 3. Định nghĩa Model Risk trong hệ thống AVM

### 3.1 Khái niệm Model Risk

Trong hệ thống Advanced AVM, **Model Risk** được hiểu là:

> Nguy cơ phát sinh sai lệch, hiểu nhầm, hoặc sử dụng sai  
> kết quả do mô hình tạo ra,  
> có thể ảnh hưởng đến kết quả định giá,  
> quyết định kinh doanh, hoặc tuân thủ ngân hàng.

---

### 3.2 Nguồn phát sinh Model Risk

Model Risk có thể phát sinh từ:

- Dữ liệu đầu vào không đại diện
- Giả định mô hình không phù hợp
- Sử dụng mô hình sai mục đích
- Diễn giải kết quả không đúng vai trò
- Lạm dụng tự động hóa

---

### 3.3 Nguyên tắc tiếp cận Model Risk

Hệ thống áp dụng cách tiếp cận:

- **Risk-based**
- **Use-case driven**
- **Không đồng nhất tất cả mô hình**

---

## 4. Nguyên tắc phân loại rủi ro mô hình

---

## 4.1 Nguyên tắc 1: Theo mục đích sử dụng

Mô hình được đánh giá rủi ro **trước hết theo mục đích**, không theo độ phức tạp kỹ thuật.

Ví dụ:

- Mô hình phức tạp nhưng chỉ dùng hỗ trợ → rủi ro thấp
- Mô hình đơn giản nhưng ảnh hưởng giá → rủi ro cao hơn

---

## 4.2 Nguyên tắc 2: Theo mức độ ảnh hưởng đến giá

Đánh giá mô hình dựa trên:

- Có tạo ra giá trị tiền tệ hay không
- Có ảnh hưởng trực tiếp đến kết quả giá cuối cùng hay không
- Có khả năng làm sai lệch kết luận định giá hay không

---

## 4.3 Nguyên tắc 3: Theo ảnh hưởng tín dụng & kinh doanh

Mô hình được đánh giá thêm theo:

- Có ảnh hưởng đến quyết định tín dụng không
- Có ảnh hưởng đến giới hạn rủi ro ngân hàng không
- Có thể gây tổn thất tài chính không

---

## 5. Các cấp độ rủi ro mô hình

Hệ thống phân loại mô hình thành 3 cấp độ chính:

- Low Risk Models
- Medium Risk Models
- High Risk Models

---

## 6. LOW RISK MODELS

### (Mô hình rủi ro thấp)

---

## 6.1 Định nghĩa

Low Risk Models là các mô hình:

- Không tạo ra giá trị định giá
- Không ảnh hưởng trực tiếp đến kết quả giá
- Chỉ hỗ trợ xử lý dữ liệu hoặc quy trình

---

## 6.2 Tiêu chí nhận diện

Một mô hình được phân loại Low Risk nếu:

- Output không phải giá
- Không ảnh hưởng đến quyết định chấp nhận / từ chối hồ sơ
- Không thay đổi trọng số giá
- Không thay thế phán đoán con người

---

## 6.3 Ví dụ mô hình Low Risk

### 6.3.1 Feature Engineering Models

- Text Embedding Model
- Image Feature Extraction
- Geo-clustering (chỉ phân nhóm)

---

### 6.3.2 Data Quality & Lineage Models

- Duplicate Detection
- Data Completeness Check
- Data Provenance Tracking

---

### 6.3.3 Drift & Monitoring Models

- Feature Drift Detection
- Distribution Shift Monitoring

---

### 6.3.4 LLM Support Layer

- Viết nhận xét
- Tóm tắt giả định
- Chuẩn hóa ngôn ngữ báo cáo

(Lưu ý: LLM **không truy cập giá**)

---

## 6.4 Ảnh hưởng tín dụng

- Không ảnh hưởng trực tiếp
- Không được dùng làm căn cứ phê duyệt

---

## 6.5 Yêu cầu kiểm soát đối với Low Risk Models

| Nội dung          | Yêu cầu            |
| ----------------- | ------------------ |
| Phê duyệt ban đầu | Đơn giản           |
| Validation        | Kiểm tra nghiệp vụ |
| Giám sát          | Định kỳ            |
| Override          | Không áp dụng      |
| Audit             | Log cơ bản         |

---

## 7. MEDIUM RISK MODELS

### (Mô hình rủi ro trung bình)

---

## 7.1 Định nghĩa

Medium Risk Models là các mô hình:

- Không ra giá trực tiếp
- Nhưng **ảnh hưởng đến quy trình định giá**
- Có thể làm thay đổi mức độ tin cậy hoặc yêu cầu thẩm định thủ công

---

## 7.2 Tiêu chí nhận diện

Mô hình được phân loại Medium Risk nếu:

- Output là score / flag
- Ảnh hưởng đến:
  - Trọng số
  - Quy trình phê duyệt
  - Mức độ kiểm soát
- Không tạo ra giá cuối cùng

---

## 7.3 Ví dụ mô hình Medium Risk

---

### 7.3.1 Trust & Fraud Models

- Listing Trust Score
- Price Anomaly Detection
- Duplicate Listing Detector
- Source Reliability Scorer

---

### 7.3.2 Risk Indicator Models

- Liquidity Score
- Market Volatility Index
- Manipulation Risk Indicator

---

### 7.3.3 Confidence Estimator

- Đánh giá độ chắc chắn
- Quyết định có cần duyệt tay hay không

---

## 7.4 Ảnh hưởng tín dụng

- Ảnh hưởng **gián tiếp**
- Có thể:
  - Yêu cầu bổ sung hồ sơ
  - Kéo dài quy trình
  - Chuyển sang thẩm định thủ công

---

## 7.5 Yêu cầu kiểm soát đối với Medium Risk Models

| Nội dung          | Yêu cầu            |
| ----------------- | ------------------ |
| Phê duyệt ban đầu | Hội đồng mô hình   |
| Validation        | Nghiệp vụ + rủi ro |
| Giám sát          | Định kỳ chặt       |
| Override          | Có log             |
| Audit             | Truy vết đầy đủ    |

---

## 8. HIGH RISK MODELS

### (Mô hình rủi ro cao)

---

## 8.1 Định nghĩa

High Risk Models là các mô hình:

- Tạo ra **ước lượng giá**
- Ảnh hưởng trực tiếp đến kết quả định giá
- Có khả năng tác động đến quyết định tín dụng

---

## 8.2 Tiêu chí nhận diện

Mô hình được xếp High Risk nếu:

- Output là giá trị tiền tệ
- Được sử dụng trong aggregation
- Có thể làm thay đổi kết luận định giá

---

## 8.3 Ví dụ mô hình High Risk

---

### 8.3.1 AVM Core Models

- Hedonic Pricing Model
- Comparable Sales Model
- Cluster-based Pricing
- Cost Approach Model
- Income Approach Model
- Tier-based Regression

---

### 8.3.2 Ensemble & Aggregation Models

- Weighted Price Ensemble
- Bayesian Fusion Model
- Outlier Suppression in Pricing

---

## 8.4 Ảnh hưởng tín dụng

- Ảnh hưởng **trực tiếp**
- Là đầu vào cho:
  - Hội đồng tín dụng
  - Quyết định bảo đảm
  - Định giá tài sản thế chấp

---

## 8.5 Yêu cầu kiểm soát đối với High Risk Models

| Nội dung          | Yêu cầu          |
| ----------------- | ---------------- |
| Phê duyệt ban đầu | Hội đồng cấp cao |
| Validation        | Độc lập          |
| Giám sát          | Liên tục         |
| Override          | Bắt buộc lý do   |
| Audit             | Tái lập kết quả  |

---

## 9. Mapping Model Risk với Kiểm soát

---

## 9.1 Bảng tổng hợp Mapping

| Cấp rủi ro | Kiểm soát dữ liệu | Kiểm soát nghiệp vụ | Giám sát           | Kiểm toán |
| ---------- | ----------------- | ------------------- | ------------------ | --------- |
| Low        | Cơ bản            | Nhẹ                 | Định kỳ            | Giới hạn  |
| Medium     | Chặt              | Trung bình          | Định kỳ tăng cường | Đầy đủ    |
| High       | Rất chặt          | Nghiêm ngặt         | Liên tục           | Bắt buộc  |

---

## 9.2 Mapping với vòng đời mô hình

### 9.2.1 Phát triển

- Low: review nội bộ
- Medium: review chéo
- High: review độc lập

---

### 9.2.2 Triển khai

- Medium & High: cần phê duyệt chính thức

---

### 9.2.3 Vận hành

- High Risk Models có dashboard giám sát riêng

---

### 9.2.4 Nghỉ hưu (Retirement)

- High Risk Models phải có biên bản ngừng sử dụng

---

## 10. LLM trong phân loại rủi ro mô hình

---

## 10.1 Phân loại

LLM được phân loại là:

> **Low Risk – Process Support Model**

---

## 10.2 Điều kiện duy trì Low Risk

LLM chỉ được giữ ở Low Risk nếu:

- Không truy cập output giá
- Không đưa ra khuyến nghị định giá
- Không override quy trình

Nếu vi phạm → nâng cấp rủi ro ngay lập tức.

---

## 11. Rà soát & cập nhật phân loại

---

## 11.1 Tần suất

- Rà soát định kỳ hàng năm
- Rà soát đột xuất khi:
  - Thay đổi mục đích
  - Thị trường biến động mạnh
  - Có sự cố

---

## 11.2 Trách nhiệm

- Bộ phận quản trị mô hình
- Bộ phận rủi ro
- Bộ phận tuân thủ

---

## 12. Giới hạn của khung phân loại

- Không loại bỏ hoàn toàn model risk
- Không thay thế giám sát con người
- Không đảm bảo kết quả tuyệt đối

---

## 13. Kết luận

Khung Model Risk Classification của hệ thống Advanced AVM:

- Phân biệt rõ **mô hình hỗ trợ** và **mô hình ảnh hưởng giá**
- Áp dụng kiểm soát **tương xứng với rủi ro**
- Đảm bảo:
  - Không lạm dụng AI
  - Không né tránh trách nhiệm
  - Không tạo rủi ro mới cho ngân hàng

AI được quản trị như **công cụ nghiệp vụ có rủi ro**,  
không phải giải pháp tự động hóa tuyệt đối.

---
