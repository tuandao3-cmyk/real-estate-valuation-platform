"""
override_view.py

ROLE
----
Manager Override Review Page (read-only).

LEGAL POSITIONING
-----------------
- Displays historical overrides
- Ensures transparency & accountability
- Read-only
- No decision making
- No workflow control

COMPLIANCE
----------
✔ MASTER_SPEC.md
✔ IMPLEMENTATION STATUS PHẦN 1 & 2
✔ Override ≠ Error
✔ UI ≠ Governance
"""

import streamlit as st
from typing import List, Dict

from ui.shared.auth.role_guard import require_role
from ui.shared.components.disclaimer_box import disclaimer_box
from ui.shared.components.kv_table import render_kv_table
from ui.shared.components.table import render_table
from ui.shared.api_client.governance_api import fetch_override_history
from ui.shared.utils.safe_render import safe_render


# =========================
# ACCESS CONTROL
# =========================

require_role("MANAGER")


# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Override Review",
    layout="wide"
)

st.title("🛑 Override Review")

safe_render(
    """
    <div style="border-left: 4px solid #d9534f; padding-left: 12px;">
        <strong>Override Transparency Notice:</strong><br/>
        Overrides are <em>expected governance actions</em>,
        not system failures.
        <br/><br/>
        This page is provided for <strong>review and accountability</strong> only.
        No override can be created, modified, or reversed from this interface.
    </div>
    """
)

st.markdown("---")


# =========================
# FETCH OVERRIDE HISTORY
# =========================

@st.cache_data(show_spinner=False)
def load_override_history() -> List[Dict]:
    """
    Fetch override history.

    GOVERNANCE
    ----------
    - Read-only
    - Chronological
    - No interpretation
    """
    return fetch_override_history()


override_items = load_override_history()


# =========================
# EMPTY STATE
# =========================

if not override_items:
    st.info("No overrides have been recorded in the system.")
    disclaimer_box()
    st.stop()


# =========================
# OVERRIDE TABLE
# =========================

st.subheader("Override History")

render_table(
    data=override_items,
    key="override_history_table",
    selectable=True,
    selection_mode="single",
    help_text="Select an override record to view details."
)

st.markdown("---")


# =========================
# DETAIL VIEW
# =========================

selected_rows = st.session_state.get("override_history_table_selected")

if selected_rows:
    selected_override = selected_rows[0]

    st.markdown("### 🔍 Override Details")

    render_kv_table(
        {
            "Override ID": selected_override.get("override_id"),
            "Valuation ID": selected_override.get("valuation_id"),
            "Overridden By": selected_override.get("actor"),
            "Role": selected_override.get("actor_role"),
            "Timestamp": selected_override.get("timestamp"),
            "Override Type": selected_override.get("override_type"),
            "Reason Code": selected_override.get("reason_code"),
            "Reason Description": selected_override.get("reason_description"),
            "Original Value": selected_override.get("original_value"),
            "Overridden Value": selected_override.get("overridden_value"),
        }
    )

    st.markdown("#### 📝 Rationale")

    st.text_area(
        label="Override Rationale",
        value=selected_override.get("rationale", ""),
        height=180,
        disabled=True
    )


# =========================
# LEGAL DISCLAIMER
# =========================

disclaimer_box()
