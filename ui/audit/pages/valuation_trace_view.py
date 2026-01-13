"""
valuation_trace_view.py

ROLE
----
Audit-grade valuation trace visualization page.

LEGAL POSITIONING
-----------------
- Displays end-to-end valuation execution trace
- Shows AI / Rule / Human actions in chronological order
- Supports audit, compliance review, and dispute resolution
- Read-only, non-decisive, non-inferential

COMPLIANCE
----------
✔ MASTER_SPEC.md
✔ IMPLEMENTATION STATUS PHẦN 1
✔ IMPLEMENTATION STATUS PHẦN 2
"""

import streamlit as st

from ui.shared.auth.role_guard import require_role
from ui.shared.state.session_state import get_session_state
from ui.shared.api_client.audit_api import get_valuation_trace

from ui.audit.components.trace_timeline import trace_timeline
from ui.audit.components.provenance_table import provenance_table
from ui.audit.components.hash_verification_box import hash_verification_box
from ui.shared.components.disclaimer_box import disclaimer_box


# =========================
# PAGE ENTRY
# =========================

@require_role(["AUDITOR", "MANAGER"])
def valuation_trace_view():
    """
    Valuation Trace Audit Page.

    Governance Guarantees
    ---------------------
    - Role-gated (AUDITOR / MANAGER)
    - Read-only
    - No workflow control
    """

    st.title("📜 Valuation Trace")

    session = get_session_state()
    valuation_id = session.get("selected_valuation_id")

    if not valuation_id:
        st.warning("No valuation selected.")
        return

    trace_data = get_valuation_trace(valuation_id)

    if not trace_data:
        st.error("Valuation trace not available.")
        return

    _render_trace_overview(trace_data)
    _render_trace_timeline(trace_data)
    _render_artifact_provenance(trace_data)
    _render_hash_evidence(trace_data)

    disclaimer_box(
        "This page presents an immutable execution trace for audit and review purposes only. "
        "It does not constitute a legal determination, valuation conclusion, or approval."
    )


# =========================
# RENDER SECTIONS
# =========================

def _render_trace_overview(trace_data: dict):
    """
    Render valuation trace summary.
    """
    st.subheader("Valuation Overview")

    cols = st.columns(2)
    cols[0].markdown(f"**Valuation ID:** `{trace_data.get('valuation_id')}`")
    cols[1].markdown(f"**Snapshot ID:** `{trace_data.get('snapshot_id')}`")

    cols = st.columns(2)
    cols[0].markdown(f"**Created At:** {trace_data.get('created_at')}")
    cols[1].markdown(f"**Current Status:** {trace_data.get('status')}")


def _render_trace_timeline(trace_data: dict):
    """
    Render chronological trace timeline.
    """
    st.subheader("Execution Timeline")

    trace_timeline(
        events=trace_data.get("events", [])
    )


def _render_artifact_provenance(trace_data: dict):
    """
    Render artifact provenance table.
    """
    st.subheader("Artifact Provenance")

    provenance_table(
        artifacts=trace_data.get("artifacts", [])
    )


def _render_hash_evidence(trace_data: dict):
    """
    Render hash verification evidence for critical artifacts.
    """
    st.subheader("Hash Integrity Evidence")

    for item in trace_data.get("hash_verifications", []):
        hash_verification_box(
            artifact_name=item.get("artifact_name"),
            computed_hash=item.get("computed_hash"),
            registry_hash=item.get("registry_hash"),
            verification_status=item.get("status"),
            metadata=item.get("metadata"),
        )
