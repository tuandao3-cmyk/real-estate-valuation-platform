# OVERRIDE POLICY

_Document initialized automatically._

# OVERRIDE_POLICY.md

🚫 DO NOT VIOLATE – GOVERNANCE LOCKED  
Part of ADVANCED AI-ASSISTED REAL ESTATE VALUATION PLATFORM (HYBRID AVM)

---

## 0. PURPOSE (LEGAL & GOVERNANCE)

File này định nghĩa **CHÍNH SÁCH OVERRIDE DUY NHẤT** cho toàn bộ hệ thống định giá.

Mục tiêu:

- Cho phép **con người có thẩm quyền** can thiệp khi cần thiết
- Đảm bảo override **là hành vi có kiểm soát**, không phá vỡ governance
- Bảo vệ hệ thống trước:
  - Lạm dụng AI
  - Tự động hóa vượt thẩm quyền
  - Trôi kiến trúc (architectural drift)

📌 Override là **ngoại lệ được quản lý**, không phải lỗ hổng hệ thống.

---

## 1. CORE PRINCIPLES (NON-NEGOTIABLE)

### 1.1 SINGLE SOURCE OF TRUTH

- `valuation_dossier.json` là **nguồn sự thật duy nhất**
- Override **KHÔNG được**:
  - Sửa dossier
  - Ghi đè model output
  - Thay đổi confidence / risk / price

📌 Override chỉ **tham chiếu** dossier – không can thiệp nội dung.

---

### 1.2 HUMAN AUTHORITY ONLY

Override chỉ được thực hiện bởi:

- Licensed Appraiser
- Credit Officer
- Manager / Committee Member

🚫 **CẤM TUYỆT ĐỐI**:

- AI
- Rule engine
- System account
- Batch job
- LLM output

📌 Nếu override không có chữ ký con người hợp lệ ⇒ **NON-COMPLIANT**

---

### 1.3 OVERRIDE ≠ DECISION REWRITE

Override:

- Không viết lại kết luận định giá
- Không tạo giá mới
- Không “sửa cho hợp lý”
- Không làm đẹp hồ sơ

Override chỉ:

- Ghi nhận **quan điểm con người**
- Áp dụng **trách nhiệm cá nhân có audit**

---

## 2. WHAT CAN BE OVERRIDDEN

Override **CHỈ ĐƯỢC PHÉP** tác động tới:

- Workflow routing (cho phép tiếp tục / dừng)
- Escalation outcome (yêu cầu cấp cao hơn)
- Final acceptance **sau khi** tất cả gate hợp lệ

📌 Override **KHÔNG** can thiệp vào:

- Model outputs
- Ensemble result
- Confidence score
- Risk band
- Rule evaluation

---

## 3. WHAT CANNOT BE OVERRIDDEN (ABSOLUTE)

Không được override trong các trường hợp:

- ❌ Vi phạm integrity / hash của valuation_dossier
- ❌ Thiếu approval_log hợp lệ
- ❌ Vi phạm Maker–Checker
- ❌ Vi phạm separation-of-duties
- ❌ Bị BLOCK bởi `rejection_conditions.yaml`

📌 Hard Rejection = **NO OVERRIDE ALLOWED**

---

## 4. OVERRIDE PROCESS (MANDATORY FLOW)

Override **PHẢI** tuân theo trình tự:

1. Valuation hoàn tất toàn bộ workflow gate
2. Maker–Checker Enforcement đã đạt ENFORCED_OK
3. Override được thực hiện bởi người có thẩm quyền
4. Override được ghi vào `approval_log.json`
5. Override được trace & snapshot

📌 Không có bước nào được bỏ qua.

---

## 5. OVERRIDE LOGGING (LEGAL-GRADE)

Mọi override **BẮT BUỘC** phải được ghi nhận trong:

### approval_log.json

- actor_id
- role
- override_flag = true
- override_reason_code (canonical)
- timestamp (UTC)
- approval_hash

📌 Free-text chỉ được phép trong **commentary**, không phải logic.

---

## 6. OVERRIDE REASON CODES (CANONICAL)

Override reason **PHẢI** thuộc danh sách được governance phê duyệt:

- MARKET_ANOMALY_CONFIRMED
- LEGAL_CONTEXT_NOT_CAPTURABLE_BY_MODEL
- DATA_LATENCY_ACKNOWLEDGED
- COURT_PRECEDENT_APPLIED
- CREDIT_POLICY_EXCEPTION_APPROVED

📌 Không có reason code ⇒ override INVALID

---

## 7. AUDIT & TRACEABILITY

Override luôn:

- Gắn với `valuation_hash`
- Xuất hiện trong `valuation_trace`
- Được snapshot bởi `snapshot_store`

Audit có thể trả lời:

- Ai override?
- Khi nào?
- Vì sao?
- Override cái gì?
- Có vi phạm policy không?

📌 Override không trace được ⇒ **FAIL AUDIT**

---

## 8. RELATIONSHIP WITH OTHER ARTIFACTS

- **Source of Truth**: valuation_dossier.json
- **Logged in**: approval_log.json
- **Traced by**: valuation_trace.py
- **Preserved by**: snapshot_store.py
- **Never modifies**:
  - decision_result.json
  - model outputs
  - risk / confidence artifacts

---

## 9. GOVERNANCE ENFORCEMENT

- Override policy được:

  - Versioned
  - Legal reviewed
  - Audit approved

- Mọi thay đổi yêu cầu:
  - Written rationale
  - Risk assessment
  - Version bump

📌 Silent change = GOVERNANCE VIOLATION

---

## 10. FINAL STATEMENT

Override tồn tại để:

> **Bảo vệ con người trước AI, không phải bảo vệ AI trước con người.**

AI hỗ trợ.  
Rule kiểm soát.  
Con người chịu trách nhiệm.

---

🛑 END OF OVERRIDE_POLICY.md  
🛑 DO NOT MODIFY WITHOUT GOVERNANCE APPROVAL
