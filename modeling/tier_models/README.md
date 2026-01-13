# Tier Models – Governance & Legal Specification

## 1. PURPOSE (NON-NEGOTIABLE)

`tier_models` tồn tại để **HỖ TRỢ WORKFLOW**, không phải để:

- định giá
- đánh giá rủi ro
- ra quyết định
- thay thế con người

👉 Tier Models chỉ trả lời **một câu hỏi duy nhất**:

> “Hồ sơ này cần mức độ review / escalation như thế nào?”

---

## 2. POSITIONING IN MASTER ARCHITECTURE

Tier Models nằm **SAU**:

- valuation_dossier.json (SSOT)
- confidence / risk band đã được đánh giá

Tier Models nằm **TRƯỚC**:

- escalation_policy
- maker–checker enforcement
- human review

📌 Tier Models **KHÔNG** nằm trong:

- AVM core
- pricing
- approval logic

---

## 3. WHAT TIER MODELS ARE

Tier Models là:

- Deterministic
- Static-coefficient
- Read-only
- Descriptive only
- Workflow-support signals

### Tier Levels

| Tier | Ý nghĩa                                   |
| ---- | ----------------------------------------- |
| LOW  | Hồ sơ đơn giản, review tối thiểu          |
| MID  | Hồ sơ trung bình, cần review kỹ hơn       |
| HIGH | Hồ sơ phức tạp / nhạy cảm, cần escalation |

📌 Tier ≠ Risk  
📌 Tier ≠ Approval  
📌 Tier ≠ Valuation Quality

---

## 4. WHAT TIER MODELS ARE NOT (ABSOLUTE BAN)

Tier Models **KHÔNG ĐƯỢC**:

- ❌ Sinh giá / điều chỉnh giá
- ❌ Sinh confidence score
- ❌ Đề xuất approve / reject
- ❌ Kích hoạt workflow
- ❌ Override rule engine
- ❌ Override con người
- ❌ Học từ outcome
- ❌ Adaptive / optimize

👉 Nếu vi phạm → **SYSTEM VIOLATION (NHÓM A)**

---

## 5. MODULE OVERVIEW

### 5.1 tier_classifier.py

- Chọn tier (LOW / MID / HIGH)
- Dựa trên rule + band có sẵn
- **Routing only**
- Không số hóa quyết định

### 5.2 tier_regression_low.py

- Sinh `review_intensity_score`
- Chỉ báo mức độ effort review thấp
- Không mang ý nghĩa “an toàn”

### 5.3 tier_regression_mid.py

- Sinh `review_intensity_score`
- Chỉ báo mức độ review trung bình
- Không phải risk score

### 5.4 tier_regression_high.py

- Sinh `escalation_intensity_score`
- Chuẩn bị escalation / senior review
- Không phải reject signal

### 5.5 output_schema.json

- Contract pháp lý cho output
- Ngăn decision leakage
- Bắt buộc validate

### 5.6 tier_selection_log.json

- Audit evidence
- Append-only
- Không chứa logic

---

## 6. OUTPUT GOVERNANCE

Mọi output từ tier_models:

- Phải tuân thủ `output_schema.json`
- Phải bounded [0.0 – 1.0]
- Phải hash input
- Phải versioned
- Phải reproducible

📌 Output chỉ mang ý nghĩa **DESCRIPTIVE**

---

## 7. LEGAL & AUDIT POSITIONING

Tier Models được thiết kế để:

- Đọc được bởi Auditor
- Giải thích được trước Tòa
- Phù hợp MRM / Model Risk Management
- Không bị coi là:
  - automated decision system
  - AI valuer
  - credit decision engine

> **Tier Models support humans. Humans remain accountable.**

---

## 8. CHANGE MANAGEMENT

Mọi thay đổi:

- Bắt buộc bump version
- Có rationale
- Có risk assessment
- Có approval

❌ Silent change = SYSTEM VIOLATION

---

## 9. FINAL DISCLAIMER

Tier Models:

- Không đưa ra ý kiến chuyên môn
- Không thay thế thẩm định viên
- Không đại diện cho quyết định ngân hàng

Chúng chỉ là **workflow-support indicators**.

---

🛑 END OF TIER MODELS GOVERNANCE  
🛑 DO NOT MODIFY WITHOUT FORMAL APPROVAL
