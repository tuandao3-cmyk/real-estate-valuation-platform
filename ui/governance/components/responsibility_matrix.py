"""
responsibility_matrix.py

ROLE
----
Governance Responsibility Matrix (UI component).

LEGAL POSITIONING
-----------------
- Clarifies accountability boundaries
- Static, declarative
- Read-only
- No inference
- No enforcement

COMPLIANCE
----------
✔ MASTER_SPEC.md
✔ IMPLEMENTATION STATUS PHẦN 1 & 2
✔ AI ≠ Decision maker
✔ Human accountability preserved
"""

import streamlit as st
from typing import List, Dict

from ui.shared.utils.safe_render import safe_render
from ui.shared.components.table import render_table


# =========================
# RESPONSIBILITY MATRIX DATA
# =========================

def _responsibility_rows() -> List[Dict]:
    """
    Static responsibility matrix.

    GOVERNANCE
    ----------
    - Declarative
    - Non-executable
    - Audit-readable
    """

    return [
        {
            "Function": "Raw Data Collection",
            "AI / Model": "❌",
            "Rule Engine": "❌",
            "Human (Analyst)": "✅",
            "Human (Manager)": "❌",
            "Notes": "Source verification & intake"
        },
        {
            "Function": "Feature Engineering",
            "AI / Model": "✅",
            "Rule Engine": "❌",
            "Human (Analyst)": "❌",
            "Human (Manager)": "❌",
            "Notes": "Deterministic transformation only"
        },
        {
            "Function": "Price Estimation",
            "AI / Model": "✅",
            "Rule Engine": "❌",
            "Human (Analyst)": "❌",
            "Human (Manager)": "❌",
            "Notes": "Multiple AVM outputs, no final value"
        },
        {
            "Function": "Risk Band Adjustment",
            "AI / Model": "❌",
            "Rule Engine": "✅",
            "Human (Analyst)": "❌",
            "Human (Manager)": "❌",
            "Notes": "Policy-driven, non-learning"
        },
        {
            "Function": "Approval Decision",
            "AI / Model": "❌",
            "Rule Engine": "❌",
            "Human (Analyst)": "❌",
            "Human (Manager)": "✅",
            "Notes": "Explicit human declaration required"
        },
        {
            "Function": "Override Execution",
            "AI / Model": "❌",
            "Rule Engine": "❌",
            "Human (Analyst)": "❌",
            "Human (Manager)": "✅",
            "Notes": "Logged, reason-coded, auditable"
        },
        {
            "Function": "Audit & Accountability",
            "AI / Model": "❌",
            "Rule Engine": "❌",
            "Human (Analyst)": "❌",
            "Human (Manager)": "✅",
            "Notes": "Ex-post review & governance"
        },
    ]


# =========================
# COMPONENT RENDER
# =========================

def responsibility_matrix():
    """
    Render responsibility matrix component.

    GOVERNANCE
    ----------
    - Informational only
    - No dynamic behavior
    - No state mutation
    """

    st.subheader("📐 Responsibility & Accountability Matrix")

    safe_render(
        """
        <div style="border-left: 4px solid #6f42c1; padding-left: 12px;">
            <strong>Governance Notice:</strong><br/>
            This matrix explicitly defines <em>who is responsible for what</em>
            within the valuation system.
            <br/><br/>
            No AI component, model, or rule engine
            is authorized to assume human responsibility.
        </div>
        """
    )

    st.markdown("---")

    render_table(
        data=_responsibility_rows(),
        key="responsibility_matrix_table",
        selectable=False
    )

    st.caption(
        "Legend: ✅ Responsible / ❌ Not Responsible. "
        "This matrix is declarative and forms part of governance documentation."
    )
