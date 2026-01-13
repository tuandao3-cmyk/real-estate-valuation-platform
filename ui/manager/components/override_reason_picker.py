"""
override_reason_picker.py

ROLE
----
UI Component for Manager to explicitly select override reason.

LEGAL POSITIONING
-----------------
- Human action capture only
- No business logic
- No validation of correctness
- No auto-selection
- No implicit approval

COMPLIANCE
----------
✔ MASTER_SPEC.md – Override is human-only, reason-coded, auditable
✔ IMPLEMENTATION STATUS P1 & P2
✔ UI ≠ Decision
✔ Selection ≠ Approval
"""

from enum import Enum
from typing import Optional

import streamlit as st

from ui.shared.utils.safe_render import safe_render


# =========================
# OVERRIDE REASON ENUM
# =========================

class OverrideReason(Enum):
    MARKET_ANOMALY = "Market anomaly not captured by models"
    DATA_INCOMPLETE = "Incomplete or outdated input data"
    LEGAL_ISSUE = "Legal / ownership considerations"
    PHYSICAL_INSPECTION = "Physical inspection findings"
    POLICY_EXCEPTION = "Approved policy exception"
    OTHER = "Other (must specify)"


# =========================
# UI COMPONENT
# =========================

def override_reason_picker(
    *,
    component_key: str,
    disabled: bool = False
) -> Optional[dict]:
    """
    Render override reason selector for Manager role.

    Parameters
    ----------
    component_key : str
        Unique Streamlit key namespace (audit & state safety)
    disabled : bool
        Render in read-only mode (e.g. after submission)

    Returns
    -------
    Optional[dict]
        {
            "reason_code": str,
            "reason_label": str,
            "free_text": Optional[str]
        }

        OR None if not selected yet.

    GOVERNANCE
    ----------
    - Does NOT trigger override
    - Does NOT validate sufficiency
    - Does NOT submit anything
    """

    st.markdown("### 🧑‍⚖️ Override Reason (Manager Required)")

    safe_render(
        """
        <small>
        Selecting a reason does <strong>not</strong> approve or apply an override.
        This information is recorded for audit and accountability purposes only.
        </small>
        """
    )

    reason_options = list(OverrideReason)

    selected_reason = st.radio(
        label="Select override reason",
        options=reason_options,
        format_func=lambda r: r.value,
        key=f"{component_key}_reason_code",
        disabled=disabled
    )

    free_text: Optional[str] = None

    if selected_reason == OverrideReason.OTHER:
        free_text = st.text_area(
            label="Please specify",
            key=f"{component_key}_reason_free_text",
            disabled=disabled,
            help="Required for audit traceability"
        )

    # Do NOT return partial / implicit data
    if not selected_reason:
        return None

    if selected_reason == OverrideReason.OTHER and not free_text:
        return None

    return {
        "reason_code": selected_reason.name,
        "reason_label": selected_reason.value,
        "free_text": free_text
    }
