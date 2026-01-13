# SYSTEM ARCHITECTURE

_Document initialized automatically._

# SYSTEM ARCHITECTURE

## Advanced AVM – Real Estate AI Valuation Platform

**Compliant with Vietnamese Banking, Audit, and Real-World Valuation Practice**

---

## 1. MỤC ĐÍCH TÀI LIỆU

Tài liệu này mô tả **kiến trúc kỹ thuật tổng thể** của hệ thống Advanced AVM (Automated Valuation Model nâng cao) dùng cho **ngân hàng, quỹ đầu tư, và hoạt động thẩm định giá chuyên nghiệp tại Việt Nam**.

Mục tiêu của tài liệu:

- Ngân hàng đọc hiểu luồng vận hành
- Kiểm toán truy vết được từng quyết định
- Kỹ sư phát triển không vượt ranh giới pháp lý
- Khẳng định rõ: **AI không thay thế thẩm định viên**

Tài liệu này được xem là **xương sống kiến trúc** cho toàn bộ repository `real_estate_ai_platform/`.

---

## 2. TRIẾT LÝ THIẾT KẾ (DESIGN PHILOSOPHY)

### 2.1 AI hỗ trợ – Con người chịu trách nhiệm

Hệ thống được thiết kế theo nguyên tắc:

> **AI chuẩn hóa – kiểm soát – hỗ trợ** > **Con người phân tích – quyết định – chịu trách nhiệm**

Không có bất kỳ model AI nào trong hệ thống:

- Tự đưa ra kết luận pháp lý cuối cùng
- Thay thế chữ ký của thẩm định viên
- Được phép override quy trình phê duyệt

---

### 2.2 Separation of Concerns (Phân tách rõ vai trò)

Toàn bộ kiến trúc được chia thành các lớp độc lập:

1. **Data Layer** – Quản lý dữ liệu & nguồn gốc
2. **Model Layer** – Mô hình định lượng
3. **Valuation Engine** – Logic nghiệp vụ & hội đồng số
4. **Governance Layer** – Kiểm soát rủi ro & tuân thủ
5. **LLM Layer** – Diễn giải, không quyết định
6. **API & UI Layer** – Phục vụ nghiệp vụ thực tế

Mỗi lớp:

- Có input/output rõ ràng
- Có log & audit trail
- Có thể bị kiểm toán độc lập

---

## 3. TỔNG QUAN KIẾN TRÚC HỆ THỐNG

### 3.1 Sơ đồ luồng tổng quát (Logical Flow)

```
Nguồn dữ liệu
   ↓
DATA FOUNDATION (Ingest – Clean – Validate)
   ↓
LISTING INTELLIGENCE (Trust & Verification)
   ↓
FEATURE PIPELINE (Chuẩn hóa đặc trưng)
   ↓
AVM CORE MODELS (Nhiều phương pháp định giá)
   ↓
ENSEMBLE & CONFIDENCE ESTIMATION
   ↓
RISK ADJUSTMENT & BUSINESS RULES
   ↓
VALUATION ENGINE (Approval / Override)
   ↓
LLM ASSISTANT (Giải thích & báo cáo)
   ↓
REPORT & DOSSIER (PDF / API / Audit Export)
```

---

## 4. DATA LAYER – NỀN TẢNG DỮ LIỆU

### 4.1 Vai trò

Data Layer mô phỏng **quy trình tiếp nhận hồ sơ ngoài đời**:

- Nhận thông tin tài sản
- Kiểm tra tính đầy đủ
- Chuẩn hóa và lưu trữ

Không có định giá tại layer này.

---

### 4.2 Data Schemas (Hợp đồng dữ liệu)

Các schema trong `data/schemas/` đóng vai trò **data contract**:

- `property.json`: Thông tin vật lý tài sản
- `listing.json`: Thông tin chào bán
- `transaction.json`: Giao dịch thực
- `legal_status.json`: Pháp lý
- `valuation_request.json`: **Mục đích định giá**

Nguyên tắc:

- Schema bất biến theo version
- Mọi thay đổi phải backward-compatible
- Audit có thể đọc schema mà không cần code

---

### 4.3 Ingest & Cleaning

Nguồn dữ liệu:

- Listing công khai
- Giao dịch lịch sử
- Dữ liệu địa lý
- Tín hiệu thị trường bên ngoài

Pipeline cleaning:

- Chuẩn hóa địa chỉ
- Geocoding
- Loại trùng lặp
- Phát hiện outlier
- Kiểm tra completeness

Nếu dữ liệu **không đạt chuẩn → dừng quy trình**.

---

### 4.4 Lineage & Provenance

Mỗi hồ sơ định giá có:

- Metadata nguồn dữ liệu
- Thời điểm ingest
- Phiên bản dữ liệu

