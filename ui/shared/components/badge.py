# ui/shared/components/badge.py
"""
BADGE COMPONENT – GOVERNANCE VISUAL INDICATOR
=============================================

🚫 GOVERNANCE LOCK – DO NOT VIOLATE
- Tuân thủ tuyệt đối:
  - MASTER_SPEC.md
  - IMPLEMENTATION STATUS – PART 1 & PART 2

📌 MỤC ĐÍCH
- Hiển thị nguồn gốc quyết định / nội dung trong UI
- Giúp:
    ✔ Appraiser
    ✔ Manager
    ✔ Auditor
  phân biệt rõ: AI / HUMAN / RULE

📌 TRIẾT LÝ
- Badge chỉ mang tính hiển thị
- KHÔNG ảnh hưởng logic
- KHÔNG suy luận
- KHÔNG trigger hành vi

UI = Transparency, not authority
"""

from enum import Enum

import streamlit as st


class BadgeType(str, Enum):
    """
    Định nghĩa loại badge hợp lệ.

    ❌ Không được tự ý mở rộng nếu không có governance approval
    """
    AI = "AI"
    HUMAN = "HUMAN"
    RULE = "RULE"


# =========================
# STYLE MAP (UI ONLY)
# =========================

_BADGE_STYLE = {
    BadgeType.AI: {
        "label": "AI",
        "color": "#6C8AE4",  # Blue – machine generated
    },
    BadgeType.HUMAN: {
        "label": "HUMAN",
        "color": "#2E8B57",  # Green – human judgment
    },
    BadgeType.RULE: {
        "label": "RULE",
        "color": "#8B0000",  # Dark red – governance / policy
    },
}


# =========================
# RENDER FUNCTION
# =========================

def render_badge(badge_type: BadgeType) -> None:
    """
    Render badge trong UI.

    📌 LƯU Ý GOVERNANCE
    - Badge chỉ phản ánh NGUỒN
    - Không phản ánh độ tin cậy
    - Không phản ánh quyết định cuối

    Ví dụ:
    - Giá từ model → AI
    - Override → HUMAN
    - Approval gate → RULE
    """

    if badge_type not in _BADGE_STYLE:
        # Failsafe: không render nếu badge không hợp lệ
        return

    style = _BADGE_STYLE[badge_type]

    st.markdown(
        f"""
        <span style="
            display: inline-block;
            padding: 4px 10px;
            margin-right: 6px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
            color: white;
            background-color: {style['color']};
        ">
            {style['label']}
        </span>
        """,
        unsafe_allow_html=True,
    )


"""
📌 AUDIT NOTE
-------------
- Badge là yêu cầu BẮT BUỘC cho:
    ✔ Giá trị hiển thị
    ✔ Quyết định
    ✔ Override
    ✔ Rule enforcement

- Auditor phải nhìn UI và trả lời được:
    "Cái này do AI, con người hay rule sinh ra?"

Nếu không trả lời được → UI NON-COMPLIANT.
"""
