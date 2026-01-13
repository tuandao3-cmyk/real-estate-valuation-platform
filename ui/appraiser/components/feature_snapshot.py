# ui/appraiser/components/feature_snapshot.py
"""
FEATURE SNAPSHOT – APPRAISER VIEW
================================

🚫 GOVERNANCE LOCK – STRICT COMPLIANCE
Tuân thủ tuyệt đối:
- MASTER_SPEC.md
- IMPLEMENTATION STATUS – PART 1 & PART 2

📌 MỤC ĐÍCH
- Hiển thị snapshot các feature đã được sử dụng cho valuation
- Phục vụ thẩm định viên:
    ✔ kiểm tra dữ liệu đầu vào
    ✔ phát hiện bất thường
    ✔ phục vụ giải trình & audit

📌 NGUYÊN TẮC BẤT BIẾN
- CHỈ HIỂN THỊ (READ-ONLY)
- KHÔNG:
    ❌ chỉnh sửa feature
    ❌ tái tính toán
    ❌ suy luận giá
    ❌ ảnh hưởng model

📌 Feature snapshot = bằng chứng dữ liệu tại thời điểm định giá
"""

import streamlit as st
from typing import Dict, Any

from ui.shared.components.table import render_table
from ui.shared.components.disclaimer_box import render_disclaimer
from ui.shared.auth.role_guard import require_role
from ui.shared.state.role_state import Role
from ui.shared.utils.safe_render import safe_markdown


# =========================
# MAIN RENDER
# =========================

def render_feature_snapshot(
    feature_snapshot: Dict[str, Any],
) -> None:
    """
    Render snapshot các feature đầu vào.

    Parameters
    ----------
    feature_snapshot : Dict[str, Any]
        Dictionary chứa feature name -> value
        Đã được backend snapshot & freeze.

    GOVERNANCE
    ----------
    - Dữ liệu phải đến từ valuation_dossier
    - UI không được tự tổng hợp hay biến đổi
    """

    # =========================
    # ROLE GUARD
    # =========================
    if not require_role(
        [Role.APPRAISER, Role.MANAGER, Role.AUDITOR],
        message="Feature snapshot is restricted to appraisal roles.",
    ):
        return

    st.subheader("📊 Feature Snapshot (Read-Only)")

    render_disclaimer(
        title="Governance Notice",
        message=(
            "This feature snapshot reflects the exact input data used at the time "
            "of valuation. Data is immutable and provided for review and audit only. "
            "Any discrepancy must be handled via override or data correction workflow."
        ),
        level="info",
    )

    if not feature_snapshot:
        st.warning("No feature snapshot available.")
        return

    # =========================
    # PREPARE TABLE DATA
    # =========================
    table_rows = []

    for feature_name, feature_value in feature_snapshot.items():
        table_rows.append(
            {
                "Feature": feature_name,
                "Value": str(feature_value),
            }
        )

    # =========================
    # RENDER TABLE
    # =========================
    render_table(
        data=table_rows,
        columns=["Feature", "Value"],
        caption="Snapshot of normalized & engineered features (frozen).",
    )

    # =========================
    # AUDIT FOOTNOTE
    # =========================
    safe_markdown(
        """
**Audit Note**
- Features shown here are *inputs*, not decisions.
- Any concern must be escalated through:
  - Data issue reporting
  - Manual override (if permitted by role & policy)

_AI systems do not modify this snapshot._
        """
    )


"""
📌 AUDIT & LEGAL NOTES
---------------------
- Feature Snapshot:
    ✔ Bắt buộc cho tái hiện định giá
    ✔ Phục vụ kiểm toán & tranh tụng
    ✔ Tách biệt hoàn toàn khỏi logic model

- UI chỉ là:
    👉 Cửa sổ quan sát (inspection window)

Nguyên tắc bất biến:
"Dữ liệu đầu vào đúng → định giá mới có giá trị pháp lý."
"""
