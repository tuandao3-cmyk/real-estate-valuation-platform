"""
data_provenance_view.py

ROLE
----
Audit page for data provenance and lineage evidence.

LEGAL POSITIONING
-----------------
- Displays immutable records of data sources used in valuation
- Shows snapshot references, source systems, and ingestion timestamps
- Supports audit, compliance, and dispute resolution
- Read-only, non-decisive, non-inferential UI

COMPLIANCE
----------
✔ MASTER_SPEC.md
✔ IMPLEMENTATION STATUS PHẦN 1
✔ IMPLEMENTATION STATUS PHẦN 2
"""

import streamlit as st

from ui.shared.auth.role_guard import require_role
from ui.shared.state.session_state import get_session_state
from ui.shared.api_client.audit_api import get_data_provenance

from ui.shared.components.table import table
from ui.shared.components.disclaimer_box import disclaimer_box


# =========================
# PAGE ENTRY
# =========================

@require_role(["AUDITOR", "MANAGER"])
def data_provenance_view():
    """
    Data Provenance Audit Page.

    Governance Guarantees
    ---------------------
    - Role-gated (AUDITOR / MANAGER)
    - Read-only
    - No data validation or inference
    """

    st.title("🗂️ Data Provenance")

    session = get_session_state()
    valuation_id = session.get("selected_valuation_id")

    if not valuation_id:
        st.warning("No valuation selected.")
        return

    provenance_records = get_data_provenance(valuation_id)

    if not provenance_records:
        st.info("No data provenance records available.")
        return

    _render_context(valuation_id)
    _render_provenance_table(provenance_records)

    disclaimer_box(
        "This page presents data provenance records for audit and review purposes only. "
        "It does not assess data quality, suitability, or correctness. "
        "All interpretations and responsibilities remain with authorized human reviewers."
    )


# =========================
# RENDER SECTIONS
# =========================

def _render_context(valuation_id: str):
    """
    Render page context information.
    """
    st.subheader("Context")
    st.markdown(f"**Valuation ID:** `{valuation_id}`")
    st.markdown("**Evidence Type:** Data Source & Snapshot Lineage")


def _render_provenance_table(records: list):
    """
    Render data provenance table.
    """
    st.subheader("Data Source Records")

    columns = [
        "data_domain",
        "source_system",
        "snapshot_id",
        "ingested_at",
        "schema_version",
        "hash_reference",
    ]

    table(
        data=records,
        columns=columns,
        empty_message="No provenance data found."
    )
