# README

_Document initialized automatically._

# 🏗️ Advanced Real Estate AVM

**AI-Assisted Property Valuation Platform**  
**Bank-Grade · Audit-Ready · Human-in-the-Loop**

---

## 1. Giới thiệu chung

**Advanced Real Estate AVM** là nền tảng AI hỗ trợ thẩm định giá bất động sản, được thiết kế dành riêng cho:

- Ngân hàng thương mại
- Tổ chức tín dụng
- Công ty thẩm định giá
- Quỹ đầu tư & Due Diligence

Hệ thống tuân thủ nguyên tắc:

> **AI hỗ trợ – Con người quyết định – Kiểm toán soi được**

Advanced AVM **không phải** hệ thống định giá tự động hoàn toàn (Fully Automated AVM).  
Đây là **Hybrid Valuation System** kết hợp:

- AI đa mô hình
- Quy trình thẩm định thực tế tại Việt Nam
- Phê duyệt & chịu trách nhiệm bởi con người

---

## 2. Mục tiêu thiết kế

### 2.1 Mục tiêu nghiệp vụ

- Chuẩn hóa quy trình thẩm định giá
- Giảm rủi ro chủ quan & gian lận dữ liệu
- Hỗ trợ thẩm định viên phân tích đa chiều
- Phục vụ tín dụng, đầu tư, quản trị rủi ro

### 2.2 Mục tiêu quản trị & kiểm toán

- Truy vết toàn bộ dữ liệu & quyết định
- Không tồn tại “AI nói gì tin nấy”
- Phân định rõ trách nhiệm AI – Con người
- Phù hợp kiểm toán nội bộ & thanh tra

---

## 3. Đối tượng sử dụng

| Nhóm           | Vai trò                          |
| -------------- | -------------------------------- |
| Thẩm định viên | Phân tích, đối chiếu, ký báo cáo |
| Quản lý        | Phê duyệt, override khi cần      |
| Ngân hàng      | Đọc hồ sơ, kiểm soát rủi ro      |
| Kiểm toán      | Truy xuất dữ liệu & quyết định   |
| IT / Data      | Vận hành, giám sát model         |

---

## 4. Nguyên tắc cốt lõi (Design Principles)

1. **Human-in-the-Loop**  
   AI không tự phê duyệt giá trị cuối cùng

2. **Multi-Model Consensus**  
   Không có model đơn lẻ quyết định giá

3. **Policy-Driven AI**  
   AI bị ràng buộc bởi SOP & chính sách

4. **Audit-by-Design**  
   Thiết kế để kiểm toán ngay từ đầu

5. **Explainability First**  
   Giải thích cho con người, không chỉ cho máy

---

## 5. Cấu trúc thư mục tổng thể

real_estate_ai_platform/
├── README.md
├── Makefile
├── pyproject.toml / requirements.txt
├── .env.example
├── docker-compose.yml
│
├── docs/ # Hồ sơ pháp lý & nghiệp vụ
├── model_governance/ # Quản trị vòng đời model
├── risk/ # Stress scenario
├── ops/ # Vận hành & fallback
│
├── tests/ # Kiểm soát chất lượng
├── scripts/ # Công cụ vận hành
│
├── data/ # Data foundation
├── listing_intelligence/ # Trust & fraud
├── feature_pipeline/ # Phân tích chuyên môn
├── modeling/ # Các phương pháp định giá
├── valuation_engine/ # Hội đồng thẩm định số
├── api/ # API trả hồ sơ
└── ui/ # Giao diện người dùng

---

## 6. docs/ – Hồ sơ trình ngân hàng

Thư mục `docs/` tương đương **Sổ tay nội bộ của công ty thẩm định** và **hồ sơ trình ngân hàng**, bao gồm:

- Tổng quan sản phẩm cho lãnh đạo
- Kiến trúc hệ thống
- Chính sách định giá theo chuẩn Việt Nam
- SOP thẩm định giá
- Chính sách sử dụng LLM
- Ma trận trách nhiệm AI – Con người
- Legal defensibility & liability boundary
- Explainability & RAI governance
- Mapping Thông tư & Tiêu chuẩn thẩm định

📌 **Ngân hàng đọc hiểu – kiểm toán soi được – pháp lý bảo vệ được**

---

## 7. tests/ – Kiểm soát nội bộ

Thư mục `tests/` mô phỏng **kiểm soát nội bộ ngân hàng**, bao gồm:

- Kiểm tra chất lượng dữ liệu
- Kiểm tra logic định giá
- Kiểm tra tính ổn định model
- Regression test chống drift
- Kiểm thử luồng phê duyệt & override

