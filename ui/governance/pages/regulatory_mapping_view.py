"""
regulatory_mapping_view.py

ROLE
----
Regulatory Mapping Disclosure Page.

LEGAL POSITIONING
-----------------
- Discloses how system components align with regulatory expectations
- Demonstrates governance-by-design
- Prevents misinterpretation of AI as autonomous decision-maker

COMPLIANCE
----------
✔ MASTER_SPEC.md
✔ IMPLEMENTATION STATUS PHẦN 1
✔ IMPLEMENTATION STATUS PHẦN 2
✔ Read-only governance artifact
"""

import streamlit as st

from ui.shared.auth.role_guard import require_role
from ui.shared.state.role_state import Role
from ui.shared.utils.safe_render import safe_render

from ui.governance.components.policy_reference_box import policy_reference_box


# =========================
# PAGE RENDER
# =========================

def regulatory_mapping_view():
    """
    Render Regulatory Mapping Governance Page.

    GOVERNANCE GUARANTEES
    ---------------------
    - Disclosure-only
    - No regulatory enforcement
    - No compliance verdict
    """

    # ---- ROLE GATE ----
    require_role(
        allowed_roles=[
            Role.MANAGER,
            Role.AUDITOR,
        ]
    )

    st.title("📚 Regulatory & Governance Mapping")

    safe_render(
        """
        <div style="border-left: 4px solid #0d6efd; padding-left: 14px;">
            <strong>Governance Disclosure:</strong><br/>
            This page documents how system components, human roles, and workflow
            controls align with regulatory and audit expectations.
            <br/><br/>
            It exists to demonstrate <em>intentional compliance by design</em>.
        </div>
        """
    )

    st.markdown("---")

    # =========================
    # SECTION 1 — PURPOSE
    # =========================
    st.header("1️⃣ Purpose of Regulatory Mapping")

    st.markdown(
        """
        Regulatory mapping provides transparency into:
        - Where decisions originate
        - Who holds authority
        - Which artifacts serve as legal evidence
        """
    )

    st.markdown(
        """
        This mapping is designed for:
        - Auditors
        - Regulators
        - Internal risk & compliance teams
        """
    )

    st.markdown("---")

    # =========================
    # SECTION 2 — DECISION AUTHORITY MAPPING
    # =========================
    st.header("2️⃣ Decision Authority Mapping")

    st.markdown(
        """
        | Layer | Authority | Regulatory Interpretation |
        |------|-----------|---------------------------|
        | AI Models | ❌ None | Analytical tools only |
        | Rule Policies | ❌ None | Deterministic routing |
        | Workflow Engine | ❌ None | Process coordination |
        | Human Roles | ✅ Full | Legal decision authority |
        """,
        unsafe_allow_html=False,
    )

    st.caption(
        "No automated component in the system has legal decision authority."
    )

    st.markdown("---")

    # =========================
    # SECTION 3 — EVIDENCE & AUDIT ARTIFACTS
    # =========================
    st.header("3️⃣ Audit & Evidence Artifacts")

    st.markdown(
        """
        | Artifact | Purpose | Regulatory Value |
        |---------|---------|------------------|
        | valuation_dossier.json | Canonical record | Legal source of truth |
        | approval_log.json | Human approval trace | Accountability evidence |
        | valuation_trace | Workflow replay | Reproducibility |
        | feature_snapshot | Input freeze | Anti-tampering |
        """
    )

    st.markdown("---")

    # =========================
    # SECTION 4 — MODEL GOVERNANCE ALIGNMENT
    # =========================
    st.header("4️⃣ Model Governance Alignment")

    st.markdown(
        """
        Model governance is enforced through:
        """
    )

    st.markdown(
        """
        - Explicit model registry & whitelist
        - Version locking & artifact hashing
        - Separation of projection vs decision
        - Human accountability preservation
        """
    )

    st.caption(
        "Model outputs are indicative signals, not regulatory decisions."
    )

    st.markdown("---")

    # =========================
    # SECTION 5 — OVERRIDE & ESCALATION
    # =========================
    st.header("5️⃣ Override & Escalation Controls")

    st.markdown(
        """
        Regulatory safeguards include:
        """
    )

    st.markdown(
        """
        - Overrides restricted to authorized human roles
        - Mandatory justification & logging
        - Escalation rules based on risk & confidence
        - Prohibition of silent or automated overrides
        """
    )

    st.markdown("---")

    # =========================
    # SECTION 6 — POLICY BASIS
    # =========================
    st.header("6️⃣ Policy & Regulatory Basis")

    policy_reference_box()

    st.markdown("---")

    st.caption(
        "This regulatory mapping is provided for transparency and governance "
        "disclosure purposes only. It does not constitute legal advice or "
        "regulatory certification."
    )
