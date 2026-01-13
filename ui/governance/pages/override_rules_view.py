"""
override_rules_view.py

ROLE
----
Governance Override Rules Disclosure Page.

LEGAL POSITIONING
-----------------
- Publicly discloses override eligibility & prohibitions
- Reinforces human accountability
- Prevents AI or UI from being perceived as override authority

COMPLIANCE
----------
✔ MASTER_SPEC.md
✔ IMPLEMENTATION STATUS PHẦN 1
✔ IMPLEMENTATION STATUS PHẦN 2
✔ Override is human action, not AI decision
"""

import streamlit as st

from ui.shared.auth.role_guard import require_role
from ui.shared.state.role_state import Role
from ui.shared.utils.safe_render import safe_render

from ui.governance.components.policy_reference_box import policy_reference_box


# =========================
# PAGE RENDER
# =========================

def override_rules_view():
    """
    Render Override Rules Governance Page.

    GOVERNANCE GUARANTEES
    ---------------------
    - Read-only disclosure
    - No workflow interaction
    - No override execution
    """

    # ---- ROLE GATE ----
    require_role(
        allowed_roles=[
            Role.MANAGER,
            Role.AUDITOR,
        ]
    )

    st.title("✍️ Override Rules & Human Accountability")

    safe_render(
        """
        <div style="border-left: 4px solid #fd7e14; padding-left: 14px;">
            <strong>Governance Disclosure:</strong><br/>
            Overrides are <em>exceptional human actions</em> that modify or bypass
            system outputs.
            <br/><br/>
            This page discloses the <strong>rules and boundaries</strong> governing
            such actions. It does not enable or validate overrides.
        </div>
        """
    )

    st.markdown("---")

    # =========================
    # SECTION 1 — WHAT IS OVERRIDE
    # =========================
    st.header("1️⃣ Definition of Override")

    st.markdown(
        """
        An **override** is a deliberate action taken by an authorized human role to
        deviate from system-generated indicative outputs or workflow suggestions.
        """
    )

    st.markdown(
        """
        Overrides exist to:
        - Address exceptional or unmodeled situations
        - Apply professional judgment
        - Comply with regulatory or legal constraints
        """
    )

    st.markdown("---")

    # =========================
    # SECTION 2 — WHO MAY OVERRIDE
    # =========================
    st.header("2️⃣ Authorized Roles")

    st.markdown(
        """
        Only the following roles may initiate an override, subject to internal policy:
        """
    )

    st.markdown(
        """
        - **Manager / Credit Officer**
        - **Authorized Senior Appraiser**
        """
    )

    st.caption(
        "Authorization is determined by backend policy and access control, "
        "not by UI rendering."
    )

    st.markdown("---")

    # =========================
    # SECTION 3 — MANDATORY REQUIREMENTS
    # =========================
    st.header("3️⃣ Mandatory Override Requirements")

    st.markdown(
        """
        Every override must:
        """
    )

    st.markdown(
        """
        - Be explicitly initiated by a human
        - Include a documented reason code
        - Identify the acting individual
        - Be timestamped and logged
        - Remain fully auditable
        """
    )

    st.markdown("---")

    # =========================
    # SECTION 4 — EXPLICIT PROHIBITIONS
    # =========================
    st.header("4️⃣ Explicitly Prohibited Override Scenarios")

    st.markdown(
        """
        Overrides are **not permitted** in the following cases:
        """
    )

    st.markdown(
        """
        - Automatic or AI-initiated overrides
        - Overrides without documented rationale
        - Silent or unlogged overrides
        - Overrides that retrain or modify models
        - Overrides that bypass audit logging
        """
    )

    st.markdown("---")

    # =========================
    # SECTION 5 — POLICY BASIS
    # =========================
    st.header("5️⃣ Policy & Regulatory Basis")

    policy_reference_box()

    st.markdown("---")

    st.caption(
        "Override rules are disclosed for governance transparency. "
        "Final enforcement and compliance assessment remain the responsibility "
        "of authorized human roles under applicable internal policies."
    )
