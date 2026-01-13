Hedonic Model Module – Advanced AVM
Purpose (Non-Negotiable)

Thư mục model/hedonic/ chứa toàn bộ logic mô hình hedonic dùng trong hệ thống Advanced AI-Assisted Valuation Platform (Hybrid AVM).

📌 Hedonic model trong hệ thống này KHÔNG phải là công cụ quyết định giá cuối cùng.
Nó chỉ tạo price projection mang tính mô tả, phục vụ:

Ensemble

Risk analysis

Human appraisal support

Audit & court defensibility

Core Governance Alignment

Module này bị ràng buộc trực tiếp bởi:

MASTER_SPEC.md

IMPLEMENTATION STATUS – ADVANCED AVM

modeling/registry/\*

valuation_dossier.json (Single Source of Truth)

Nguyên tắc bất biến

Model ≠ Valuer

Output ≠ Decision

Không có auto-approval

Không tự học / tự điều chỉnh

Reproducibility là bắt buộc

📌 Bất kỳ thay đổi nào làm vi phạm các nguyên tắc trên → SYSTEM VIOLATION.

Functional Scope
Hedonic model ĐƯỢC PHÉP

Học mối quan hệ thuộc tính ↔ giá từ dữ liệu lịch sử

Tạo ước lượng giá (projection) ở thời điểm inference

Cung cấp feature contribution để giải thích

Xuất residual diagnostics phục vụ MRM

Ghi output read-only vào valuation_dossier.model_outputs.hedonic

Hedonic model TUYỆT ĐỐI KHÔNG

Quyết định giá cuối

Gán confidence workflow

Override rule engine

Override human appraiser

Điều chỉnh output dựa trên override

Fine-tune online / self-training

Directory Structure
model/hedonic/
├── README.md # Tài liệu governance (file này)
├── feature_matrix_builder.py # Xây dựng ma trận feature (deterministic)
├── hedonic_model.py # Inference hedonic (read-only coefficients)
├── residual_analysis.py # Phân tích sai số (offline, diagnostic only)
├── coefficient_store.json # Hệ số model (immutable, audit-grade)
├── output_schema.json # Schema output chuẩn hóa
└── tests/ # Test cho reproducibility & schema

Key Files & Roles
feature_matrix_builder.py

Chuẩn hóa feature đầu vào

Tuân thủ feature_snapshot_hash

Không suy luận, không fill mang tính phán đoán

📌 Feature builder ≠ Feature engineering tùy ý

hedonic_model.py

Load coefficient_store.json

Thực hiện inference thuần toán học

Không áp rule, không clip giá, không điều chỉnh band

📌 Nếu không load được coefficient đúng version → FAIL FAST

coefficient_store.json

Artifact bất biến của model

Gắn chặt với:

model_version

feature_snapshot_hash

Không được sửa ngoài quy trình retraining

📌 Thiếu file này → model KHÔNG reproducible → NON-COMPLIANT

residual_analysis.py

Chỉ dùng cho:

Model Risk Management

Audit

Offline evaluation

Không chạy trong valuation flow

📌 Residual ≠ confidence ≠ approval

output_schema.json

Chuẩn hóa output hedonic

Đảm bảo:

Non-decisive

Explainable

Hashable

Court-defensible

📌 Schema drift không bump version = SYSTEM VIOLATION

Input & Output Contract
Input (Read-only)

valuation_dossier.json

Feature snapshot (by hash)

Model registry metadata

Output (Read-only)

Ghi vào:

valuation_dossier.model_outputs.hedonic.\*

Không được ghi trực tiếp sang:

decision_result

approval_log

rule engine state

Audit & Reproducibility Guarantees

Hedonic module phải đảm bảo:

Same input → same output

Full trace:

model_version

coefficient hash

feature_snapshot_hash

Output có deterministic hash

📌 Không reproducible = không được dùng trong hệ thống ngân hàng.

Relationship to Other Modules
Module Relationship
modeling/registry Kiểm soát activation & version
feature_pipeline Cung cấp feature snapshot
ensemble Có thể aggregate output
risk_engine Chỉ đọc output
override Không ảnh hưởng hedonic logic
LLM Chỉ được giải thích output
Strict Prohibitions (System-Level)

❌ Hedonic tự kích hoạt
❌ Hedonic tự thay đổi hệ số
❌ Dùng hedonic output làm giá cuối
❌ Mapping trực tiếp hedonic → approval
❌ Human override làm thay đổi model output

Final Statement (For Audit / Legal)

Hedonic model trong hệ thống này không thay thế thẩm định viên.
Nó tồn tại để hỗ trợ, chuẩn hóa và tăng tính kiểm toán được cho quy trình định giá.

Nếu một kiểm toán viên hỏi:

“Nếu model này sai, ai chịu trách nhiệm?”

👉 Câu trả lời luôn là: Con người.

Status: ✅ IMPLEMENTED – GOVERNANCE LOCKED
Risk Classification: 🟡 Model Output (Non-Decisive, Controlled)
