# ============================================================

# FEATURE OWNER REGISTRY

# File: feature_pipeline/registry/feature_owner.md

#

# Purpose:

# Define clear ownership, accountability, and governance

# responsibility for every feature group in the system.

#

# Governance Level:

# NHÓM A – Audit / Accountability Critical

#

# MASTER_SPEC COMPLIANCE:

# - Every feature MUST have a human owner

# - AI / LLM can NEVER be an owner

# - Ownership ≠ authority to change valuation outcomes

# ============================================================

## 1. GOVERNANCE PRINCIPLES (NON-NEGOTIABLE)

- Every feature has exactly **one accountable owner**
- Owner is responsible for:
  - Feature definition clarity
  - Input/output correctness
  - Documented limitations
  - Audit explanations
- Owner is **NOT** allowed to:
  - Adjust price
  - Modify confidence score
  - Override rules
  - Approve valuation outcomes

📌 Ownership is **accountability**, not **decision power**.

---

## 2. ROLE DEFINITIONS

### Feature Owner

- Senior engineer / data scientist
- Accountable for feature correctness & documentation
- Point of contact for auditors

### Governance Committee

- Approves feature changes
- Reviews risk & compliance impact
- Enforces MASTER_SPEC.md

### Human Valuer / Credit Officer

- Uses outputs
- Makes final decisions
- Not responsible for feature internals

---

## 3. FEATURE OWNERSHIP REGISTRY

### 3.1 Data Cleaning & Quality Features

| Feature ID   | Feature Name               | Owner Role           | Team            |
| ------------ | -------------------------- | -------------------- | --------------- |
| FTR_ADDR_001 | address_normalization_hash | Lead Data Engineer   | Data Platform   |
| FTR_GEO_001  | geocode_confidence         | Senior Data Engineer | Data Platform   |
| FTR_DATA_001 | data_completeness_ratio    | Data Quality Lead    | Data Governance |

---

### 3.2 Trust & Integrity Features

| Feature ID    | Feature Name                 | Owner Role           | Team           |
| ------------- | ---------------------------- | -------------------- | -------------- |
| FTR_TRUST_001 | listing_trust_feature_vector | Senior ML Engineer   | Trust & Safety |
| FTR_IMG_001   | image_condition_score        | Computer Vision Lead | ML Engineering |

📌 These owners **do NOT** classify fraud  
📌 They only provide descriptive signals

---

### 3.3 Text & Semantic Features

| Feature ID   | Feature Name          | Owner Role | Team           |
| ------------ | --------------------- | ---------- | -------------- |
| FTR_TEXT_001 | text_embedding_vector | NLP Lead   | ML Engineering |

📌 Embeddings are **feature extractors**, not interpreters

---

### 3.4 Geo & Market Structure Features

| Feature ID  | Feature Name            | Owner Role         | Team                |
| ----------- | ----------------------- | ------------------ | ------------------- |
| FTR_GEO_002 | micro_market_cluster_id | Geo Analytics Lead | Market Intelligence |

📌 Cluster ID ≠ market price  
📌 Cluster ID ≠ investment advice

---

### 3.5 Monitoring & Drift Features

| Feature ID    | Feature Name       | Owner Role            | Team             |
| ------------- | ------------------ | --------------------- | ---------------- |
| FTR_DRIFT_001 | feature_drift_flag | Model Governance Lead | Model Risk (MRM) |

📌 Drift flag is **informational only**  
📌 No auto-retraining, no auto-blocking

---

## 4. CHANGE & ESCALATION PROCESS

Any change to a feature requires:

1. Owner proposal
2. Written rationale
3. Impact analysis (model + compliance)
4. Governance committee approval
5. Version bump in:
   - feature_catalog.yaml
   - feature_dependencies.yaml

🚫 Silent changes are **SYSTEM VIOLATION**

---

## 5. AUDIT & ACCOUNTABILITY STATEMENT

- Each feature is:
  - Traceable
  - Reproducible
  - Owned by a named role
- No feature exists without ownership
- No AI system is accountable for outcomes

> **AI assists. Humans are accountable.**

---

# END OF FEATURE OWNER REGISTRY

# MASTER_SPEC.md OVERRIDES ALL
