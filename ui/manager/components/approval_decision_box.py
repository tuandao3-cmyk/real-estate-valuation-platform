"""
approval_decision_box.py

ROLE
----
Manager Approval Decision Capture (UI only).

LEGAL POSITIONING
-----------------
- Human decision declaration
- Explicit, non-inferred
- No business logic
- No workflow control
- No implicit approval

COMPLIANCE
----------
✔ MASTER_SPEC.md
✔ IMPLEMENTATION STATUS PHẦN 1 & 2
✔ Maker–Checker separation
✔ UI ≠ Decision enforcement
"""

from enum import Enum
from typing import Optional, Dict

import streamlit as st

from ui.shared.utils.safe_render import safe_render


# =========================
# DECISION ENUM
# =========================

class ApprovalDecision(Enum):
    APPROVE = "Approve valuation result"
    REJECT = "Reject valuation result"
    REQUEST_REVIEW = "Request further review"


# =========================
# APPROVAL DECISION BOX
# =========================

def approval_decision_box(
    *,
    component_key: str,
    disabled: bool = False
) -> Optional[Dict]:
    """
    Render manager approval decision box.

    Parameters
    ----------
    component_key : str
        Unique Streamlit key namespace
    disabled : bool
        Render as read-only (e.g. after submission)

    Returns
    -------
    Optional[Dict]
        {
            "decision_code": str,
            "decision_label": str,
            "decision_comment": Optional[str]
        }

        OR None if decision not yet selected.

    GOVERNANCE
    ----------
    - Does NOT approve anything
    - Does NOT reject anything
    - Does NOT block or advance workflow
    - Records declaration only
    """

    st.markdown("## ✅ Manager Decision Declaration")

    safe_render(
        """
        <div style="border-left: 4px solid #0275d8; padding-left: 12px;">
            <strong>Declaration Notice:</strong><br/>
            Your selection below represents a <em>human managerial decision</em>.
            <br/><br/>
            This interface does <strong>not</strong> enforce, validate,
            or execute the decision.
            All effects are subject to backend policy, audit logging,
            and institutional governance.
        </div>
        """
    )

    st.markdown("---")

    decision_options = list(ApprovalDecision)

    selected_decision = st.radio(
        label="Select decision",
        options=decision_options,
        format_func=lambda d: d.value,
        key=f"{component_key}_decision_code",
        disabled=disabled
    )

    if not selected_decision:
        return None

    st.markdown("---")

    decision_comment = st.text_area(
        label="Manager comment (optional but recommended)",
        key=f"{component_key}_decision_comment",
        disabled=disabled,
        help="Free-text rationale for audit and accountability purposes."
    )

    return {
        "decision_code": selected_decision.name,
        "decision_label": selected_decision.value,
        "decision_comment": decision_comment or None
    }
