"""
liability_notice.py

ROLE
----
Liability & Accountability Disclosure Page.

LEGAL POSITIONING
-----------------
- Explicitly disclaims AI decision authority
- Reaffirms human responsibility and accountability
- Prevents misinterpretation of system outputs as legal decisions

COMPLIANCE
----------
✔ MASTER_SPEC.md
✔ IMPLEMENTATION STATUS PHẦN 1
✔ IMPLEMENTATION STATUS PHẦN 2
✔ Court-defensible governance artifact
"""

import streamlit as st

from ui.shared.auth.role_guard import require_role
from ui.shared.state.role_state import Role
from ui.shared.utils.safe_render import safe_render


# =========================
# PAGE RENDER
# =========================

def liability_notice():
    """
    Render Liability & Accountability Notice Page.

    GOVERNANCE GUARANTEES
    ---------------------
    - Read-only legal disclosure
    - No workflow interaction
    - Explicit responsibility boundaries
    """

    # ---- ROLE GATE ----
    require_role(
        allowed_roles=[
            Role.MANAGER,
            Role.AUDITOR,
        ]
    )

    st.title("⚖️ Liability & Accountability Notice")

    safe_render(
        """
        <div style="border-left: 4px solid #dc3545; padding-left: 14px;">
            <strong>Important Legal Notice:</strong><br/>
            This system is an <em>assistive valuation platform</em>.
            It does not replace licensed professionals, legal judgment,
            or regulatory authority.
        </div>
        """
    )

    st.markdown("---")

    # =========================
    # SECTION 1 — SYSTEM LIMITATION
    # =========================
    st.header("1️⃣ System Role & Limitations")

    st.markdown(
        """
        The platform provides:
        """
    )

    st.markdown(
        """
        - Analytical signals
        - Standardized workflows
        - Risk indicators
        - Documentation support
        """
    )

    st.markdown(
        """
        The platform does **not**:
        """
    )

    st.markdown(
        """
        - Make legal, credit, or valuation decisions
        - Replace licensed appraisers
        - Approve or reject transactions
        - Assume professional responsibility
        """
    )

    st.markdown("---")

    # =========================
    # SECTION 2 — AI & MODEL DISCLAIMER
    # =========================
    st.header("2️⃣ AI & Model Disclaimer")

    st.markdown(
        """
        All AI, ML, and algorithmic components:
        """
    )

    st.markdown(
        """
        - Generate indicative outputs only
        - Operate under predefined constraints
        - Cannot override policies or humans
        - Have no legal standing or agency
        """
    )

    st.caption(
        "Model outputs are informational signals, not determinations."
    )

    st.markdown("---")

    # =========================
    # SECTION 3 — HUMAN ACCOUNTABILITY
    # =========================
    st.header("3️⃣ Human Responsibility & Accountability")

    st.markdown(
        """
        All final decisions are made by authorized human roles, including:
        """
    )

    st.markdown(
        """
        - Licensed appraisers
        - Credit officers
        - Authorized managers
        """
    )

    st.markdown(
        """
        These individuals:
        """
    )

    st.markdown(
        """
        - Review system outputs
        - Apply professional judgment
        - Accept or override recommendations
        - Bear full accountability for decisions
        """
    )

    st.markdown("---")

    # =========================
    # SECTION 4 — OVERRIDE LIABILITY
    # =========================
    st.header("4️⃣ Override Liability")

    st.markdown(
        """
        Overrides are:
        """
    )

    st.markdown(
        """
        - Explicit human actions
        - Logged and auditable
        - Performed under internal policy
        """
    )

    st.markdown(
        """
        Responsibility for an override lies entirely with:
        """
    )

    st.markdown(
        """
        - The individual performing the override
        - The organization authorizing that role
        """
    )

    st.caption(
        "The system does not assume liability for override outcomes."
    )

    st.markdown("---")

    # =========================
    # SECTION 5 — NO TRANSFER OF LIABILITY
    # =========================
    st.header("5️⃣ No Transfer of Liability")

    st.markdown(
        """
        Use of this system does not:
        """
    )

    st.markdown(
        """
        - Transfer legal liability to the platform
        - Diminish professional obligations
        - Substitute statutory or regulatory requirements
        """
    )

    st.markdown(
        """
        Users remain subject to:
        """
    )

    st.markdown(
        """
        - Applicable laws and regulations
        - Professional standards
        - Internal governance policies
        """
    )

    st.markdown("---")

    # =========================
    # SECTION 6 — FINAL NOTICE
    # =========================
    st.header("6️⃣ Final Notice")

    st.markdown(
        """
        This notice is provided to ensure transparency and correct
        interpretation of system capabilities and responsibilities.
        """
    )

    st.caption(
        "This page is a governance disclosure artifact and does not "
        "constitute legal advice."
    )
