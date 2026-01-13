# LLM USAGE POLICY

_Document initialized automatically._

# CHÍNH SÁCH SỬ DỤNG MÔ HÌNH NGÔN NGỮ LỚN (LLM USAGE POLICY)

**Phiên bản:** 1.0 (Internal – Audit Ready)

**Áp dụng cho:** Hệ thống Advanced AVM – Hybrid AI + Thẩm định thủ công

**Đối tượng áp dụng:** Ngân hàng, Quỹ đầu tư, Đơn vị Due Diligence (DD)

**Tham chiếu:**

- Tiêu chuẩn Thẩm định giá Việt Nam (TĐGVN)
- Khung quản trị rủi ro mô hình ngân hàng (Model Risk Management)
- Nguyên tắc AI có trách nhiệm (Responsible AI)

---

## 1. MỤC ĐÍCH VÀ PHẠM VI

Tài liệu này quy định **nguyên tắc, phạm vi, giới hạn và cơ chế kiểm soát** đối với việc sử dụng Mô hình Ngôn ngữ Lớn (Large Language Model – LLM) trong hệ thống Advanced AVM.

Mục tiêu của chính sách là:

- Đảm bảo LLM **không can thiệp vào hoạt động định giá**
- Phòng ngừa rủi ro sai lệch, suy diễn, hoặc “hallucination”
- Thiết lập **ranh giới trách nhiệm rõ ràng** giữa con người – mô hình định lượng – LLM
- Đảm bảo mọi đầu ra của LLM **có thể audit, truy vết và tái lập**

LLM trong hệ thống này **không được xem là mô hình định giá**, không thuộc nhóm AVM core models và **không có tư cách tham gia quyết định giá trị tài sản**.

---

## 2. NGUYÊN TẮC NỀN TẢNG (FOUNDATIONAL PRINCIPLES)

### 2.1. Nguyên tắc không quyết định (Non-Decision Principle)

LLM **không được phép**:

- Đề xuất giá trị bất động sản
- Điều chỉnh, hiệu chỉnh hoặc khuyến nghị thay đổi giá trị
- Lựa chọn phương pháp định giá
- Thay thế, mô phỏng hoặc đại diện vai trò thẩm định viên

Mọi giá trị định lượng liên quan đến giá **chỉ có thể** được tạo ra bởi:

- Các mô hình AVM đã được phê duyệt
- Hoặc quyết định thủ công của thẩm định viên có thẩm quyền

### 2.2. Nguyên tắc hỗ trợ có kiểm soát (Controlled Assistance)

LLM chỉ được sử dụng như **công cụ hỗ trợ hành chính – diễn giải – chuẩn hóa ngôn ngữ**, tương đương vai trò:

> “Thư ký nghiệp vụ / Trợ lý soạn thảo”

### 2.3. Nguyên tắc con người chịu trách nhiệm cuối cùng

Mọi nội dung do LLM sinh ra:

- Phải được **con người kiểm tra, xác nhận hoặc chỉnh sửa**
- Không có giá trị pháp lý độc lập
- Không được coi là ý kiến chuyên môn

---

## 3. PHẠM VI ĐƯỢC PHÉP SỬ DỤNG (WHAT LLM IS ALLOWED TO DO)

LLM chỉ được phép thực hiện các nhóm chức năng sau:

### 3.1. Viết nhận xét thẩm định (Narrative Generation)

- Diễn giải kết quả định giá đã có
- Mô tả bối cảnh thị trường bằng ngôn ngữ trung lập
- Soạn thảo phần nhận xét tổng hợp dựa trên dữ liệu đầu vào đã được khóa

### 3.2. Tóm tắt thông tin (Summarization)

- Tóm tắt hồ sơ tài sản
- Tóm tắt danh sách mô hình đã kích hoạt
- Tóm tắt các rủi ro đã được hệ thống phát hiện

### 3.3. Chuẩn hóa ngôn ngữ (Language Normalization)

- Chuẩn hóa thuật ngữ giữa các báo cáo
- Chuyển đổi nội dung kỹ thuật sang ngôn ngữ dễ hiểu cho lãnh đạo
- Đảm bảo văn phong nhất quán trong toàn bộ hồ sơ

### 3.4. Sinh nội dung phụ trợ (Ancillary Content)

- Giả định định giá (Assumptions)
- Hạn chế và điều kiện sử dụng (Limitations)
- Checklist xác minh thủ công cho thẩm định viên

---

## 4. PHẠM VI BỊ CẤM TUYỆT ĐỐI (WHAT LLM IS NOT ALLOWED TO DO)

LLM **bị cấm tuyệt đối** trong các trường hợp sau:

- Sinh hoặc đề xuất **bất kỳ con số giá trị** nào
- Thực hiện phép tính, suy diễn định lượng
- Điều chỉnh kết quả của AVM hoặc con người
- Đưa ra kết luận phê duyệt / từ chối hồ sơ
- Đánh giá tính hợp pháp của tài sản
- Đưa ra khuyến nghị tín dụng hoặc đầu tư

Mọi vi phạm phạm vi này được xem là **sự cố kiểm soát AI (AI Control Incident)**.

---

## 5. KIỂM SOÁT HALLUCINATION

### 5.1. Kiểm soát đầu vào (Input Control)

- LLM chỉ được truy cập dữ liệu đã được khóa (read-only)
- Không có quyền truy vấn dữ liệu thô hoặc dữ liệu ngoài hồ sơ

### 5.2. Kiểm soát prompt

- Prompt được chuẩn hóa, versioned và phê duyệt
- Cấm prompt mở yêu cầu suy diễn giá trị

### 5.3. Kiểm soát đầu ra (Output Guardrails)

- Tự động kiểm tra từ khóa liên quan đến giá
- Tự động chặn số liệu định lượng không nằm trong metadata cho phép

### 5.4. Human Review bắt buộc

- Mọi nội dung LLM sinh ra đều phải được người dùng xác nhận
- Không có chế độ auto-publish

---

## 6. LOGGING, TRACEABILITY & AUDIT TRAIL

### 6.1. Nhật ký hoạt động LLM

Mỗi lần gọi LLM phải được ghi nhận:

- Thời gian
- Người khởi tạo
- Mục đích sử dụng
- Phiên bản prompt

### 6.2. Lưu trữ đầu ra

- Output LLM được lưu snapshot
- Gắn với hồ sơ định giá tương ứng

### 6.3. Khả năng tái lập (Reproducibility)

- Có thể tái tạo lại nội dung LLM với cùng input và prompt
- Phục vụ kiểm toán nội bộ và bên ngoài

---

## 7. QUẢN TRỊ RỦI RO & XỬ LÝ VI PHẠM

- Mọi sai lệch vượt phạm vi được ghi nhận là sự cố
- Sự cố LLM không làm thay đổi kết quả định giá
- Trách nhiệm cuối cùng thuộc về đơn vị vận hành

---

## 8. HIỆU LỰC & RÀ SOÁT

- Chính sách có hiệu lực từ ngày phê duyệt
- Được rà soát tối thiểu hàng năm
- Mọi thay đổi phải được phê duyệt bởi Hội đồng Quản trị Mô hình

---

## 9. TUYÊN BỐ CUỐI

LLM trong hệ thống Advanced AVM **không phải chuyên gia thẩm định**, không có tư cách pháp lý và không thay thế con người.

LLM chỉ là công cụ hỗ trợ ngôn ngữ, nhằm nâng cao tính nhất quán, minh bạch và khả năng giải trình của hồ sơ thẩm định.
