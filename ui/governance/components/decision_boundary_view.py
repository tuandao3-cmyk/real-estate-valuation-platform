"""
decision_boundary_view.py

ROLE
----
Governance Decision Boundary Visualization Page.

LEGAL POSITIONING
-----------------
- Explicitly visualizes responsibility & authority boundaries
- Demonstrates separation between AI, Rules, and Humans
- Prevents implicit delegation of decision power to AI

COMPLIANCE
----------
✔ MASTER_SPEC.md
✔ IMPLEMENTATION STATUS PHẦN 1
✔ IMPLEMENTATION STATUS PHẦN 2
✔ Court-defensible governance UI
"""

import streamlit as st

from ui.shared.auth.role_guard import require_role
from ui.shared.state.role_state import Role
from ui.shared.utils.safe_render import safe_render

from ui.governance.components.responsibility_matrix import responsibility_matrix
from ui.governance.components.model_capability_table import model_capability_table
from ui.governance.components.policy_reference_box import policy_reference_box


# =========================
# PAGE RENDER
# =========================

def decision_boundary_view():
    """
    Render Decision Boundary Governance Page.

    GOVERNANCE GUARANTEES
    ---------------------
    - Read-only
    - No side effects
    - No workflow interaction
    """

    # ---- ROLE GATE ----
    require_role(
        allowed_roles=[
            Role.MANAGER,
            Role.AUDITOR,
        ]
    )

    st.title("🛑 Decision Boundary & Responsibility View")

    safe_render(
        """
        <div style="border-left: 4px solid #dc3545; padding-left: 14px;">
            <strong>Critical Governance Disclosure:</strong><br/>
            This page explicitly documents the <em>decision boundaries</em> within the
            valuation system.
            <br/><br/>
            No AI component, model, or rule engine shown here has authority to approve,
            reject, or finalize a valuation outcome.
        </div>
        """
    )

    st.markdown("---")

    # =========================
    # SECTION 1 — RESPONSIBILITY
    # =========================
    st.header("1️⃣ Responsibility Allocation")

    st.markdown(
        "This section clarifies **who is responsible for what** in the valuation workflow."
    )

    responsibility_matrix()

    st.markdown("---")

    # =========================
    # SECTION 2 — MODEL LIMITS
    # =========================
    st.header("2️⃣ Model Capability Boundaries")

    st.markdown(
        "This section discloses the **explicit capabilities and prohibitions** of each model."
    )

    model_capability_table()

    st.markdown("---")

    # =========================
    # SECTION 3 — POLICY BASIS
    # =========================
    st.header("3️⃣ Policy & Regulatory Basis")

    st.markdown(
        "This section lists the **policy and regulatory references** that define these boundaries."
    )

    policy_reference_box()

    st.markdown("---")

    st.caption(
        "This page is provided for governance transparency. "
        "It does not constitute approval authority, legal interpretation, "
        "or automated compliance determination."
    )
