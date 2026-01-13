"""
trace_timeline.py

ROLE
----
Audit Trace Timeline Component.

LEGAL POSITIONING
-----------------
- Visualizes immutable workflow events
- Supports audit replay and accountability
- Prevents ambiguity in decision chronology

COMPLIANCE
----------
✔ MASTER_SPEC.md
✔ IMPLEMENTATION STATUS PHẦN 1
✔ IMPLEMENTATION STATUS PHẦN 2
✔ Read-only audit artifact
"""

import streamlit as st
from datetime import datetime
from typing import List, Dict


# =========================
# COMPONENT
# =========================

def trace_timeline(events: List[Dict]):
    """
    Render an immutable audit trace timeline.

    Parameters
    ----------
    events : List[Dict]
        Ordered list of trace events.
        Each event must include:
            - timestamp (ISO string)
            - actor (human / system)
            - action (short verb)
            - description (human-readable)
            - immutable (bool)

    GOVERNANCE GUARANTEES
    ---------------------
    - Read-only rendering
    - No mutation
    - Chronological integrity
    """

    st.subheader("🧭 Valuation Trace Timeline")

    if not events:
        st.info("No trace events available for this valuation case.")
        return

    for idx, event in enumerate(events):
        _render_event(event, idx == 0)


# =========================
# INTERNAL RENDER
# =========================

def _render_event(event: Dict, is_first: bool):
    """
    Render a single timeline event.
    """

    timestamp = _format_ts(event.get("timestamp"))
    actor = event.get("actor", "Unknown")
    action = event.get("action", "Event")
    description = event.get("description", "")
    immutable = event.get("immutable", True)

    border_color = "#198754" if immutable else "#dc3545"
    immutability_label = "IMMUTABLE" if immutable else "NON-IMMUTABLE"

    st.markdown(
        f"""
        <div style="
            border-left: 4px solid {border_color};
            padding-left: 14px;
            margin-bottom: 14px;
        ">
            <strong>{action}</strong><br/>
            <small>
                {timestamp} · {actor} ·
                <span style="color:{border_color}; font-weight:600;">
                    {immutability_label}
                </span>
            </small>
            <br/>
            <div style="margin-top:6px;">
                {description}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================
# UTILS
# =========================

def _format_ts(ts: str) -> str:
    """
    Safely format timestamp for audit readability.
    """
    try:
        return datetime.fromisoformat(ts).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return ts or "Unknown time"