---

## 8. data/ – Data Foundation

🎯 Ngoài đời: tiếp nhận hồ sơ khách hàng

Chức năng:

- Chuẩn hóa dữ liệu tài sản
- Quản lý mục đích định giá
- Snapshot từng hồ sơ
- Truy xuất nguồn dữ liệu (data lineage)

📌 **Không đủ hồ sơ → không cho định giá**

---

## 9. listing_intelligence/ – Trust & Fraud

🎯 Ngoài đời: khảo sát thực tế – rà soát pháp lý

Chức năng:

- Phát hiện tin ảo, tin rác
- Kiểm tra trùng lặp
- Phát hiện thao túng giá
- Xác thực ảnh & vị trí

📌 **KHÔNG dùng để ra giá**  
📌 **Chỉ dùng để điều chỉnh trọng số & yêu cầu xác minh**

---

## 10. feature_pipeline/ – Phân tích chuyên môn

🎯 Ngoài đời: thẩm định viên phân tích vị trí & thị trường

- Feature tabular, ảnh, text, geo
- Chấm điểm tình trạng công trình
- Phát hiện drift thị trường
- Chuẩn hóa đầu vào cho AVM core

---

## 11. modeling/ – Hệ sinh thái model định giá

Tổng cộng ~25 model, chia 6 nhóm:

1. Trust & Fraud Models
2. Feature Models
3. AVM Core Models
4. Ensemble Models
5. Risk Models
6. LLM Support Model

📌 Mỗi model đều có:

- Input rõ ràng
- Output định lượng
- Vai trò cụ thể
- Audit & trace được

---

## 12. AVM Core – Phương pháp định giá

Bao gồm:

- Hedonic Pricing
- Comparable Sales
- Cluster-based Pricing
- Cost Approach
- Income Approach (khi phù hợp)
- Tier-based Regression

📌 **Mọi ước lượng đều neo vào dữ liệu giao dịch thực**

---

## 13. Ensemble & Risk Adjustment

- Kết hợp nhiều giá → khoảng giá hợp lý
- Ước lượng confidence score
- Điều chỉnh theo rủi ro thanh khoản & biến động

📌 **Giá thấp confidence → bắt buộc duyệt tay**

---

## 14. valuation_engine/ – Hội đồng thẩm định số

🎯 Ngoài đời: hội đồng thẩm định

Chức năng:

- Áp rule nghiệp vụ
- Escalation khi rủi ro cao
- Lưu snapshot quyết định
- Ghi log override

📌 **AI đề xuất – Con người ký**

---

## 15. LLM – Vai trò giới hạn rõ ràng

LLM trong hệ thống:

- ❌ Không ra giá
- ❌ Không override model
- ❌ Không quyết định phê duyệt

LLM chỉ:

- Viết nhận xét thẩm định
- Tóm tắt giả định & hạn chế
- Chuẩn hóa ngôn ngữ báo cáo
- Giải trình cho ngân hàng & kiểm toán

🧠 _LLM là người viết biên bản, không phải người ký_

---

## 16. API – Trả hồ sơ, không chỉ trả giá

API trả về:

- Giá trị đề xuất
- Khoảng giá hợp lý
- Confidence score
- Risk band
- Hồ sơ định giá đầy đủ (valuation dossier)

📌 **Ngân hàng không nhận “1 con số trơ trọi”**

---

## 17. UI – Mô phỏng công ty thẩm định thật

- Giao diện thẩm định viên
- Giao diện quản lý
- Xuất báo cáo PDF
- Lưu trữ báo cáo đã ký

---

## 18. Luồng quyết định tổng thể

Listing Data
↓ Trust & Fraud Models
↓ Feature Engineering
↓ AVM Core (nhiều giá)
↓ Ensemble & Confidence
↓ Risk Adjustment
↓ Rule / Approval
↓ LLM → Báo cáo

---

## 19. Kết luận cho ngân hàng

- AI **không thay thẩm định viên**
- AI **chuẩn hóa – kiểm soát – hỗ trợ**
- Mọi quyết định:
  - Có dữ liệu
  - Có logic
  - Có người chịu trách nhiệm

**Advanced Real Estate AVM** được xây dựng để:

- Phục vụ tín dụng thận trọng
- Hỗ trợ đầu tư dài hạn
- Đứng vững trước kiểm toán & thanh tra

---

📌 _Advanced Real Estate AVM – Built for Trust, Governance, and Real-World Valuation._
