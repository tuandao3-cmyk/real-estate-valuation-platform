Cost Approach Module – Governance & Implementation Notes

1. PURPOSE & LEGAL POSITIONING

Module Cost Approach cung cấp tham chiếu định giá theo chi phí (cost-based reference) nhằm:

Hỗ trợ human appraiser trong việc đối chiếu

Cung cấp một trụ tham chiếu độc lập trong hệ sinh thái AVM đa mô hình

Phục vụ ensemble reasoning, không phải kết luận

📌 Cost Approach trong hệ thống này KHÔNG PHẢI là giá trị thị trường cuối cùng.
📌 Module này không có quyền quyết định, phê duyệt, hay điều chỉnh workflow.

2. ROLE DEFINITION (NON-NEGOTIABLE)
   Thuộc tính Quy định
   Model Type COST_APPROACH_REFERENCE
   Decision Authority NONE
   Output Nature Descriptive, arithmetic
   Legal Standing Supporting evidence only
   Human Override Always allowed
   Auto Approval ❌ Forbidden

📌 Cost Approach ≠ Valuer
📌 Cost Approach ≠ Final Price Engine

3. ARCHITECTURAL BOUNDARIES
   3.1 WHAT THIS MODULE DOES

✔ Tính toán Replacement Cost New (RCN) từ bảng chi phí chuẩn
✔ Áp dụng depreciation curve tĩnh
✔ Tổng hợp total cost reference (structure + land reference)
✔ Sinh output hashable, reproducible

3.2 WHAT THIS MODULE MUST NEVER DO

❌ Không suy luận giá thị trường
❌ Không tối ưu theo outcome
❌ Không học từ override / approval
❌ Không sửa input khác
❌ Không bypass rule / human layer

📌 Mọi hành vi vượt ranh giới trên = SYSTEM VIOLATION

4. DATA & INPUT GOVERNANCE
   Mandatory Inputs (Read-only)

valuation_dossier.json (SSOT)

feature_snapshot_hash

Approved construction cost table

Static depreciation curve

Land value reference (external / approved)

📌 Module không được:

Recompute feature

Fill missing data bằng suy luận

Fallback sang heuristic ngầm

5. OUTPUT CONTRACT
   Output File

output_schema.json

Key Governance Guarantees

Không chứa:

confidence_score

risk_band

approval_hint

decision_flag

Mọi giá trị đều:

Arithmetic

Explainable

Traceable

📌 Field total_cost_reference chỉ mang ý nghĩa tham chiếu, không phải kết luận.

6. REPRODUCIBILITY & AUDIT

Module này bắt buộc đáp ứng:

Deterministic execution

Explicit versioning

SHA-256 audit hash

Snapshot-based replay

📌 Nếu không tái hiện được kết quả → output vô hiệu về mặt pháp lý

7. MODEL RISK CLASSIFICATION
   Dimension Assessment
   Model Risk 🟡 Medium
   Decision Impact None
   Automation Level Low
   Audit Sensitivity High
   Regulatory Exposure Medium

📌 Được phép deploy chỉ khi nằm trong ensemble, không standalone.

8. INTERACTION WITH OTHER MODELS

✔ Có thể dùng làm input cho ensemble aggregation

✔ Có thể hiển thị cho human appraiser

❌ Không được dùng trực tiếp để:

Approve khoản vay

Auto-pass workflow

Override hedonic / comparable outputs

9. FAILURE MODES & HANDLING
   Scenario Handling
   Missing cost table Fail-fast
   Depreciation mismatch Block output
   Version conflict Reject execution
   Incomplete dossier Abort

📌 Không có silent fallback. Không có best guess.

10. CHANGE MANAGEMENT

Mọi thay đổi đối với module này bắt buộc:

Bump version rõ ràng

Cập nhật registry

Có rationale văn bản

Đánh giá lại model risk

📌 Silent change = governance breach

11. FINAL GOVERNANCE STATEMENT

Module Cost Approach:

Hỗ trợ, không thay thế thẩm định viên

Minh bạch, không tối ưu hóa

Bảo thủ, không suy đoán

Được thiết kế để chịu được kiểm toán & tranh tụng

AI hỗ trợ định giá.
Con người chịu trách nhiệm cuối cùng.

🛑 END OF DOCUMENT – GOVERNANCE LOCKED
