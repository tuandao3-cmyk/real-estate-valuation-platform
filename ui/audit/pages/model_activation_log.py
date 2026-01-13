"""
model_activation_log.py

ROLE
----
Audit page for model activation governance logs.

LEGAL POSITIONING
-----------------
- Displays immutable activation permission records
- Supports audit, compliance review, and regulatory inspection
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
from ui.shared.api_client.audit_api import get_model_activation_logs

from ui.shared.components.table import table
from ui.shared.components.disclaimer_box import disclaimer_box


# =========================
# PAGE ENTRY
# =========================

@require_role(["AUDITOR", "MANAGER"])
def model_activation_log():
    """
    Model Activation Log Audit Page.

    Governance Guarantees
    ---------------------
    - Role-gated (AUDITOR / MANAGER)
    - Read-only access
    - No activation, no rollback, no control actions
    """

    st.title("🧩 Model Activation Log")

    session = get_session_state()
    valuation_id = session.get("selected_valuation_id")

    if not valuation_id:
        st.warning("No valuation selected.")
        return

    activation_logs = get_model_activation_logs(valuation_id)

    if not activation_logs:
        st.info("No model activation records found.")
        return

    _render_overview(valuation_id)
    _render_activation_table(activation_logs)

    disclaimer_box(
        "This page displays immutable records of model activation permissions. "
        "It does not indicate model quality, correctness, or suitability for valuation decisions. "
        "Interpretation and accountability remain with authorized human reviewers."
    )


# =========================
# RENDER SECTIONS
# =========================

def _render_overview(valuation_id: str):
    """
    Render page overview metadata.
    """
    st.subheader("Context")
    st.markdown(f"**Valuation ID:** `{valuation_id}`")
    st.markdown("**Log Type:** Model Activation Permission Records")


def _render_activation_table(logs: list):
    """
    Render model activation log table.
    """
    st.subheader("Activation Records")

    columns = [
        "timestamp",
        "model_id",
        "model_version",
        "activation_status",
        "policy_reference",
        "actor",
        "reason_code",
    ]

    table(
        data=logs,
        columns=columns,
        empty_message="No activation records available."
    )
