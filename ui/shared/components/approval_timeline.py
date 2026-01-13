# ui/shared/components/approval_timeline.py
"""
APPROVAL TIMELINE – WORKFLOW TRACE UI COMPONENT
===============================================

🚫 GOVERNANCE LOCK – STRICT COMPLIANCE
- Tuân thủ tuyệt đối:
  - MASTER_SPEC.md
  - IMPLEMENTATION STATUS – PART 1 & PART 2

📌 MỤC ĐÍCH
- Hiển thị timeline các bước trong valuation / approval workflow
- Phục vụ:
    ✔ Minh bạch quy trình
    ✔ Audit & traceability
    ✔ Phân tách rõ AI / Rule / Human action

📌 NGUYÊN TẮC BẤT DI BẤT DỊCH
- Timeline ≠ Recommendation
- Timeline ≠ Approval decision
- Timeline ≠ Workflow control

📌 UI CHỈ HIỂN THỊ
- Không trigger
- Không thay đổi trạng thái
- Không suy luận bước tiếp theo
"""

import streamlit as st
from typing import List, Dict


# =========================
# EXPECTED EVENT SCHEMA
# =========================
# Mỗi event là dữ liệu ĐÃ ĐƯỢC backend / audit log xác nhận
#
# {
#   "timestamp": "2025-01-01T10:15:00Z",
#   "actor_type": "AI" | "RULE" | "HUMAN",
#   "actor_id": "system" | "user_id",
#   "action": "MODEL_RUN" | "RULE_CHECK" | "HUMAN_OVERRIDE" | ...
#   "description": "Mô tả trung lập"
# }
#
# ❌ UI không diễn giải logic
# ❌ UI không suy luận thiếu event


# =========================
# VISUAL CONFIG
# =========================

_ACTOR_BADGE = {
    "AI": "🤖 AI",
    "RULE": "📜 RULE",
    "HUMAN": "👤 HUMAN",
}


# =========================
# RENDER FUNCTION
# =========================

def render_approval_timeline(events: List[Dict]) -> None:
    """
    Render approval / workflow timeline.

    Parameters
    ----------
    events : List[Dict]
        Danh sách event theo thứ tự thời gian (đã được sort từ backend).

    GOVERNANCE NOTES
    ----------------
    - UI không reorder event
    - UI không fill missing step
    - UI không gán ý nghĩa quyết định
    """

    st.subheader("Approval & Workflow Timeline")

    if not events:
        st.info("No workflow events recorded for this valuation.")
        return

    for idx, event in enumerate(events):
        timestamp = event.get("timestamp", "N/A")
        actor_type = event.get("actor_type", "UNKNOWN")
        actor_label = _ACTOR_BADGE.get(actor_type, "❔ UNKNOWN")
        action = event.get("action", "UNSPECIFIED_ACTION")
        description = event.get("description", "")

        st.markdown(
            f"""
            <div style="
                border-left: 4px solid #cccccc;
                padding: 0.5em 1em;
                margin-bottom: 0.75em;
                background-color: #fafafa;
            ">
                <div style="font-size: 0.85em; color: #666;">
                    {timestamp}
                </div>
                <div style="margin-top: 0.25em;">
                    <strong>{actor_label}</strong>
                    <span style="color:#999;">|</span>
                    <code>{action}</code>
                </div>
                <div style="font-size: 0.9em; margin-top: 0.25em;">
                    {description}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


"""
📌 AUDIT & LEGAL NOTES
---------------------
- Component này:
    ✔ Hiển thị chuỗi hành động đã xảy ra
    ✔ Phân biệt rõ AI / RULE / HUMAN
    ✔ Phục vụ audit trail & court defense

- Component này KHÔNG ĐƯỢC:
    ❌ dùng để suy luận trạng thái hiện tại
    ❌ gợi ý bước tiếp theo
    ❌ đánh giá đúng / sai của hành động

Nguyên tắc pháp lý:
"Timeline ghi nhận sự kiện – không diễn giải trách nhiệm."

Trách nhiệm cuối:
- AI: tạo tín hiệu
- Rule: enforce chính sách
- Human: chịu trách nhiệm quyết định
"""
