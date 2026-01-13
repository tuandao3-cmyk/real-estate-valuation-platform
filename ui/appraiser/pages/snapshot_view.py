# ui/appraiser/pages/snapshot_view.py
"""
SNAPSHOT VIEW – APPRAISER
========================

🚫 GOVERNANCE LOCK – STRICT COMPLIANCE
Tuân thủ tuyệt đối:
- MASTER_SPEC.md
- IMPLEMENTATION STATUS – PART 1 & PART 2

🎯 MỤC ĐÍCH
- Hiển thị Feature Snapshot đã được backend đóng băng
- Phục vụ:
    ✔ Appraiser review
    ✔ Audit traceability
- READ-ONLY tuyệt đối

📌 NGUYÊN TẮC BẤT BIẾN
- Snapshot = bằng chứng
- UI KHÔNG:
    ❌ sửa
    ❌ enrich
    ❌ suy luận
    ❌ tái tính toán
"""

import streamlit as st
from typing import Dict, Any

from ui.shared.auth.role_guard import require_role
from ui.shared.state.role_state import Role
from ui.shared.state.session_state import get_selected_valuation_id
from ui.shared.api_client.valuation_api import get_dossier
from ui.shared.components.disclaimer_box import render_disclaimer
from ui.shared.components.table import render_table
from ui.shared.utils.safe_render import safe_markdown


# =========================
# PAGE ENTRY
# =========================

def render_snapshot_view() -> None:
    """
    Render immutable feature snapshot for Appraiser.
    """

    # =========================
    # ROLE GUARD
    # =========================
    if not require_role(
        [Role.APPRAISER],
        message="Only Appraisers are allowed to view valuation snapshots.",
    ):
        return

    st.title("📦 Feature Snapshot (Read-Only)")

    render_disclaimer(
        title="Snapshot Governance",
        message=(
            "This snapshot represents the immutable input state at the moment "
            "the valuation was triggered. It is legally auditable and cannot "
            "be modified."
        ),
        level="warning",
    )

    # =========================
    # LOAD CONTEXT
    # =========================
    valuation_id = get_selected_valuation_id()

    if not valuation_id:
        st.info("No valuation selected. Please submit or select a valuation first.")
        return

    # =========================
    # FETCH SNAPSHOT
    # =========================
    with st.spinner("Loading snapshot…"):
        dossier: Dict[str, Any] = get_dossier(valuation_id)

    if not dossier:
        st.error("Unable to load snapshot dossier.")
        return

    snapshot: Dict[str, Any] = dossier.get("feature_snapshot")
    metadata: Dict[str, Any] = dossier.get("metadata", {})

    if not snapshot:
        st.warning("No feature snapshot found for this valuation.")
        return

    # =========================
    # METADATA
    # =========================
    st.subheader("🧾 Snapshot Metadata")

    render_table(
        [
            {"Field": "Valuation ID", "Value": valuation_id},
            {"Field": "Snapshot Hash", "Value": metadata.get("feature_snapshot_hash")},
            {"Field": "Created At", "Value": metadata.get("snapshot_timestamp")},
            {"Field": "Schema Version", "Value": metadata.get("snapshot_schema_version")},
        ]
    )

    # =========================
    # SNAPSHOT CONTENT
    # =========================
    st.subheader("📊 Feature Data (Frozen)")

    # Render as key-value table, grouped
    rows = [
        {"Feature": key, "Value": value}
        for key, value in snapshot.items()
    ]

    render_table(rows)

    # =========================
    # FOOTNOTE
    # =========================
    safe_markdown(
        """
---
### Legal Notice
- This snapshot is **append-only evidence**.
- Any discrepancy with on-site inspection must be handled via:
  **Human review or override workflow**.
- Snapshot data is **not equal** to legal truth or market value.

📌 *Snapshot ≠ Valuation ≠ Approval*
        """
    )


"""
📌 AUDIT & LEGAL NOTES
---------------------
- Snapshot view is mandatory for valuation traceability
- UI đóng vai trò trình bày bằng chứng, không diễn giải
- Mọi thay đổi yêu cầu override được log riêng

Nguyên tắc cốt lõi:
"Frozen input → reproducible valuation → defensible outcome"
"""
