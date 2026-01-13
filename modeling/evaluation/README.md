Model Evaluation Module – Governance & Usage README

1. PURPOSE (LEGAL & GOVERNANCE FIRST)

Thư mục model/evaluation/ tồn tại chỉ để phục vụ:

Đánh giá OFFLINE hiệu năng & ổn định của model

Phục vụ Model Risk Management (MRM)

Cung cấp bằng chứng định lượng cho:

Audit nội bộ

Hội đồng mô hình

Tranh chấp / kiểm toán / tòa án

🚫 Module này KHÔNG tham gia valuation runtime
🚫 Không có quyền quyết định, kích hoạt, hay loại bỏ model

Evaluation ≠ Approval ≠ Activation ≠ Valuation

2. ABSOLUTE GOVERNANCE BOUNDARIES
   2.1 WHAT THIS MODULE IS ALLOWED TO DO

✔ Chạy backtest trên dữ liệu lịch sử
✔ Tính metric thuần toán học (MAE, RMSE, MAPE, R²…)
✔ Kiểm tra ổn định theo thời gian / phân phối
✔ So sánh mô tả giữa các model
✔ Sinh artifact read-only, immutable

2.2 WHAT THIS MODULE IS STRICTLY FORBIDDEN TO DO

❌ PASS / FAIL model
❌ Xếp hạng model “tốt nhất”
❌ Đề xuất activation / retirement
❌ Sinh threshold hành động
❌ Được gọi từ valuation_flow.py
❌ Tự động trigger governance action

📌 Mọi diễn giải đều phải do con người thực hiện

3. FILE & ROLE OVERVIEW
   3.1 Core Evaluation Files
   File Role Governance Level
   metrics_regression.py Tính metric regression thuần số học 🟢 Numeric only
   backtest_runner.py Orchestrator chạy backtest offline 🟡 Control logic
   stability_check.py Kiểm tra độ ổn định model 🟡 Descriptive
   benchmark_report.json Báo cáo benchmark cho human 🟢 Evidence
   README.md Tài liệu pháp lý & audit 🔒 LOCKED
   3.2 Artifact Nature

Tất cả output từ module này là:

Offline

Descriptive

Non-decisive

Audit-traceable

Reproducible

📌 Artifact ở đây = Evidence, không phải Instruction

4. DATA & EXECUTION CONSTRAINTS
   4.1 Input Constraints

Dữ liệu lịch sử đã đóng băng

Có dataset_id, time_range, jurisdiction

Không được:

Clean lại dữ liệu runtime

Fill missing bằng suy luận

Trộn dữ liệu ngoài scope

4.2 Execution Constraints

Chạy ngoài valuation pipeline

Không được gọi bởi API production

Không được chạy theo schedule tự động kích hoạt model

📌 Evaluation luôn là hoạt động có chủ đích & có kiểm soát

5. RELATION TO MODEL REGISTRY

Evaluation module:

❌ KHÔNG đăng ký model

❌ KHÔNG kích hoạt model

❌ KHÔNG retire model

❌ KHÔNG thay đổi registry state

Chỉ có thể:

✔ Tham chiếu model_registry.yaml
✔ Ghi nhận model_id, version, artifact_hash

6. HUMAN INTERPRETATION REQUIREMENT

Mọi kết quả evaluation:

Phải được đọc bởi:

Model Owner

Risk Officer

Valuation Governance Committee (nếu cần)

Phải được:

Ghi biên bản

Lưu log quyết định

Lý giải bằng ngôn ngữ nghiệp vụ

📌 Không có “auto conclusion” trong hệ thống này

7. AUDIT & COURT DEFENSE STATEMENT

Module model/evaluation/ được thiết kế để:

Chứng minh nỗ lực quản trị mô hình hợp lý

Cho phép forensic replay

Chịu được cross-examination pháp lý

Sự tồn tại của evaluation ≠ khẳng định model đúng
Chỉ khẳng định hệ thống có trách nhiệm

8. CHANGE MANAGEMENT

Bất kỳ thay đổi nào trong thư mục này yêu cầu:

Version bump rõ ràng

Ghi chú lý do

Đánh giá rủi ro

Không ảnh hưởng artifact lịch sử

📌 Silent change = SYSTEM VIOLATION

9. FINAL GOVERNANCE STATEMENT

Model Evaluation trong hệ thống này không nhằm tìm model tốt nhất.

Nó tồn tại để:

Giới hạn rủi ro

Minh bạch hành vi

Bảo vệ con người ra quyết định

AI hỗ trợ đánh giá.
Con người chịu trách nhiệm cuối.

🛑 END OF MODEL EVALUATION README – GOVERNANCE LOCKED
