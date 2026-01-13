"""
policy_reference_box.py

ROLE
----
Governance Policy Reference Disclosure Component.

LEGAL POSITIONING
-----------------
- Displays authoritative policy & standard references
- Declarative, non-interpretive
- Prevents implicit legal claims by UI

COMPLIANCE
----------
✔ MASTER_SPEC.md
✔ IMPLEMENTATION STATUS PHẦN 1
✔ IMPLEMENTATION STATUS PHẦN 2
✔ Governance-first UI
✔ Court-defensible disclosure
"""

import streamlit as st
from typing import List, Dict

from ui.shared.utils.safe_render import safe_render


# =========================
# STATIC POLICY REFERENCES
# =========================

def _policy_references() -> List[Dict]:
    """
    Static list of policy & regulatory references.

    GOVERNANCE GUARANTEES
    ---------------------
    - Hardcoded
    - Reviewed by governance / legal
    - No runtime mutation
    """

    return [
        {
            "title": "Vietnamese Valuation Standards (TĐGVN)",
            "description": "Statutory valuation standards applicable in Vietnam.",
        },
        {
            "title": "Bank Internal Credit Risk Management Policy",
            "description": "Internal bank policy governing valuation use in credit decisions.",
        },
        {
            "title": "Model Risk Management (MRM) Framework",
            "description": "Internal framework for model governance, validation, and audit.",
        },
        {
            "title": "MASTER_SPEC.md",
            "description": "System-wide immutable architecture & role separation blueprint.",
        },
        {
            "title": "Internal Override & Approval Policy",
            "description": "Defines human override authority, logging, and accountability.",
        },
    ]


# =========================
# COMPONENT RENDER
# =========================

def policy_reference_box():
    """
    Render governance policy reference box.

    GOVERNANCE
    ----------
    - Informational only
    - No compliance assertion
    - No legal interpretation
    """

    st.subheader("📚 Policy & Regulatory References")

    safe_render(
        """
        <div style="border-left: 4px solid #198754; padding-left: 12px;">
            <strong>Governance Notice:</strong><br/>
            The following references indicate the <em>policy and regulatory sources</em>
            considered in the design of this system.
            <br/><br/>
            This list is provided for <strong>transparency only</strong> and does not
            constitute legal interpretation, certification, or automatic compliance.
        </div>
        """
    )

    st.markdown("---")

    for ref in _policy_references():
        st.markdown(f"**• {ref['title']}**")
        st.caption(ref["description"])

    st.markdown("---")

    st.caption(
        "Policy references are provided for audit and governance transparency. "
        "Final interpretation and compliance determination remain the responsibility "
        "of authorized human roles."
    )
