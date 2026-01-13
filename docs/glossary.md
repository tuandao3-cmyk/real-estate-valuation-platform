# GLOSSARY

_Document initialized automatically._

# GLOSSARY – THUẬT NGỮ AI & THẨM ĐỊNH GIÁ (INTERNAL USE)

**Tài liệu này nhằm mục đích:**

- Chuẩn hóa ngôn ngữ giữa **thẩm định viên truyền thống** và **hệ thống AI/AVM**
- Tránh hiểu sai vai trò của AI trong hoạt động định giá
- Phục vụ đào tạo nội bộ, kiểm toán, và phê duyệt hệ thống

**Nguyên tắc sử dụng:**

- AI là công cụ hỗ trợ phân tích, **không phải chủ thể định giá**
- Thuật ngữ AI được diễn giải theo cách **phi kỹ thuật**, ưu tiên logic nghiệp vụ

---

## BẢNG THUẬT NGỮ

| Thuật ngữ AI                    | Thuật ngữ Thẩm định     | Giải thích dễ hiểu                                                                               |
| ------------------------------- | ----------------------- | ------------------------------------------------------------------------------------------------ |
| AVM (Automated Valuation Model) | Định giá tự động hỗ trợ | Hệ thống sử dụng dữ liệu và quy tắc để hỗ trợ ước tính giá, nhưng không thay thế thẩm định viên. |
| Hybrid AVM                      | Định giá kết hợp        | Mô hình kết hợp giữa kết quả máy tính và đánh giá của con người.                                 |
| Model Output                    | Kết quả mô hình         | Con số/khoảng giá do hệ thống tính toán, cần được thẩm định viên xem xét.                        |
| Confidence Score                | Mức độ tin cậy          | Chỉ số phản ánh độ đầy đủ và ổn định của dữ liệu, không phải cam kết đúng sai.                   |
| Training Data                   | Dữ liệu lịch sử         | Dữ liệu giao dịch, hồ sơ cũ dùng để “dạy” hệ thống nhận biết xu hướng.                           |
| Inference                       | Ước tính                | Quá trình hệ thống đưa ra kết quả từ dữ liệu hiện có.                                            |
| Bias                            | Thiên lệch              | Nguy cơ hệ thống bị lệch nếu dữ liệu đầu vào không đại diện thị trường.                          |
| Feature                         | Biến số so sánh         | Các yếu tố như diện tích, vị trí, pháp lý… tương tự tiêu chí so sánh truyền thống.               |
| Outlier                         | Tài sản dị biệt         | Tài sản có đặc điểm khác thường, cần thẩm định thủ công.                                         |
| Human-in-the-loop               | Thẩm định viên tham gia | Con người luôn kiểm soát và quyết định cuối cùng.                                                |
| Override                        | Điều chỉnh thủ công     | Thẩm định viên ghi đè kết quả AI khi có cơ sở nghiệp vụ.                                         |
| Audit Trail                     | Hồ sơ kiểm soát         | Nhật ký ghi lại mọi thao tác, phục vụ kiểm toán.                                                 |
| Explainability                  | Khả năng giải trình     | Hệ thống phải giải thích được vì sao ra kết quả đó, không phải “hộp đen”.                        |
| Model Governance                | Quản trị mô hình        | Quy trình quản lý, kiểm soát, đánh giá mô hình AI.                                               |
| Data Validation                 | Kiểm tra dữ liệu        | Bước rà soát dữ liệu trước khi dùng để định giá.                                                 |
| Scenario Analysis               | Phân tích kịch bản      | Xem xét giá trị trong các giả định khác nhau.                                                    |
| Stress Test                     | Kiểm tra chịu đựng      | Đánh giá phản ứng mô hình khi thị trường biến động mạnh.                                         |
| LLM (Large Language Model)      | Công cụ soạn thảo       | AI dùng để viết nhận xét, không tham gia tính giá.                                               |
| Hallucination                   | Suy diễn sai            | Khi AI tạo nội dung không có cơ sở dữ liệu, cần kiểm soát chặt.                                  |
| Prompt                          | Yêu cầu đầu vào         | Câu lệnh hướng dẫn AI viết nội dung theo khuôn mẫu.                                              |
| Output Review                   | Soát xét kết quả        | Bước bắt buộc thẩm định viên kiểm tra nội dung AI sinh ra.                                       |
| Traceability                    | Khả năng truy vết       | Có thể lần ngược lại nguồn dữ liệu và quyết định.                                                |
| Compliance                      | Tuân thủ                | Đảm bảo hệ thống phù hợp luật và tiêu chuẩn định giá.                                            |
| Regulatory Mapping              | Đối chiếu pháp lý       | Liên kết chức năng hệ thống với quy định pháp luật.                                              |
| Risk Flag                       | Cảnh báo rủi ro         | Dấu hiệu cho thấy hồ sơ cần xem xét kỹ hơn.                                                      |
| Manual Review                   | Rà soát thủ công        | Thẩm định viên kiểm tra chi tiết từng yếu tố.                                                    |
| Model Limitation                | Giới hạn mô hình        | Những trường hợp AI không phù hợp sử dụng.                                                       |
| Data Freshness                  | Độ mới dữ liệu          | Mức độ cập nhật của thông tin thị trường.                                                        |
| Market Volatility               | Biến động thị trường    | Yếu tố làm giảm độ tin cậy của định giá tự động.                                                 |
| Use Case                        | Mục đích sử dụng        | Lý do định giá: tín dụng, đầu tư, DD…                                                            |
| Purpose-based Valuation         | Định giá theo mục đích  | Cùng tài sản nhưng mục đích khác thì giá khác.                                                   |
| Governance Layer                | Lớp kiểm soát           | Phần hệ thống đảm bảo AI không vượt quyền.                                                       |
| Documentation                   | Hồ sơ nghiệp vụ         | Tài liệu giải trình toàn bộ quá trình định giá.                                                  |
| Accountability                  | Trách nhiệm cuối        | Luôn thuộc về con người, không gán cho AI.                                                       |

---

## GHI CHÚ SỬ DỤNG

- Tài liệu này là **phụ lục bắt buộc** khi đào tạo thẩm định viên sử dụng AVM.
- Mọi thuật ngữ AI khi dùng trong báo cáo phải được hiểu theo bảng này.
- Trường hợp phát sinh thuật ngữ mới, phải được bổ sung và phê duyệt bởi bộ phận quản trị rủi ro.

---

**Kết luận:**
Bảng thuật ngữ này nhằm đảm bảo mọi bên liên quan có cùng cách hiểu, giảm rủi ro diễn giải sai vai trò của AI trong hoạt động thẩm định giá bất động sản.
