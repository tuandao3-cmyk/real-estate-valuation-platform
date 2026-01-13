# ui/shared/components/risk_indicator.py
"""
RISK INDICATOR – DESCRIPTIVE GOVERNANCE UI COMPONENT
===================================================

🚫 GOVERNANCE LOCK – STRICT COMPLIANCE
- Tuân thủ tuyệt đối:
  - MASTER_SPEC.md
  - IMPLEMENTATION STATUS – PART 1 & PART 2

📌 MỤC ĐÍCH
- Hiển thị tín hiệu rủi ro (risk indicator) cho valuation workflow
- Phục vụ nhận biết, KHÔNG phán xét

📌 NGUYÊN TẮC BẤT DI BẤT DỊCH
- Risk Indicator ≠ Risk Decision
- Risk Indicator ≠ Approval / Rejection
- Risk Indicator ≠ Giá trị tài sản

📌 NGÔN NGỮ HIỂN THỊ
- Trung lập
- Mô tả
- Audit-safe
"""

import streamlit as st
from enum import Enum
from typing import Optional


# =========================
# RISK LEVEL DEFINITION
# =========================

class RiskLevel(str, Enum):
    """
    Risk level chuẩn hóa cho UI.
    ❌ Không suy luận
    ❌ Không gán threshold tại UI
    """
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    UNKNOWN = "UNKNOWN"


# =========================
# VISUAL CONFIGURATION
# =========================

_RISK_VISUAL = {
    RiskLevel.LOW: {
        "icon": "🟢",
        "label": "Low Risk Signal",
        "color": "#2ca02c",
        "description": (
            "Không phát hiện tín hiệu rủi ro đáng chú ý "
            "theo các kiểm tra hiện có."
        ),
    },
    RiskLevel.MEDIUM: {
        "icon": "🟡",
        "label": "Medium Risk Signal",
        "color": "#ffbf00",
        "description": (
            "Tồn tại một số tín hiệu cần được xem xét thêm "
            "trong quá trình thẩm định."
        ),
    },
    RiskLevel.HIGH: {
        "icon": "🔴",
        "label": "High Risk Signal",
        "color": "#d62728",
        "description": (
            "Phát hiện tín hiệu rủi ro cao "
            "yêu cầu human review bắt buộc."
        ),
    },
    RiskLevel.UNKNOWN: {
        "icon": "⚪",
        "label": "Risk Signal Not Available",
        "color": "#7f7f7f",
        "description": (
            "Không đủ dữ liệu hoặc không áp dụng đánh giá rủi ro "
            "cho trường hợp này."
        ),
    },
}


# =========================
# RENDER FUNCTION
# =========================

def render_risk_indicator(
    risk_level: Optional[str],
    context_note: Optional[str] = None,
) -> None:
    """
    Render risk indicator cho UI.

    Parameters
    ----------
    risk_level : str | None
        Giá trị risk level do backend / rule engine cung cấp
        (LOW / MEDIUM / HIGH / UNKNOWN)

    context_note : str | None
        Ghi chú bổ sung mang tính mô tả (tùy chọn).
        ❌ Không được mang tính chỉ đạo.

    GOVERNANCE NOTES
    ----------------
    - UI không tính risk
    - UI không nâng cấp / hạ cấp risk
    - UI không trigger workflow
    """

    try:
        level = RiskLevel(risk_level) if risk_level else RiskLevel.UNKNOWN
    except ValueError:
        level = RiskLevel.UNKNOWN

    cfg = _RISK_VISUAL[level]

    st.subheader("Risk Indicator (Descriptive)")

    st.markdown(
        f"""
        <div style="
            border-left: 6px solid {cfg['color']};
            padding: 0.5em 1em;
            margin: 0.5em 0;
            background-color: #f9f9f9;
        ">
            <strong>{cfg['icon']} {cfg['label']}</strong><br/>
            <span style="font-size: 0.9em;">
                {cfg['description']}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if context_note:
        st.markdown(
            f"""
            <div style="font-size: 0.85em; color: #555;">
            <em>Context note:</em> {context_note}
            </div>
            """,
            unsafe_allow_html=True,
        )


"""
📌 AUDIT & LEGAL NOTES
---------------------
- Component này:
    ✔ Chỉ hiển thị tín hiệu rủi ro
    ✔ Không gắn với quyết định giá
    ✔ Không thay thế judgement con người

- Component này KHÔNG ĐƯỢC:
    ❌ dùng để auto-approve / reject
    ❌ ánh xạ trực tiếp sang hành động workflow
    ❌ diễn giải rủi ro thành “nên / không nên định giá”

Nguyên tắc pháp lý:
"Risk để nhận biết – không để kết luận."

Human review luôn là tuyến cuối.
"""
