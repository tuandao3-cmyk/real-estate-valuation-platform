# MA TRẬN TRÁCH NHIỆM (RESPONSIBILITY MATRIX)

**Phiên bản:** 1.0 (Internal Control Standard)
**Áp dụng cho:** Advanced AVM – Hybrid AI + Thẩm định thủ công
**Mục tiêu:** Xác lập rõ ràng trách nhiệm con người, loại bỏ hoàn toàn rủi ro hiểu nhầm rằng AI hoặc LLM chịu trách nhiệm pháp lý, nghiệp vụ hoặc tín dụng.

---

## 1. NGUYÊN TẮC CHUNG

1. AI và LLM **không phải chủ thể chịu trách nhiệm** theo bất kỳ nghĩa pháp lý, nghiệp vụ hay quản trị rủi ro nào.
2. Mọi kết quả định giá chỉ có giá trị khi được **con người có thẩm quyền xem xét, phê duyệt và ký xác nhận**.
3. Trách nhiệm được phân tách theo nguyên tắc:

   - Phát sinh (Execution)
   - Kiểm soát (Control)
   - Phê duyệt (Approval)
   - Trách nhiệm cuối cùng (Accountability)

4. Ma trận này là tài liệu bắt buộc trong:

   - Hồ sơ phê duyệt hệ thống AVM
   - Hồ sơ quản trị rủi ro mô hình (Model Risk Management)
   - Hồ sơ kiểm toán nội bộ và kiểm toán độc lập

---

## 2. ĐỊNH NGHĨA VAI TRÒ

### 2.1. AI Model (AVM Models)

- Bao gồm: mô hình so sánh, chi phí, thu nhập, mô hình hỗ trợ thống kê
- Vai trò: xử lý dữ liệu, tạo kết quả trung gian
- **Không có thẩm quyền quyết định**

### 2.2. LLM (Large Language Model)

- Vai trò: hỗ trợ ngôn ngữ
- Chỉ thực hiện các tác vụ phi quyết định

### 2.3. Thẩm định viên

- Cá nhân có chứng chỉ hành nghề hợp pháp theo quy định pháp luật Việt Nam
- Chịu trách nhiệm nghiệp vụ trực tiếp

### 2.4. Trưởng bộ phận Thẩm định / Quản lý rủi ro

- Vai trò kiểm soát cấp quản lý
- Đảm bảo tuân thủ chính sách

### 2.5. Hội đồng tín dụng / Hội đồng đầu tư

- Cơ quan quyết định cuối cùng về tín dụng hoặc đầu tư
- Chịu trách nhiệm tập thể theo quy chế nội bộ

---

## 3. MA TRẬN TRÁCH NHIỆM TỔNG HỢP

| Hoạt động / Vai trò            | AI Model  | LLM             | Thẩm định viên       | Trưởng bộ phận       | Hội đồng tín dụng |
| ------------------------------ | --------- | --------------- | -------------------- | -------------------- | ----------------- |
| Thu thập & xử lý dữ liệu       | Thực hiện | Không           | Giám sát             | Giám sát             | Không             |
| Sinh kết quả định giá sơ bộ    | Thực hiện | Không           | Kiểm tra             | Giám sát             | Không             |
| Phân tích pháp lý & hiện trạng | Không     | Hỗ trợ ngôn ngữ | **Chịu trách nhiệm** | Giám sát             | Không             |
| Lựa chọn phương pháp định giá  | Không     | Không           | **Chịu trách nhiệm** | Phê duyệt            | Không             |
| Điều chỉnh giả định            | Không     | Không           | **Chịu trách nhiệm** | Phê duyệt            | Không             |
| Tổng hợp báo cáo định giá      | Không     | Hỗ trợ          | **Chịu trách nhiệm** | Giám sát             | Không             |
| Soát xét nội bộ                | Không     | Không           | Hỗ trợ               | **Chịu trách nhiệm** | Không             |
| Phê duyệt nghiệp vụ định giá   | Không     | Không           | Đề xuất              | **Phê duyệt**        | Không             |
| Quyết định tín dụng / đầu tư   | Không     | Không           | Không                | Tham mưu             | **Ký cuối**       |

---

## 4. PHÂN TÁCH TRÁCH NHIỆM CHI TIẾT THEO RACI

### 4.1. AI Model

- **Responsible:** Không
- **Accountable:** Không
- **Consulted:** Không
- **Informed:** Không

