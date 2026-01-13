"""
override_panel.py

ROLE
----
Manager Override Panel (UI container only).

LEGAL POSITIONING
-----------------
- Human override information capture
- Explicit, structured, auditable
- No business logic
- No workflow control
- No implicit approval

COMPLIANCE
----------
✔ MASTER_SPEC.md
✔ IMPLEMENTATION STATUS PHẦN 1 & 2
✔ Override = Human Action
✔ UI ≠ Decision
"""

from typing import Optional, Dict

import streamlit as st

from ui.shared.utils.safe_render import safe_render
from ui.manager.components.override_reason_picker import override_reason_picker


# =========================
# OVERRIDE PANEL
# =========================

def override_panel(
    *,
    component_key: str,
    disabled: bool = False
) -> Optional[Dict]:
    """
    Render manager override panel.

    Parameters
    ----------
    component_key : str
        Unique key namespace for Streamlit state isolation
    disabled : bool
        Render panel in read-only mode (post-submission)

    Returns
    -------
    Optional[Dict]
        {
            "override_reason": {
                "reason_code": str,
                "reason_label": str,
                "free_text": Optional[str]
            },
            "manager_comment": Optional[str]
        }

        OR None if required inputs are not completed.

    GOVERNANCE
    ----------
    - This function does NOT apply override
    - This function does NOT validate business sufficiency
    - This function does NOT submit data
    """

    st.markdown("## 🧑‍💼 Manager Override Panel")

    safe_render(
        """
        <div style="border-left: 4px solid #d9534f; padding-left: 12px;">
            <strong>Important:</strong><br/>
            Any override is a <em>human decision</em> and will be logged
            with your identity, timestamp, and stated rationale.
            <br/><br/>
            This panel does <strong>not</strong> approve, apply,
            or validate an override.
        </div>
        """
    )

    st.markdown("---")

    # =========================
    # OVERRIDE REASON
    # =========================

    override_reason = override_reason_picker(
        component_key=f"{component_key}_reason",
        disabled=disabled
    )

    if override_reason is None:
        return None

    st.markdown("---")

    # =========================
    # MANAGER COMMENT (OPTIONAL)
    # =========================

    manager_comment = st.text_area(
        label="Additional manager comments (optional)",
        key=f"{component_key}_manager_comment",
        disabled=disabled,
        help="Free-text context for audit and review purposes only."
    )

    # =========================
    # RETURN RAW PAYLOAD ONLY
    # =========================

    return {
        "override_reason": override_reason,
        "manager_comment": manager_comment or None
    }