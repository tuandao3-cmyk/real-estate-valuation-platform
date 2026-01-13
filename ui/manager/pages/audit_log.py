"""
audit_log.py

ROLE
----
Audit Log Review Page (read-only).

LEGAL POSITIONING
-----------------
- Displays immutable audit events
- Supports accountability & traceability
- Read-only
- No interpretation
- No governance action

COMPLIANCE
----------
✔ MASTER_SPEC.md
✔ IMPLEMENTATION STATUS PHẦN 1 & 2
✔ Audit log immutability
✔ UI ≠ Audit authority
"""

import streamlit as st
from typing import List, Dict

from ui.shared.auth.role_guard import require_role
from ui.shared.components.table import render_table
from ui.shared.components.kv_table import render_kv_table
from ui.shared.components.disclaimer_box import disclaimer_box
from ui.shared.api_client.audit_api import fetch_audit_logs
from ui.shared.utils.safe_render import safe_render


# =========================
# ACCESS CONTROL
# =========================

require_role("MANAGER")


# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Audit Log",
    layout="wide"
)

st.title("📑 Audit Log")

safe_render(
    """
    <div style="border-left: 4px solid #5bc0de; padding-left: 12px;">
        <strong>Audit Log Notice:</strong><br/>
        The records below represent an <em>immutable system audit trail</em>.
        <br/><br/>
        This interface provides <strong>visibility only</strong>.
        No record can be modified, deleted, filtered by interpretation,
        or reclassified from this page.
    </div>
    """
)

st.markdown("---")


# =========================
# FETCH AUDIT LOGS
# =========================

@st.cache_data(show_spinner=False)
def load_audit_logs() -> List[Dict]:
    """
    Fetch audit logs from backend.

    GOVERNANCE
    ----------
    - Read-only
    - Append-only source
    - Ordered by timestamp (backend responsibility)
    """
    return fetch_audit_logs()


audit_logs = load_audit_logs()


# =========================
# EMPTY STATE
# =========================

if not audit_logs:
    st.info("No audit events are available.")
    disclaimer_box()
    st.stop()


# =========================
# AUDIT LOG TABLE
# =========================

st.subheader("Audit Events")

render_table(
    data=audit_logs,
    key="audit_log_table",
    selectable=True,
    selection_mode="single",
    help_text="Select an audit event to view full details."
)

st.markdown("---")


# =========================
# DETAIL VIEW
# =========================

selected_rows = st.session_state.get("audit_log_table_selected")

if selected_rows:
    event = selected_rows[0]

    st.markdown("### 🔍 Audit Event Details")

    render_kv_table(
        {
            "Event ID": event.get("event_id"),
            "Timestamp": event.get("timestamp"),
            "Actor": event.get("actor"),
            "Actor Role": event.get("actor_role"),
            "Action": event.get("action"),
            "Entity Type": event.get("entity_type"),
            "Entity ID": event.get("entity_id"),
            "Source IP": event.get("source_ip"),
            "Session ID": event.get("session_id"),
        }
    )

    st.markdown("#### 🧾 Event Payload (Raw)")

    st.json(
        event.get("payload", {}),
        expanded=False
    )


# =========================
# LEGAL DISCLAIMER
# =========================

disclaimer_box()
