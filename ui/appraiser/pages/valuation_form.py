# ui/appraiser/pages/valuation_form.py
"""
VALUATION FORM – APPRAISER PAGE
===============================

🚫 GOVERNANCE LOCK – STRICT COMPLIANCE
Tuân thủ tuyệt đối:
- MASTER_SPEC.md
- IMPLEMENTATION STATUS – PART 1 & PART 2

🎯 MỤC ĐÍCH
- Hiển thị thông tin hồ sơ thẩm định (valuation_dossier)
- Cho phép Appraiser:
    ✔ xem dữ liệu đầu vào
    ✔ xem kết quả model (read-only)
    ✔ xem risk / confidence / warnings
- KHÔNG cho phép:
    ❌ chỉnh sửa dữ liệu
    ❌ tính toán lại
    ❌ ghi đè hồ sơ

📌 Đây KHÔNG phải form nhập liệu – mà là Valuation Review Form
"""

import streamlit as st
from typing import Dict, Any

from ui.shared.auth.role_guard import require_role
from ui.shared.state.role_state import Role
from ui.shared.state.session_state import get_selected_valuation_id
from ui.shared.api_client.valuation_api import get_dossier
from ui.shared.components.disclaimer_box import render_disclaimer
from ui.shared.components.model_status import render_model_status
from ui.shared.components.confidence_gauge import render_confidence_gauge
from ui.shared.components.risk_indicator import render_risk_indicator
from ui.appraiser.components.feature_snapshot import render_feature_snapshot
from ui.appraiser.components.comparable_table import render_comparable_table
from ui.appraiser.components.model_breakdown import render_model_breakdown
from ui.appraiser.components.warning_panel import render_warning_panel
from ui.shared.utils.safe_render import safe_markdown


# =========================
# PAGE ENTRY
# =========================

def render_valuation_form() -> None:
    """
    Appraiser valuation review page.

    GOVERNANCE
    ----------
    - Mọi dữ liệu lấy từ valuation_dossier (SSOT)
    - Không có bất kỳ hành vi ghi / mutate nào
    """

    # =========================
    # ROLE GUARD
    # =========================
    if not require_role(
        [Role.APPRAISER, Role.MANAGER, Role.AUDITOR],
        message="You do not have permission to access valuation review.",
    ):
        return

    st.title("🏗️ Valuation Review Form")

    render_disclaimer(
        title="Governance Disclaimer",
        message=(
            "This page displays a governed valuation dossier for human review. "
            "All information is READ-ONLY. "
            "No changes performed here will affect the valuation outcome."
        ),
        level="info",
    )

    # =========================
    # LOAD CONTEXT
    # =========================
    valuation_id = get_selected_valuation_id()
    if not valuation_id:
        st.warning("No valuation selected.")
        return

    with st.spinner("Loading valuation dossier…"):
        dossier: Dict[str, Any] = get_dossier(valuation_id)

    if not dossier:
        st.error("Unable to load valuation dossier.")
        return

    # =========================
    # BASIC INFO
    # =========================
    st.subheader("📄 Valuation Context")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Valuation ID", dossier.get("valuation_id", "N/A"))
    with col2:
        st.metric("Asset Type", dossier.get("asset_type", "N/A"))
    with col3:
        st.metric("Jurisdiction", dossier.get("jurisdiction", "N/A"))

    # =========================
    # MODEL STATUS
    # =========================
    st.subheader("🤖 Model Execution Status")
    render_model_status(dossier.get("model_status", {}))

    # =========================
    # CONFIDENCE & RISK
    # =========================
    st.subheader("📊 Risk & Confidence")

    col_risk, col_conf = st.columns(2)
    with col_risk:
        render_risk_indicator(dossier.get("risk_band"))
    with col_conf:
        render_confidence_gauge(dossier.get("confidence_score"))

    # =========================
    # FEATURE SNAPSHOT
    # =========================
    st.subheader("🧩 Feature Snapshot")
    render_feature_snapshot(dossier.get("features", {}))

    # =========================
    # COMPARABLES
    # =========================
    st.subheader("🏘️ Comparable Properties")
    render_comparable_table(dossier.get("comparables", []))

    # =========================
    # MODEL BREAKDOWN
    # =========================
    st.subheader("📐 Model Breakdown")
    render_model_breakdown(dossier.get("model_outputs", {}))

    # =========================
    # WARNINGS
    # =========================
    st.subheader("⚠️ Warnings & Limitations")
    render_warning_panel(dossier.get("warnings", []))

    # =========================
    # FOOTER – AUDIT NOTE
    # =========================
    safe_markdown(
        """
---
### Audit & Responsibility Notice
- This valuation is **not auto-approved**.
- Presence of AI outputs does **not replace** human judgment.
- Final responsibility lies with the licensed appraiser and approval workflow.

_This page is reproducible, immutable, and audit-ready._
        """
    )


"""
📌 LEGAL & GOVERNANCE STATEMENT
------------------------------
- valuation_form.py:
    ✔ Chỉ hiển thị dữ liệu
    ✔ Không sinh quyết định
    ✔ Không thay đổi workflow state

Nguyên tắc cốt lõi:
"UI hiển thị – Con người quyết – Governance kiểm soát"
"""
