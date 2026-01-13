modeling/registry/README.md
PURPOSE & GOVERNANCE ROLE

Thư mục modeling/registry/ là trung tâm đăng ký (Model Registry) của toàn bộ hệ thống AVM.

📌 Mục đích duy nhất:

Quản lý metadata, versioning, auditability và governance của các mô hình định giá và mô hình phụ trợ.

❌ KHÔNG PHẢI nơi:

Train model

Chạy inference

Ensemble

Tối ưu thuật toán

Ra quyết định giá

📌 Thư mục này KHÔNG BAO GIỜ can thiệp vào workflow hay kết quả định giá.

COMPLIANCE STATEMENT (NON-NEGOTIABLE)

Thư mục này tuân thủ tuyệt đối:

MASTER_SPEC.md

Nguyên tắc AI is not a valuer

Nguyên tắc LLM is clerical only

Nguyên tắc Multi-model, no single truth

Nguyên tắc Audit > Accuracy

📌 Nếu metadata của model không tồn tại hoặc không hợp lệ → model đó KHÔNG ĐƯỢC PHÉP tham gia hệ thống.

CORE RESPONSIBILITIES

Model Registry CHỈ chịu trách nhiệm:

Đăng ký model (registration)

Quản lý version

Lưu business role

Khai báo input / output schema

Lưu giới hạn sử dụng (limitations)

Cung cấp audit trail

Cho phép kiểm toán truy xuất lịch sử

FORBIDDEN RESPONSIBILITIES 🚫

Registry TUYỆT ĐỐI KHÔNG:

So sánh model

Chọn model tốt nhất

Quyết định model nào được dùng trong valuation

Thay đổi trọng số ensemble

Trigger retraining

Đánh giá chất lượng business

📌 Registry là sổ đăng ký pháp lý, không phải bộ não hệ thống.

REQUIRED MODEL METADATA (MANDATORY)

Mỗi model đăng ký BẮT BUỘC phải có đầy đủ các trường sau:

1. Identity

model_id

model_name

model_type (AVM_CORE / FEATURE / RISK / TRUST)

owner_team

business_owner

2. Versioning

version

release_date

status (active / deprecated / retired)

change_log

3. Business Role

intended_use

explicitly_not_used_for

decision_authority = NONE

📌 Mọi model đều có decision_authority = NONE

4. Input Specification

Input schema (validated)

Data source reference

Required / optional fields

Data freshness assumptions

📌 Input schema phải khớp 100% với feature pipeline.

5. Output Specification

Output schema

Unit (VND, score, band…)

Uncertainty expression

Confidence meaning

📌 Output KHÔNG ĐƯỢC là final price.

6. Limitations & Risks

Known bias

Data sparsity zones

Market regimes not covered

Regulatory constraints

📌 Model không có limitations → NON-COMPLIANT

7. Performance (Reference Only)

Validation metrics

Backtest window

Benchmark context

📌 Metrics KHÔNG DÙNG để tự động chọn model.

8. Audit & Traceability

Training data description

Snapshot hash

Reproducibility notes

Audit contact

MODEL LIFECYCLE GOVERNANCE

Model lifecycle trong registry:

Draft
↓
Reviewed
↓
Approved (Governance)
↓
Active
↓
Deprecated
↓
Retired (Read-only)

📌 Registry không tự promote trạng thái.
📌 Mọi thay đổi trạng thái đều cần governance approval.

RELATION TO OTHER MODULES
Module Relationship
feature_pipeline Registry chỉ tham chiếu schema
avm_core_models Registry lưu metadata, không gọi model
ensemble_engine Registry không biết trọng số
risk_engine Registry không điều chỉnh band
valuation_dossier Registry không ghi dossier
LLM Registry không expose số liệu
FAILURE MODES (INTENTIONAL)

Registry được thiết kế fail-fast:

Thiếu metadata → ERROR

Version trùng → ERROR

Schema mismatch → ERROR

Unknown status → ERROR

📌 Fail sớm để bảo vệ tính pháp lý.

AUDITOR VIEW

Một auditor có thể dùng registry để trả lời:

Model này dùng để làm gì?

Ai chịu trách nhiệm?

Dữ liệu huấn luyện từ đâu?

Version nào được dùng tại thời điểm định giá X?

Model có bị dùng sai mục đích không?

📌 Nếu registry không trả lời được → hệ thống KHÔNG ĐẠT CHUẨN.

FINAL STATEMENT

modeling/registry/ tồn tại để đảm bảo rằng:

Không có model nào được sử dụng trong hệ thống mà không thể giải thích, truy vết và bảo vệ trước pháp luật.

📌 Registry không thông minh, nhưng cực kỳ quan trọng.