Điều này cho phép:

- Truy ngược từng con số
- Phục vụ tranh chấp pháp lý
- Tái hiện kết quả tại thời điểm quá khứ

---

## 5. LISTING INTELLIGENCE – XÁC THỰC & ĐÁNH GIÁ ĐỘ TIN CẬY

### 5.1 Mục tiêu

Layer này thay thế công đoạn:

> “Đi xem nhà – hỏi môi giới – nghi ngờ tin rác”

Không sinh giá.

---

### 5.2 Trust & Fraud Models

Các model trong nhóm này:

- Chỉ sinh **điểm rủi ro / độ tin cậy**
- Không ảnh hưởng trực tiếp tới giá
- Ảnh hưởng tới **trọng số & yêu cầu xác minh**

Ví dụ:

- Listing Trust Score
- Price Anomaly Detection
- Duplicate Listing
- AI-generated Image Detection

---

### 5.3 Verification Workflow

Luồng xác minh:

- Địa chỉ
- Pháp lý
- Quy hoạch
- Quyền sở hữu
- Tính nhất quán nội dung

Kết quả:

- Pass
- Warning
- Reject (yêu cầu bổ sung)

---

## 6. FEATURE PIPELINE – PHÂN TÍCH CHUYÊN MÔN

### 6.1 Vai trò

Feature pipeline đóng vai trò:

> “Bộ não phân tích kỹ thuật của thẩm định viên”

Chỉ tạo **đặc trưng đầu vào cho model**.

---

### 6.2 Các nhóm feature

- Tabular: diện tích, tầng, mặt tiền
- Image: tình trạng công trình
- Text: mô tả, pháp lý
- Geo: vị trí, cluster

Feature được version hóa và lưu registry.

---

### 6.3 Drift Detection

Hệ thống liên tục kiểm tra:

- Phân phối feature
- So sánh với training data

Nếu drift vượt ngưỡng:

- Gắn cờ model
- Cảnh báo hội đồng model

---

## 7. MODEL LAYER – HỆ SINH THÁI ĐỊNH GIÁ

### 7.1 Nguyên tắc chung

Mỗi model:

- Có input/output rõ ràng
- Có vai trò xác định
- Có log & explainability
- Không tự kết luận

---

### 7.2 AVM Core Models

Bao gồm:

- Hedonic Regression
- Comparable Sales
- Cluster Median Pricing
- Cost Approach
- Income Approach
- Tier-based Models

Mỗi model là **một phương pháp định giá độc lập**.

---

### 7.3 Ensemble Models

Ensemble không "bình quân máy móc" mà:

- Cân theo độ tin cậy
- Loại bỏ outlier
- Ước lượng bất định

Kết quả:

- Giá đề xuất
- Khoảng giá hợp lý
- Confidence score

---

## 8. VALUATION ENGINE – HỘI ĐỒNG THẨM ĐỊNH SỐ

### 8.1 Vai trò trung tâm

Valuation Engine là:

> **Nơi ra quyết định nghiệp vụ**

Không phải model ML.

---

### 8.2 Rule-based Decision

Sử dụng rule YAML:

- Confidence threshold
- Risk band
- Điều kiện reject

Rule có thể đọc bởi:

- Ngân hàng
- Kiểm toán
- Pháp chế

---

### 8.3 Approval & Override

Nếu:

- Confidence thấp
- Rủi ro cao

→ Bắt buộc duyệt tay.

Override:

- Có lý do
- Có người chịu trách nhiệm
- Có audit log

---

## 9. LLM LAYER – HỖ TRỢ DIỄN GIẢI

### 9.1 Nguyên tắc sắt đá

LLM:

- ❌ Không định giá
- ❌ Không override
- ❌ Không quyết định

---

### 9.2 Vai trò hợp lệ

LLM được phép:

- Viết nhận xét thẩm định
- Tóm tắt giả định
- Sinh disclaimer
- Giải trình cho ngân hàng

LLM luôn hoạt động **sau quyết định**.

---

## 10. AUDIT, TRACEABILITY & LEGAL DEFENSIBILITY

### 10.1 Snapshot & Hash

Mỗi hồ sơ:

- Snapshot dữ liệu
- Hash tái lập

Cho phép tái hiện 100%.

---

### 10.2 Audit Trail

Ghi lại:

- Model nào chạy
- Version nào
- Ai override
- Khi nào

---

## 11. KẾT LUẬN KIẾN TRÚC

Hệ thống Advanced AVM này:

- Phù hợp ngân hàng Việt Nam
- Kiểm toán soi được
- Không lạm dụng AI
- Bảo vệ thẩm định viên & tổ chức

> **AI không thay thẩm định viên** > **LLM không ký quyết định** > **Hồ sơ luôn truy vết được**

---

_End of system_architecture.md_
