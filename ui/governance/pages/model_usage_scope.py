"""
model_usage_scope.py

ROLE
----
Governance Model Usage Scope Disclosure Page.

LEGAL POSITIONING
-----------------
- Explicitly discloses where models MAY and MAY NOT be used
- Prevents scope creep and misuse
- Supports audit, regulatory review, and court defense

COMPLIANCE
----------
✔ MASTER_SPEC.md
✔ IMPLEMENTATION STATUS PHẦN 1
✔ IMPLEMENTATION STATUS PHẦN 2
✔ AI assists – Human decides
"""

import streamlit as st

from ui.shared.auth.role_guard import require_role
from ui.shared.state.role_state import Role
from ui.shared.utils.safe_render import safe_render

from ui.governance.components.model_capability_table import model_capability_table
from ui.governance.components.policy_reference_box import policy_reference_box


# =========================
# PAGE RENDER
# =========================

def model_usage_scope():
    """
    Render Model Usage Scope Governance Page.

    GOVERNANCE GUARANTEES
    ---------------------
    - Read-only
    - Declarative disclosure only
    - No workflow or execution coupling
    """

    # ---- ROLE GATE ----
    require_role(
        allowed_roles=[
            Role.MANAGER,
            Role.AUDITOR,
        ]
    )

    st.title("📐 Model Usage Scope Disclosure")

    safe_render(
        """
        <div style="border-left: 4px solid #6f42c1; padding-left: 14px;">
            <strong>Governance Disclosure:</strong><br/>
            This page defines the <em>intended usage scope</em> and
            <em>explicit prohibitions</em> for valuation-related models.
            <br/><br/>
            Usage scope disclosure does <strong>not</strong> grant permission,
            activate models, or authorize decisions.
        </div>
        """
    )

    st.markdown("---")

    # =========================
    # SECTION 1 — INTENDED USE
    # =========================
    st.header("1️⃣ Intended Usage Scope")

    st.markdown(
        """
        Models in this system are designed to be used **only** within the following scope:
        """
    )

    st.markdown(
        """
        - Assist licensed appraisers and credit officers
        - Provide **indicative, non-decisive signals**
        - Improve consistency and transparency
        - Support auditability and documentation
        """
    )

    st.markdown("---")

    # =========================
    # SECTION 2 — EXPLICITLY FORBIDDEN USE
    # =========================
    st.header("2️⃣ Explicitly Forbidden Uses")

    st.markdown(
        """
        The following uses are **explicitly prohibited**:
        """
    )

    st.markdown(
        """
        - Autonomous valuation or price finalization
        - Credit approval or rejection decisions
        - Customer-facing price quotation
        - Speculative trading or investment advice
        - Legal certification or statutory valuation replacement
        """
    )

    st.markdown("---")

    # =========================
    # SECTION 3 — MODEL-LEVEL BOUNDARIES
    # =========================
    st.header("3️⃣ Model-Level Usage Boundaries")

    st.markdown(
        """
        The table below summarizes **what each model type may and may not be used for**.
        """
    )

    model_capability_table()

    st.markdown("---")

    # =========================
    # SECTION 4 — POLICY BASIS
    # =========================
    st.header("4️⃣ Policy & Regulatory Basis")

    policy_reference_box()

    st.markdown("---")

    st.caption(
        "This usage scope disclosure is provided for governance transparency only. "
        "Final determination of appropriate model use remains the responsibility "
        "of authorized human roles under applicable policies and regulations."
    )
