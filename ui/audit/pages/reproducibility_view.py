"""
reproducibility_view.py

ROLE
----
Audit page for valuation reproducibility evidence.

LEGAL POSITIONING
-----------------
- Displays immutable configuration required for valuation reproduction
- Shows snapshot hashes, model versions, feature snapshots, and execution trace IDs
- Supports audit, regulatory review, and dispute resolution
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
from ui.shared.api_client.audit_api import get_reproducibility_record

from ui.shared.components.table import table
from ui.shared.components.disclaimer_box import disclaimer_box


# =========================
# PAGE ENTRY
# =========================

@require_role(["AUDITOR", "MANAGER"])
def reproducibility_view():
    """
    Reproducibility Audit Page.

    Governance Guarantees
    ---------------------
    - Role-gated (AUDITOR / MANAGER)
    - Read-only
    - No execution, no recomputation, no validation logic
    """

    st.title("♻️ Reproducibility Evidence")

    session = get_session_state()
    valuation_id = session.get("selected_valuation_id")

    if not valuation_id:
        st.warning("No valuation selected.")
        return

    record = get_reproducibility_record(valuation_id)

    if not record:
        st.error("Reproducibility record not available.")
        return

    _render_context(record)
    _render_snapshot_evidence(record)
    _render_model_evidence(record)
    _render_execution_evidence(record)

    disclaimer_box(
        "This page presents technical evidence supporting valuation reproducibility. "
        "It does not execute, validate, or certify the reproduction of results. "
        "Final interpretation and responsibility remain with authorized human reviewers."
    )


# =========================
# RENDER SECTIONS
# =========================

def _render_context(record: dict):
    """
    Render high-level reproducibility context.
    """
    st.subheader("Context")

    cols = st.columns(2)
    cols[0].markdown(f"**Valuation ID:** `{record.get('valuation_id')}`")
    cols[1].markdown(f"**Execution Trace ID:** `{record.get('execution_trace_id')}`")

    cols = st.columns(2)
    cols[0].markdown(f"**Created At:** {record.get('created_at')}")
    cols[1].markdown(f"**Reproducibility Mode:** Snapshot-based")


def _render_snapshot_evidence(record: dict):
    """
    Render snapshot and feature immutability evidence.
    """
    st.subheader("Snapshot & Feature Evidence")

    rows = [
        {
            "artifact": "Property Snapshot",
            "snapshot_id": record.get("property_snapshot_id"),
            "hash": record.get("property_snapshot_hash"),
        },
        {
            "artifact": "Feature Snapshot",
            "snapshot_id": record.get("feature_snapshot_id"),
            "hash": record.get("feature_snapshot_hash"),
        },
    ]

    table(
        data=rows,
        columns=["artifact", "snapshot_id", "hash"],
        empty_message="No snapshot evidence available."
    )


def _render_model_evidence(record: dict):
    """
    Render model version and registry evidence.
    """
    st.subheader("Model Version Evidence")

    table(
        data=record.get("models", []),
        columns=[
            "model_id",
            "model_family",
            "model_version",
            "artifact_hash",
            "registry_status",
        ],
        empty_message="No model evidence available."
    )


def _render_execution_evidence(record: dict):
    """
    Render execution configuration evidence.
    """
    st.subheader("Execution Configuration")

    rows = [
        {"parameter": "Random Seed", "value": record.get("random_seed")},
        {"parameter": "Ensemble Version", "value": record.get("ensemble_version")},
        {"parameter": "Rule Engine Version", "value": record.get("rule_engine_version")},
    ]

    table(
        data=rows,
        columns=["parameter", "value"],
        empty_message="No execution parameters available."
    )
