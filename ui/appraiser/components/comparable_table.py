# ui/appraiser/components/comparable_table.py
"""
COMPARABLE TABLE – APPRAISER VIEW
================================

🚫 GOVERNANCE LOCK – STRICT COMPLIANCE
Tuân thủ tuyệt đối:
- MASTER_SPEC.md
- IMPLEMENTATION STATUS – PART 1 & PART 2

📌 MỤC ĐÍCH
- Hiển thị danh sách BĐS so sánh (comparables) đã được model sử dụng
- Phục vụ thẩm định viên:
    ✔ kiểm tra tính phù hợp
    ✔ đánh giá độ tương đồng
    ✔ giải trình quyết định định giá

📌 NGUYÊN TẮC BẤT BIẾN
- READ-ONLY tuyệt đối
- KHÔNG:
    ❌ thêm / xoá / sửa comparable
    ❌ tính lại trọng số
    ❌ suy luận giá
    ❌ che giấu dispersion

📌 Comparable table = bằng chứng thị trường tại thời điểm định giá
"""

import streamlit as st
from typing import List, Dict, Any

from ui.shared.components.table import render_table
from ui.shared.components.disclaimer_box import render_disclaimer
from ui.shared.auth.role_guard import require_role
from ui.shared.state.role_state import Role
from ui.shared.utils.format_price import format_price
from ui.shared.utils.format_date import format_date
from ui.shared.utils.safe_render import safe_markdown


# =========================
# MAIN RENDER
# =========================

def render_comparable_table(
    comparables: List[Dict[str, Any]],
) -> None:
    """
    Render bảng BĐS so sánh.

    Parameters
    ----------
    comparables : List[Dict[str, Any]]
        Danh sách comparable đã được backend chọn & freeze.
        Ví dụ mỗi item:
        {
            "id": "...",
            "address": "...",
            "price": 3500000000,
            "transaction_date": "2024-08-12",
            "distance_km": 0.8,
            "similarity_score": 0.82,
            "data_source": "Registry / Listing"
        }

    GOVERNANCE
    ----------
    - Dữ liệu phải đến từ valuation_dossier
    - UI không được suy luận hay tính toán bổ sung
    """

    # =========================
    # ROLE GUARD
    # =========================
    if not require_role(
        [Role.APPRAISER, Role.MANAGER, Role.AUDITOR],
        message="Comparable data is restricted to appraisal roles.",
    ):
        return

    st.subheader("🏘️ Comparable Properties (Read-Only)")

    render_disclaimer(
        title="Governance Notice",
        message=(
            "Comparable properties shown below are selected by the system "
            "based on predefined similarity rules and data availability. "
            "They are provided for review and explanation only."
        ),
        level="info",
    )

    if not comparables:
        st.warning("No comparable properties available.")
        return

    # =========================
    # PREPARE TABLE DATA
    # =========================
    table_rows: List[Dict[str, Any]] = []

    for comp in comparables:
        table_rows.append(
            {
                "ID": comp.get("id"),
                "Address": comp.get("address"),
                "Transaction Price": format_price(comp.get("price")),
                "Transaction Date": format_date(comp.get("transaction_date")),
                "Distance (km)": comp.get("distance_km"),
                "Similarity": comp.get("similarity_score"),
                "Source": comp.get("data_source"),
            }
        )

    # =========================
    # RENDER TABLE
    # =========================
    render_table(
        data=table_rows,
        columns=[
            "ID",
            "Address",
            "Transaction Price",
            "Transaction Date",
            "Distance (km)",
            "Similarity",
            "Source",
        ],
        caption=(
            "List of comparable properties used by similarity models. "
            "No manual adjustment is allowed at UI level."
        ),
    )

    # =========================
    # AUDIT FOOTNOTE
    # =========================
    safe_markdown(
        """
**Audit Notes**
- Comparable selection follows predefined similarity logic.
- Similarity score reflects *feature agreement*, not value judgment.
- Any concern must be handled via:
  - Comparable review comments
  - Manual override (if permitted by policy)

_AI does not choose comparables arbitrarily._
        """
    )


"""
📌 AUDIT & LEGAL NOTES
---------------------
- Comparable Table:
    ✔ Bằng chứng thị trường bắt buộc
    ✔ Phục vụ giải trình với ngân hàng / kiểm toán
    ✔ Không được chỉnh sửa hậu kiểm

Nguyên tắc vàng:
"So sánh là tham chiếu – không phải quyết định."

AI hỗ trợ chọn.  
Con người chịu trách nhiệm đánh giá.
"""
