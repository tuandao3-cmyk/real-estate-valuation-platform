Ensemble Model Governance Specification

Module Path: model/ensemble/
Status: ✅ IMPLEMENTED – GOVERNANCE LOCKED
Risk Level: 🟡 NHÓM A/B – Aggregation Layer (Non-Decisive)

1. PURPOSE (LEGAL & TECH)

Ensemble layer tồn tại để:

Tổng hợp nhiều output mô hình độc lập

Tăng tính defensible của valuation

Hiển thị độ phân tán & bất định

Ngăn single-model dominance

📌 Ensemble ≠ Valuation decision ≠ Approval logic

2. CORE GOVERNANCE PRINCIPLES (NON-NEGOTIABLE)
   2.1 Ensemble Is Not a Valuer

❌ Không quyết định giá cuối

❌ Không phán quyết đúng/sai

❌ Không override rule / human

✔ Chỉ được:

Aggregate

Suppress outlier theo rule

Trình bày dispersion

2.2 Deterministic & Reproducible

Không học

Không adaptive

Không optimization theo outcome

Cùng input → cùng output

📌 Bắt buộc hashable & replayable.

2.3 Read-Only Authority

Ensemble:

Đọc valuation_dossier.json (SSOT)

Đọc output model (read-only)

Ghi output indicative only

📌 Không ghi ngược lại bất kỳ artifact nào.

3. MODULE STRUCTURE & ROLES
   File Role Authority
   outlier_suppressor.py Loại bỏ extreme value theo rule tĩnh ❌ No decision
   weight_optimizer.py Gán trọng số minh bạch, không adaptive ❌ No learning
   price_aggregator.py Tính giá aggregate + range ❌ No approval
   confidence_estimator.py Confidence mô tả (agreement + data) ❌ No threshold
   ensemble_trace.json Audit trace Read-only
   output_schema.json Output contract Enforcement only
   README.md Governance & legal context Audit-first
4. OUTPUT CHARACTERISTICS

Ensemble output:

Có thể chứa:

indicative_price

price_range

confidence_score (descriptive)

Không bao giờ chứa:

approval hint

risk decision

threshold crossing

recommendation language

📌 Output chỉ hợp lệ khi tham chiếu valuation_hash.

5. CONFIDENCE DISCLAIMER (CRITICAL)

confidence_score tại ensemble layer:

Đo mức độ đồng thuận + chất lượng dữ liệu

❌ Không đo accuracy

❌ Không dùng để auto-approve

❌ Không dùng để reject

📌 Confidence là workflow gate input, không phải quyết định.

6. OUTLIER & WEIGHTING GOVERNANCE
   Outlier Suppression

Rule-based

Bound trước

Không statistical learning

Không dynamic threshold

Weighting

Minh bạch

Version-locked

Không optimize theo historical error

📌 Weight ≠ trust ≠ importance pháp lý.

7. AUDIT & TRACEABILITY

Mỗi lần chạy ensemble phải có:

ensemble_trace.json

valuation_hash

model_id + version

weight used

outlier decisions (descriptive)

timestamp UTC

📌 Không trace = output không hợp lệ.

8. STRICT PROHIBITIONS

❌ Ensemble KHÔNG ĐƯỢC:

Thay đổi output model gốc

Ẩn dispersion

Làm tròn để “đẹp số”

Tối ưu để match market

Suy luận hành vi con người

Tham gia approval flow

9. FAILURE HANDLING

Thiếu model → degrade có log

Conflict version → fail-fast

Schema mismatch → hard error

📌 Silent failure = SYSTEM VIOLATION.

10. LEGAL STATEMENT (FOR AUDITOR / COURT)

Ensemble layer trong hệ thống này:

Không thay thế thẩm định viên

Không tự đưa ra quyết định

Chỉ hỗ trợ minh bạch & nhất quán

Trách nhiệm cuối cùng thuộc về con người có thẩm quyền.

11. CHANGE MANAGEMENT

Mọi thay đổi:

Bắt buộc bump version

Có rationale

Có risk assessment

📌 Silent change = governance breach.
