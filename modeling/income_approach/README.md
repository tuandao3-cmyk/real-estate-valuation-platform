Income Approach Module

(Governance-Locked – Non-Decisional Valuation Signal)

1. Purpose & Governance Role

Module Income Approach triển khai phương pháp thu nhập (NOI / Cap Rate) với mục tiêu duy nhất:

👉 Sinh ra một tín hiệu định giá mang tính tham chiếu (indicative signal)
❌ KHÔNG phải Market Value
❌ KHÔNG được dùng để phê duyệt, quyết định, hay ghi đè hệ thống

Governance Classification

Risk Group: 🟦 Nhóm B – Model Output (Human-dependent)

Decision Authority: ❌ None

Legal Standing: ❌ Không có giá trị pháp lý độc lập

Audit Role: Evidence-supporting only

2. Absolute Constraints (MANDATORY)

Module này bị khóa cứng bởi các nguyên tắc sau:

❌ Không auto-activate

❌ Không tự chọn Cap Rate

❌ Không suy luận dòng tiền

❌ Không điều chỉnh assumption

❌ Không đưa ra quyết định giá cuối

❌ Không ghi đè valuation_dossier.json

➡️ Mọi output chỉ được ghi vào valuation_dossier.json như READ-ONLY SIGNAL

3. Architecture Overview
   income_approach/
   ├── activation_check.py # Kiểm tra điều kiện được phép chạy (workflow-only)
   ├── rental_assumption.yaml # Assumption tĩnh, governance-approved
   ├── cap_rate_table.yaml # Cap rate reference table (human-selected)
   ├── income_model.py # Tính toán cơ học NOI / Cap Rate
   ├── output_schema.json # Schema output (non-decisional)
   └── README.md # (This file)

4. Module Responsibilities
   4.1 activation_check.py

Vai trò: Workflow gate

Kiểm tra:

Asset type có cho phép Income Approach không

Có đủ dữ liệu vận hành không

❌ Không kích hoạt model

❌ Không trả về giá trị

4.2 rental_assumption.yaml

Assumption tĩnh, được phê duyệt governance

Không cá nhân hóa theo tài sản

Versioned & auditable

❌ Không điều chỉnh runtime

4.3 cap_rate_table.yaml

Bảng cap rate tham chiếu

Cap rate phải do con người chọn

Model chỉ sử dụng giá trị đã được xác nhận

❌ Không nội suy

❌ Không tự tối ưu

4.4 income_model.py

Thực hiện phép tính thuần cơ học:

Indicated Value = NOI / Cap Rate

Không heuristic

Không weighting

Không ensemble

Không confidence scoring

4.5 output_schema.json

Định nghĩa output phi quyết định

Bắt buộc:

Governance flags

Limitation disclosure

Version metadata

❌ Không cho phép thiếu context

5. Data Flow & SSOT Compliance
   valuation_dossier.json (SSOT)
   ↓ (read-only)
   activation_check.py
   ↓
   income_model.py
   ↓
   output_schema.json
   ↓
   valuation_dossier.json (append-only signal)

📌 Nếu không có valuation_dossier.json → module không được phép chạy

6. Legal & Audit Guarantees

Output:

Hashable

Replayable

Deterministic

Mọi version:

Assumption

Cap rate table

Code
→ đều phải xuất hiện trong audit trace

➡️ Không có audit trail = output vô hiệu

7. Explicit Non-Goals

Module này KHÔNG:

Đánh giá Market Value

Thay thế thẩm định viên

Tự động phê duyệt

So sánh với Sales / Cost Approach

Điều chỉnh rủi ro

Sinh confidence score

8. Integration Rules

Chỉ được tiêu thụ bởi:

Ensemble layer (read-only)

Human appraisal review

❌ Không cho phép:

Core banking dùng trực tiếp

LOS auto-approve

External API expose raw value

9. Compliance Checklist (ENFORCED)
   Rule Status
   valuation_dossier là SSOT ✅
   Human chọn Cap Rate ✅
   Output phi quyết định ✅
   Audit-ready ✅
   No auto-activation ✅
   MASTER_SPEC compliant ✅
10. Final Governance Statement

Income Approach trong hệ thống này là một công cụ tính toán hỗ trợ,
không phải là thẩm định viên,
không có thẩm quyền pháp lý,
và không bao giờ được xem là quyết định cuối.

🔒 FILE STATUS: GOVERNANCE LOCKED
📄 LAST REVIEW: Manual Spec Alignment
⚠️ MODIFICATION: Requires Governance Approval
