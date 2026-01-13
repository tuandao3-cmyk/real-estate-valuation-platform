# ui/shared/components/model_status.py
"""
MODEL STATUS INDICATOR – GOVERNANCE UI COMPONENT
================================================

🚫 GOVERNANCE LOCK – DO NOT VIOLATE
- Tuân thủ tuyệt đối:
  - MASTER_SPEC.md
  - IMPLEMENTATION STATUS – PART 1 & PART 2

📌 MỤC ĐÍCH
- Hiển thị trạng thái model / artifact trong UI
- Phục vụ:
    ✔ Appraiser
    ✔ Manager
    ✔ Auditor

📌 NGUYÊN TẮC CỐT LÕI
- CHỈ hiển thị trạng thái đã được xác định từ backend / dossier
- KHÔNG suy luận
- KHÔNG đánh giá
- KHÔNG thay đổi workflow
- KHÔNG trigger hành vi

UI = Mirror, not Judge
"""

from enum import Enum

import streamlit as st


class ModelStatus(str, Enum):
    """
    Trạng thái model / artifact hợp lệ.

    ❌ Không tự ý mở rộng nếu không có governance approval
    """
    OK = "OK"            # ✅
    WARNING = "WARNING"  # ⚠️
    ERROR = "ERROR"      # ❌


# =========================
# STATUS CONFIG (UI ONLY)
# =========================

_STATUS_STYLE = {
    ModelStatus.OK: {
        "icon": "✅",
        "label": "OK",
        "color": "#2E8B57",  # Green
    },
    ModelStatus.WARNING: {
        "icon": "⚠️",
        "label": "WARNING",
        "color": "#DAA520",  # Gold
    },
    ModelStatus.ERROR: {
        "icon": "❌",
        "label": "ERROR",
        "color": "#8B0000",  # Dark Red
    },
}


# =========================
# RENDER FUNCTION
# =========================

def render_model_status(status: ModelStatus, description: str | None = None) -> None:
    """
    Render trạng thái model / artifact.

    Parameters
    ----------
    status : ModelStatus
        Trạng thái đã được backend / dossier xác định.
    description : Optional[str]
        Mô tả ngắn (read-only, human-readable).

    📌 GOVERNANCE NOTE
    - Status ≠ Approval
    - Status ≠ Trust
    - Status ≠ Decision
    """

    if status not in _STATUS_STYLE:
        # Failsafe: không render nếu trạng thái không hợp lệ
        return

    cfg = _STATUS_STYLE[status]

    tooltip = f"title='{description}'" if description else ""

    st.markdown(
        f"""
        <span {tooltip} style="
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 10px;
            border-radius: 14px;
            font-size: 13px;
            font-weight: 600;
            color: white;
            background-color: {cfg['color']};
        ">
            <span>{cfg['icon']}</span>
            <span>{cfg['label']}</span>
        </span>
        """,
        unsafe_allow_html=True,
    )


"""
📌 AUDIT & COMPLIANCE NOTE
-------------------------
- Component này PHẢI dùng cho:
    ✔ Model output status
    ✔ Feature pipeline status
    ✔ Verification / signal status
    ✔ Registry / activation status

- Nếu UI hiển thị trạng thái mà không dùng component này
  → UI NON-COMPLIANT

Auditor có thể hỏi:
"⚠️ này từ đâu ra?"
→ Câu trả lời PHẢI nằm ở valuation_dossier / trace.

UI chỉ phản chiếu – không được phán xét.
"""
