# ui/appraiser/components/model_breakdown.py
"""
MODEL BREAKDOWN – APPRAISER VIEW
===============================

🚫 GOVERNANCE LOCK – STRICT COMPLIANCE
Tuân thủ tuyệt đối:
- MASTER_SPEC.md
- IMPLEMENTATION STATUS – PART 1 & PART 2

📌 MỤC ĐÍCH
- Hiển thị breakdown kết quả từ CÁC AVM CORE MODELS
- Cho phép thẩm định viên:
    ✔ xem từng model đã chạy
    ✔ xem output độc lập của mỗi model
    ✔ hiểu mức độ phân tán (dispersion)

📌 NGUYÊN TẮC BẤT BIẾN
- READ-ONLY tuyệt đối
- KHÔNG:
    ❌ ensemble lại
    ❌ chọn model tốt hơn
    ❌ điều chỉnh trọng số
    ❌ suy luận giá cuối

📌 Đây KHÔNG PHẢI là nơi quyết định giá
→ chỉ là minh bạch hoá mô hình
"""

import streamlit as st
from typing import List, Dict, Any

from ui.shared.auth.role_guard import require_role
from ui.shared.state.role_state import Role
from ui.shared.components.table import render_table
from ui.shared.components.disclaimer_box import render_disclaimer
from ui.shared.components.model_status import render_model_status
from ui.shared.utils.format_price import format_price
from ui.shared.utils.safe_render import safe_markdown


# =========================
# MAIN RENDER
# =========================

def render_model_breakdown(
    model_outputs: List[Dict[str, Any]],
) -> None:
    """
    Render breakdown các model AVM.

    Parameters
    ----------
    model_outputs : List[Dict[str, Any]]
        Ví dụ:
        [
            {
                "model_id": "hedonic_v3",
                "model_type": "HEDONIC",
                "version": "3.1.0",
                "status": "OK",
                "estimated_price": 4_200_000_000,
                "confidence_note": "High data coverage",
                "limitations": "Urban areas only"
            },
            ...
        ]

    GOVERNANCE
    ----------
    - Output phải đến từ valuation_dossier
    - UI không được tính toán hay xếp hạng
    """

    # =========================
    # ROLE GUARD
    # =========================
    if not require_role(
        [Role.APPRAISER, Role.MANAGER, Role.AUDITOR],
        message="Model breakdown is restricted to appraisal roles.",
    ):
        return

    st.subheader("🧠 Model Output Breakdown")

    render_disclaimer(
        title="Governance Notice",
        message=(
            "Each model below operates independently and produces its own estimate. "
            "No single model represents the final valuation. "
            "Final price is derived via governed ensemble & human review."
        ),
        level="info",
    )

    if not model_outputs:
        st.warning("No model outputs available.")
        return

    # =========================
    # TABLE DATA
    # =========================
    rows: List[Dict[str, Any]] = []

    for model in model_outputs:
        rows.append(
            {
                "Model ID": model.get("model_id"),
                "Type": model.get("model_type"),
                "Version": model.get("version"),
                "Status": render_model_status(model.get("status")),
                "Estimated Price": format_price(model.get("estimated_price")),
                "Notes": model.get("confidence_note"),
                "Limitations": model.get("limitations"),
            }
        )

    # =========================
    # RENDER TABLE
    # =========================
    render_table(
        data=rows,
        columns=[
            "Model ID",
            "Type",
            "Version",
            "Status",
            "Estimated Price",
            "Notes",
            "Limitations",
        ],
        caption=(
            "Independent AVM core model outputs. "
            "Prices shown here are NOT final and MUST NOT be used standalone."
        ),
    )

    # =========================
    # AUDIT FOOTNOTE
    # =========================
    safe_markdown(
        """
**Audit Notes**
- Model prices are *signals*, not conclusions.
- Dispersion across models indicates uncertainty.
- Low agreement MUST trigger higher scrutiny.

_Core principle: No single model is trusted._
        """
    )


"""
📌 AUDIT & LEGAL NOTES
---------------------
- Model Breakdown:
    ✔ Bắt buộc cho minh bạch mô hình
    ✔ Phục vụ kiểm toán & MRM
    ✔ Cho phép phát hiện model drift / bias

Nguyên tắc bất biến:
"Minh bạch mô hình > độ chính xác đơn lẻ."

AI tạo tín hiệu.  
Con người chịu trách nhiệm.
"""
