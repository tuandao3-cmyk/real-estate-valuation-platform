"""
hash_verification_box.py

ROLE
----
Hash Verification Evidence Renderer.

LEGAL POSITIONING
-----------------
- Displays hash comparison results between artifacts and registry records
- Supports immutability, reproducibility, and tamper-evidence claims
- Read-only, non-decisive, audit-focused UI component

COMPLIANCE
----------
✔ MASTER_SPEC.md
✔ IMPLEMENTATION STATUS PHẦN 1
✔ IMPLEMENTATION STATUS PHẦN 2
✔ No inference, no validation logic, no mutation
"""

import streamlit as st
from typing import Optional, Dict


# =========================
# COMPONENT
# =========================

def hash_verification_box(
    artifact_name: str,
    computed_hash: Optional[str],
    registry_hash: Optional[str],
    verification_status: str,
    metadata: Optional[Dict] = None,
):
    """
    Render hash verification evidence.

    Parameters
    ----------
    artifact_name : str
        Human-readable artifact identifier (e.g. 'feature_snapshot.json')

    computed_hash : Optional[str]
        Hash computed at artifact creation time (read-only display)

    registry_hash : Optional[str]
        Hash stored in official registry / dossier

    verification_status : str
        One of: 'MATCH', 'MISMATCH', 'MISSING'

    metadata : Optional[Dict]
        Optional trace metadata (request_id, timestamp, source)

    GOVERNANCE GUARANTEES
    ---------------------
    - UI does NOT compute or compare hashes
    - Status is passed from backend audit service
    - No legal conclusion is derived
    """

    st.subheader("🔐 Hash Verification")

    _render_status_badge(verification_status)

    with st.expander("Hash Details", expanded=True):
        _render_hash_row("Artifact", computed_hash)
        _render_hash_row("Registry", registry_hash)

    if metadata:
        _render_metadata(metadata)

    _render_disclaimer()


# =========================
# INTERNAL HELPERS
# =========================

def _render_status_badge(status: str):
    """
    Render visual status badge.
    """
    status = status.upper()

    if status == "MATCH":
        st.success("Hash Match — Artifact is byte-identical to registry record.")
    elif status == "MISMATCH":
        st.error("Hash Mismatch — Artifact differs from registry record.")
    elif status == "MISSING":
        st.warning("Hash Missing — Registry or artifact hash not available.")
    else:
        st.info("Hash Status Unknown.")


def _render_hash_row(label: str, value: Optional[str]):
    """
    Render a single hash row.
    """
    display_value = value if value else "—"
    st.markdown(f"**{label} Hash:** `{display_value}`")


def _render_metadata(metadata: Dict):
    """
    Render trace metadata.
    """
    st.markdown("**Trace Metadata**")
    for key, value in metadata.items():
        st.markdown(f"- **{key}**: {value}")


def _render_disclaimer():
    """
    Render governance disclaimer.
    """
    st.caption(
        "⚖️ Hash verification is presented as immutable technical evidence. "
        "This component does not assert legal validity, correctness, or approval. "
        "Final interpretation is the responsibility of authorized human reviewers."
    )
