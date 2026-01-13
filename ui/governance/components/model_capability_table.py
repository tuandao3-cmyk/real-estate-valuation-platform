"""
model_capability_table.py

ROLE
----
Governance Model Capability Disclosure Table (UI Component).

LEGAL POSITIONING
-----------------
- Declarative capability disclosure
- Explicit limitation statement
- Prevents AI over-claim & authority creep
- Read-only, non-inferential

COMPLIANCE
----------
✔ MASTER_SPEC.md
✔ IMPLEMENTATION STATUS PHẦN 1
✔ IMPLEMENTATION STATUS PHẦN 2
✔ AI ≠ Decision maker
✔ Capability ≠ Authorization
"""

import streamlit as st
from typing import List, Dict

from ui.shared.utils.safe_render import safe_render
from ui.shared.components.table import render_table


# =========================
# STATIC CAPABILITY MATRIX
# =========================

def _capability_rows() -> List[Dict]:
    """
    Static, governance-approved model capability table.

    GOVERNANCE GUARANTEES
    ---------------------
    - Hardcoded
    - Human-curated
    - No runtime mutation
    - Audit-readable
    """

    return [
        {
            "Model / Component": "Similarity Model",
            "Can Estimate Price": "❌",
            "Can Compare Assets": "✅",
            "Can Decide / Approve": "❌",
            "Can Override Rules": "❌",
            "Notes": "Comparable analysis only"
        },
        {
            "Model / Component": "Hedonic Model",
            "Can Estimate Price": "⚠️ Indicative",
            "Can Compare Assets": "❌",
            "Can Decide / Approve": "❌",
            "Can Override Rules": "❌",
            "Notes": "Projection, not valuation"
        },
        {
            "Model / Component": "Cost Approach Model",
            "Can Estimate Price": "⚠️ Indicative",
            "Can Compare Assets": "❌",
            "Can Decide / Approve": "❌",
            "Can Override Rules": "❌",
            "Notes": "Replacement cost reference"
        },
        {
            "Model / Component": "Income Approach Model",
            "Can Estimate Price": "⚠️ Indicative",
            "Can Compare Assets": "❌",
            "Can Decide / Approve": "❌",
            "Can Override Rules": "❌",
            "Notes": "NOI-based signal only"
        },
        {
            "Model / Component": "Tier Classifier",
            "Can Estimate Price": "❌",
            "Can Compare Assets": "❌",
            "Can Decide / Approve": "❌",
            "Can Override Rules": "❌",
            "Notes": "Routing classification only"
        },
        {
            "Model / Component": "Ensemble Aggregator",
            "Can Estimate Price": "⚠️ Indicative",
            "Can Compare Assets": "❌",
            "Can Decide / Approve": "❌",
            "Can Override Rules": "❌",
            "Notes": "Weighted aggregation, no authority"
        },
        {
            "Model / Component": "Confidence Estimator",
            "Can Estimate Price": "❌",
            "Can Compare Assets": "❌",
            "Can Decide / Approve": "❌",
            "Can Override Rules": "❌",
            "Notes": "Descriptive uncertainty signal"
        },
    ]


# =========================
# COMPONENT RENDER
# =========================

def model_capability_table():
    """
    Render model capability disclosure table.

    GOVERNANCE
    ----------
    - Informational only
    - Zero side effects
    - No execution logic
    """

    st.subheader("🧩 Model Capability Disclosure")

    safe_render(
        """
        <div style="border-left: 4px solid #0d6efd; padding-left: 12px;">
            <strong>Governance Disclosure:</strong><br/>
            This table explicitly discloses the <em>capabilities and limitations</em>
            of each model component.
            <br/><br/>
            Listed capabilities do <strong>not</strong> imply authorization,
            approval power, or decision authority.
        </div>
        """
    )

    st.markdown("---")

    render_table(
        data=_capability_rows(),
        key="model_capability_table",
        selectable=False
    )

    st.caption(
        "Legend: ✅ Allowed capability · ⚠️ Indicative / Non-decisive · ❌ Explicitly forbidden. "
        "This disclosure is part of governance documentation."
    )
