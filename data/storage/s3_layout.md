# S3 LAYOUT

_Document initialized automatically._
S3 STORAGE LAYOUT – GOVERNANCE LOCKED

(Audit-Grade · Immutable · Court-Defensible)

Spec Authority: MASTER_SPEC.md
Risk Classification: NHÓM A – Legal / Audit / Evidence Integrity
Change Policy: GOVERNANCE-LOCKED (Versioned Only)

1. PURPOSE (LEGAL & TECH)

Tài liệu này định nghĩa cấu trúc lưu trữ S3 DUY NHẤT & BẮT BUỘC
cho toàn bộ hệ thống Advanced AVM nhằm đảm bảo:

Tính bất biến (immutability)

Truy vết pháp lý (audit & litigation)

Reproducibility tuyệt đối

Không ghi đè – không mập mờ – không “latest magic”

📌 Bất kỳ artifact nào không tuân theo layout này = NON-COMPLIANT.

2. CORE STORAGE PRINCIPLES (NON-NEGOTIABLE)

❌ Không overwrite object

❌ Không update in-place

❌ Không “latest” pointer ngầm

❌ Không ghi dữ liệu chưa finalized

✅ Mọi object được tham chiếu bằng content-hash

✅ Mọi path đều deterministic

✅ Phù hợp legal hold & forensic replay

3. HIGH-LEVEL BUCKET STRATEGY
   s3://avm-platform/
   ├── raw/
   ├── cleaned/
   ├── features/
   ├── model_outputs/
   ├── valuation/
   ├── audit/
   ├── snapshots/
   └── governance/

📌 Không bucket nào được phép chứa mixed purpose.

4. DETAILED DIRECTORY LAYOUT
   4.1 Raw Data (Immutable Input Evidence)
   raw/
   ├── source_system/
   │ ├── source_name/
   │ │ └── ingestion_date=YYYY-MM-DD/
   │ │ └── content_hash.json

Rules

Chỉ append

Không chỉnh sửa

Là bằng chứng “hệ thống đã nhận gì”

4.2 Cleaned Data (Signal-Only Derivatives)
cleaned/
├── normalize_address/
├── geocode/
├── deduplicate/
├── outlier_detection/
├── completeness_check/
│ └── run_date=YYYY-MM-DD/
│ └── content_hash.json

Rules

Cleaned ≠ corrected

Chỉ signal

Không thay đổi raw

4.3 Feature Artifacts (Read-Only Inputs for Models)
features/
├── feature_set_name/
│ └── version=vX.Y/
│ └── content_hash.json

Rules

Feature version bất biến

Không regenerate ngầm

4.4 Model Outputs (Strictly Read-Only)
model_outputs/
├── model_name/
│ └── version=vX.Y/
│ └── valuation_hash/
│ └── content_hash.json

Rules

Model output ≠ decision

Không overwrite kết quả

4.5 Valuation Core Artifacts (Legal Canonical)
valuation/
├── dossier/
│ └── valuation_hash.json
├── decision_result/
│ └── valuation_hash.json
├── approval_log/
│ └── valuation_hash.json

📌 valuation_dossier.json là Single Source of Truth

4.6 Audit & Trace (Legal Evidence)
audit/
├── valuation_trace/
│ └── trace_id.json
├── reproducibility_hash/
│ └── valuation_hash.json

Rules

Audit artifact không được dùng để quyết định

Chỉ để chứng minh & truy vết

4.7 Snapshots (Frozen Legal Evidence)
snapshots/
├── valuation/
│ └── snapshot_id/
│ ├── valuation_dossier.json
│ ├── valuation_trace.json
│ ├── decision_result.json
│ └── approval_log.json

📌 Snapshot = “tại thời điểm đó hệ thống đã thấy gì”

4.8 Governance & Policy
governance/
├── MASTER_SPEC.md
├── IMPLEMENTATION_STATUS.md
├── policies/
│ ├── confidence_threshold.yaml
│ ├── risk_band_rules.yaml
│ └── rejection_conditions.yaml

5. NAMING & HASHING RULES

content_hash = SHA-256

Hash dựa trên:

Canonical JSON

Sorted keys

UTF-8

Path ≠ hash

Hash là định danh pháp lý, không phải filename

6. ACCESS CONTROL (MANDATORY)
   Layer Write Read
   raw Ingestion service Read-only
   cleaned Cleaning pipeline Read-only
   valuation Valuation engine Read-only
   audit Orchestrator Read-only
   snapshots Snapshot store Legal / Audit

📌 Không có human manual write vào S3.

7. ILLEGAL OPERATIONS (ABSOLUTE BAN)

❌ Update object

❌ Delete object (trừ retention policy được phê duyệt)

❌ Rename path

❌ Copy không gắn trace

❌ Ghi dữ liệu tạm / draft

8. AUDIT & COURT DEFENSIBILITY

Cấu trúc này đảm bảo:

Replay valuation bất kỳ

Trả lời được:

Ai tạo?

Khi nào?

Dựa trên dữ liệu gì?

Đáp ứng:

Ngân hàng

Big4

Tòa án

9. FINAL GOVERNANCE STATEMENT

S3 Layout này:

Không tối ưu chi phí

Không tối ưu tiện lợi

Ưu tiên tuyệt đối cho pháp lý & kiểm toán

Storage is Evidence, not Convenience.
