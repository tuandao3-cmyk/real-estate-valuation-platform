# Explainability Module – Governance Specification

## 1. PURPOSE (LEGAL & OPERATIONAL)

Thư mục `model/explainability/` định nghĩa **toàn bộ lớp giải thích (explainability layer)** cho hệ thống:

> 🏗️ **ADVANCED AI-ASSISTED REAL ESTATE VALUATION PLATFORM (HYBRID AVM)**

Mục tiêu:

- Giải thích **model output** cho con người (appraiser / credit officer / auditor)
- Hỗ trợ **audit, kiểm toán, tranh tụng**
- Tăng minh bạch **mà KHÔNG can thiệp quyết định**

📌 Explainability **KHÔNG** được phép trở thành:

- Logic định giá
- Justification cho giá cuối
- Công cụ override rule hoặc human

---

## 2. CORE PRINCIPLES (NON-NEGOTIABLE)

### 2.1 EXPLAINABILITY ≠ DECISION

- Không file nào trong module này:
  - ❌ Sinh giá
  - ❌ Điều chỉnh giá
  - ❌ Gợi ý approve / reject
  - ❌ Gán confidence authority

Explainability chỉ:

- Mô tả
- Phân rã
- Giải thích **sau khi model đã chạy xong**

---

### 2.2 DESCRIPTIVE – NOT PRESCRIPTIVE

Mọi output phải:

- Trung lập
- Mô tả
- Không ngôn ngữ đánh giá (good / bad / reasonable / acceptable)

📌 Nếu explainability làm người đọc “tin rằng giá này đúng”  
→ **SYSTEM VIOLATION**

---

### 2.3 HUMAN JUDGMENT REMAINS PRIMARY

Explainability:

- Hỗ trợ hiểu
- Không thay thế thẩm định viên
- Không đóng vai “lý do pháp lý” cho quyết định tín dụng

📌 Trách nhiệm cuối luôn thuộc về **con người**.

---

## 3. MODULE SCOPE

### 3.1 FILES & ROLES

| File                         | Role                           | Key Constraints                     |
| ---------------------------- | ------------------------------ | ----------------------------------- |
| `feature_contribution.py`    | Trình bày mức đóng góp feature | Không causal, không weight decision |
| `price_breakdown.py`         | Phân rã signal giá             | Indicative only                     |
| `model_reasoning.py`         | Diễn giải logic model          | Không biện minh                     |
| `explainability_schema.json` | Schema kiểm soát output        | No decision leakage                 |
| `README.md`                  | Governance & legal spec        | Audit-first                         |

---

## 4. STRICT PROHIBITIONS

### ❌ FORBIDDEN ACTIONS

Explainability module **TUYỆT ĐỐI KHÔNG ĐƯỢC**:

- Dùng kết quả explainability để:
  - Điều chỉnh ensemble
  - Điều chỉnh confidence
  - Ảnh hưởng rule engine
- Gán:
  - “Hợp lý”
  - “Nên chấp nhận”
  - “Giá phù hợp thị trường”
- Chứa field:
  - `approval_hint`
  - `decision_score`
  - `recommended_price`

📌 Bất kỳ attempt nào như trên → **INVALID VALUATION**

---

## 5. DATA & GOVERNANCE GUARANTEES

### 5.1 READ-ONLY CONTRACT

- Explainability chỉ đọc:

  - model output
  - feature snapshot
  - metadata

- Không ghi ngược
- Không mutate data

---

### 5.2 REPRODUCIBILITY

- Explainability output:
  - Hashable
  - Versioned
  - Re-generatable từ cùng input

📌 Không reproducible → không dùng cho audit.

---

### 5.3 SCHEMA LOCK

- Mọi output phải tuân theo:
  - `explainability_schema.json`
- Schema drift:
  - Phải bump version
  - Phải có rationale
  - Phải có risk note

📌 Silent schema change = SYSTEM VIOLATION

---

## 6. AUDIT & COURT DEFENSE POSITIONING

Explainability layer được thiết kế để:

- Auditor:
  - Hiểu model làm gì
  - Không hiểu nhầm là “AI quyết định”
- Luật sư / tòa án:
  - Thấy rõ vai trò hỗ trợ
  - Không thể quy trách nhiệm pháp lý cho AI

📌 Đây là **legal shield**, không phải ML optimization layer.

---

## 7. WHAT THIS MODULE IS NOT

- ❌ Không phải SHAP playground
- ❌ Không phải justification engine
- ❌ Không phải AI explanation cho end-user retail
- ❌ Không dùng để marketing độ chính xác

---

## 8. FINAL STATEMENT

Explainability trong hệ thống này tồn tại để:

> **Giúp con người hiểu – không giúp máy quyết định.**

AI có thể giải thích.  
Con người chịu trách nhiệm.

---

🛑 END OF EXPLAINABILITY GOVERNANCE – DO NOT MODIFY WITHOUT APPROVAL
