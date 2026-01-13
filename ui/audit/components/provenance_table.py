"""
provenance_table.py

ROLE
----
Provenance / Data Lineage Visualization Component.

LEGAL POSITIONING
-----------------
- Displays immutable data lineage (parent → child)
- Supports forensic audit & reproducibility claims
- Prevents hidden inference or silent data mutation

COMPLIANCE
----------
✔ MASTER_SPEC.md
✔ IMPLEMENTATION STATUS PHẦN 1
✔ IMPLEMENTATION STATUS PHẦN 2
✔ Read-only, audit-grade evidence renderer
"""

import streamlit as st
from typing import List, Dict


# =========================
# COMPONENT
# =========================

def provenance_table(records: List[Dict]):
    """
    Render a provenance / lineage table.

    Parameters
    ----------
    records : List[Dict]
        Each record must include:
            - parent_hashes : List[str]
            - child_hash : str
            - process_name : str
            - created_at_utc : str (ISO)
            - immutable : bool

    GOVERNANCE GUARANTEES
    ---------------------
    - Read-only rendering
    - No inference
    - No mutation
    """

    st.subheader("🔗 Data Provenance & Lineage")

    if not records:
        st.info("No provenance records available.")
        return

    table_rows = []
    for rec in records:
        table_rows.append(_normalize_row(rec))

    st.dataframe(
        table_rows,
        use_container_width=True,
        hide_index=True,
    )

    _render_disclaimer()


# =========================
# INTERNAL HELPERS
# =========================

def _normalize_row(record: Dict) -> Dict:
    """
    Normalize a provenance record for display.
    """

    parents = record.get("parent_hashes", [])
    parent_display = ", ".join(parents) if parents else "—"

    immutable = record.get("immutable", True)
    immutability_label = "IMMUTABLE" if immutable else "NON-IMMUTABLE"

    return {
        "Process": record.get("process_name", "Unknown"),
        "Parent Hash(es)": parent_display,
        "Child Hash": record.get("child_hash", "Unknown"),
        "Created At (UTC)": record.get("created_at_utc", "Unknown"),
        "Immutability": immutability_label,
    }


def _render_disclaimer():
    """
    Render governance disclaimer.
    """
    st.caption(
        "⚖️ Provenance records are immutable evidence of data lineage. "
        "This table is descriptive only and does not validate correctness "
        "or legality of the underlying data."
    )