> AI Model được coi là công cụ kỹ thuật. Mọi kết quả chỉ mang tính tham khảo.

### 4.2. LLM

- **Responsible:** Không
- **Accountable:** Không
- **Consulted:** Không
- **Informed:** Không

> LLM không được phép tạo, đề xuất hoặc điều chỉnh giá trị.

### 4.3. Thẩm định viên

- **Responsible:** Có
- **Accountable:** Có (nghiệp vụ)
- **Consulted:** Có
- **Informed:** Có

> Thẩm định viên là chủ thể chịu trách nhiệm chuyên môn trực tiếp.

### 4.4. Trưởng bộ phận

- **Responsible:** Có (kiểm soát)
- **Accountable:** Có (quản lý)
- **Consulted:** Có
- **Informed:** Có

### 4.5. Hội đồng tín dụng

- **Responsible:** Không
- **Accountable:** **Có (cuối cùng)**
- **Consulted:** Có
- **Informed:** Có

---

## 5. CÁC NGUYÊN TẮC CẤM GẮN TRÁCH NHIỆM CHO AI

1. Không sử dụng cụm từ:

   - “AI quyết định giá”
   - “Giá do hệ thống AI phê duyệt”

2. Không ghi tên AI/LLM trong bất kỳ mục nào yêu cầu chữ ký.
3. Không sử dụng output AI làm căn cứ duy nhất cho quyết định tín dụng.

---

## 6. LIÊN KẾT VỚI CÁC CHÍNH SÁCH KHÁC

- Valuation Policy & Methodology
- Valuation Purpose Policy
- LLM Usage Policy
- Model Governance Policy
- Human-in-the-loop Policy

---

## 7. GIÁ TRỊ KIỂM TOÁN

Ma trận này được sử dụng để:

- Chứng minh trách nhiệm con người
- Phản biện rủi ro "AI quyết định"
- Đáp ứng yêu cầu của kiểm toán nội bộ, Big4 và cơ quan quản lý

---

**Kết luận:**
Trong mọi trường hợp, **AI và LLM không và không bao giờ là chủ thể chịu trách nhiệm**. Trách nhiệm luôn thuộc về con người theo phân cấp được phê duyệt.

<!-- # RESPONSIBILITY MATRIX

_Document initialized automatically._

# MA TRẬN TRÁCH NHIỆM: AI vs CON NGƯỜI (RACI)

## 1. Tuyên bố miễn trừ (Disclaimer)

Hệ thống AI đóng vai trò là **Trợ lý phân tích (Analytical Assistant)**, KHÔNG đóng vai trò là **Thẩm định viên (Appraiser)**. Mọi chứng thư định giá phát hành ra bên ngoài bắt buộc phải có chữ ký của Thẩm định viên có thẻ hành nghề.

## 2. Quy trình phê duyệt (Approval Workflow)

| Mức độ tin cậy (Confidence Score) | Rủi ro phát hiện         | Hành động của AI                           | Trách nhiệm con người                                               |
| :-------------------------------- | :----------------------- | :----------------------------------------- | :------------------------------------------------------------------ |
| **Cao (> 0.85)**                  | Thấp                     | Đề xuất giá, Tự động soạn thảo Báo cáo     | **Review nhanh (L1)**: Cán bộ định giá kiểm tra và duyệt.           |
| **Trung bình (0.60 - 0.85)**      | Trung bình (Vd: Ít tsss) | Đề xuất khoảng giá, Cảnh báo các biến số   | **Thẩm định chi tiết (L2)**: Cán bộ phải điều chỉnh hệ số thủ công. |
| **Thấp (< 0.60)**                 | Cao (Vd: Quy hoạch lạ)   | **KHÔNG ra giá**, Chỉ cung cấp dữ liệu thô | **Thẩm định hiện trường (L3)**: Bắt buộc đi khảo sát thực tế 100%.  |

## 3. Quyền hạn can thiệp (Manual Override)

- Con người có quyền ghi đè (override) kết quả của AI bất cứ lúc nào.
- Mọi hành động ghi đè phải đi kèm:
  1. Lý do cụ thể (Chọn từ danh sách hoặc nhập text).
  2. Bằng chứng đính kèm (Ảnh chụp, văn bản pháp lý mới).
- Hệ thống sẽ lưu vết (Audit Trail) toàn bộ các lần ghi đè này. -->
