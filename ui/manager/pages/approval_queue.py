"""
approval_queue.py

ROLE
----
Manager Approval Queue Page (UI only).

LEGAL POSITIONING
-----------------
- Displays pending approvals
- Allows selection for review
- No decision logic
- No workflow control
- No approval execution

COMPLIANCE
----------
✔ MASTER_SPEC.md
✔ IMPLEMENTATION STATUS PHẦN 1 & 2
✔ UI ≠ Decision
✔ UI ≠ Workflow
✔ UI ≠ Governance
"""

import streamlit as st
from typing import List, Dict

from ui.shared.state.session_state import session_state
from ui.shared.auth.role_guard import require_role
from ui.shared.components.table import render_table
from ui.shared.components.disclaimer_box import disclaimer_box
from ui.shared.api_client.governance_api import fetch_manager_approval_queue
from ui.shared.utils.safe_render import safe_render


# =========================
# ACCESS CONTROL
# =========================

require_role("MANAGER")


# =========================
# PAGE HEADER
# =========================

st.set_page_config(
    page_title="Manager Approval Queue",
    layout="wide"
)

st.title("📋 Approval Queue")

safe_render(
    """
    <div style="border-left: 4px solid #f0ad4e; padding-left: 12px;">
        <strong>Manager Responsibility Notice:</strong><br/>
        The items listed below require <em>human managerial review</em>.
        <br/><br/>
        This page does <strong>not</strong> approve, reject,
        or modify any valuation result.
        All decisions must be explicitly declared on the review page.
    </div>
    """
)

st.markdown("---")


# =========================
# FETCH APPROVAL QUEUE
# =========================

@st.cache_data(show_spinner=False)
def load_approval_queue() -> List[Dict]:
    """
    Fetch approval queue from backend.

    GOVERNANCE
    ----------
    - Read-only
    - No filtering logic
    - No prioritization
    """
    return fetch_manager_approval_queue()


approval_items = load_approval_queue()


# =========================
# EMPTY STATE
# =========================

if not approval_items:
    st.info("No valuations are currently pending managerial approval.")
    disclaimer_box()
    st.stop()


# =========================
# DISPLAY TABLE
# =========================

st.subheader("Pending Valuations")

render_table(
    data=approval_items,
    key="manager_approval_queue_table",
    selectable=True,
    selection_mode="single",
    help_text="Select a valuation to review details."
)

st.markdown("---")


# =========================
# SELECTION HANDLING
# =========================

selected_rows = st.session_state.get("manager_approval_queue_table_selected")

if selected_rows:
    selected_item = selected_rows[0]

    st.markdown("### 🔍 Selected Valuation")

    st.write(f"**Valuation ID:** `{selected_item.get('valuation_id')}`")
    st.write(f"**Asset Type:** {selected_item.get('asset_type')}")
    st.write(f"**Jurisdiction:** {selected_item.get('jurisdiction')}")
    st.write(f"**Risk Band:** {selected_item.get('risk_band')}")
    st.write(f"**Submitted At:** {selected_item.get('submitted_at')}")

    st.markdown("---")

    if st.button("Review valuation"):
        session_state.selected_valuation_id = selected_item.get("valuation_id")
        st.switch_page("ui/manager/pages/approval_review.py")


# =========================
# LEGAL DISCLAIMER
# =========================

disclaimer_box()
