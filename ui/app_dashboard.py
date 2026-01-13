"""
ui/app_dashboard.py

ROLE
----
System landing dashboard after authentication.

LEGAL & GOVERNANCE POSITIONING
------------------------------
- Orientation page, not an operational page
- Explains system boundaries, roles, and responsibilities
- No valuation, no approval, no override actions

COMPLIANCE
----------
✔ MASTER_SPEC.md
✔ IMPLEMENTATION STATUS PHẦN 1
✔ IMPLEMENTATION STATUS PHẦN 2
"""

import streamlit as st

# from ui.shared.auth.role_guard import require_role
from ui.shared.components.disclaimer_box import render_disclaimer_box
from ui.shared.components.badge import BadgeType, render_badge
from ui.shared.components.approval_timeline import render_approval_timeline
from ui.shared.utils.safe_render import render_safe_markdown
from ui.shared.auth.role_guard import get_current_role




# =========================
# DASHBOARD VIEW
# =========================

def app_dashboard_view():
    """
    Render system dashboard based on current user role.

    GUARANTEES
    ----------
    - Read-only informational UI
    - Role-aware messaging
    - No system state mutation
    """

    role = get_current_role()

    if role is None:
        st.error("No role assigned in session.")
        st.stop()

    st.title("📊 Hệ thống định giá – Tổng quan")

    render_disclaimer_box()

    _render_role_context(role)
    _render_system_positioning()
    _render_process_overview()
    _render_next_steps(role)


# =========================
# SECTION RENDERERS
# =========================

def _render_role_context(role: str):
    """Explain current user role and responsibility."""

    st.subheader("👤 Vai trò hiện tại")

    render_badge(BadgeType.HUMAN)

    role_descriptions = {
        "APPRAISER": (
            "Bạn chịu trách nhiệm **nhập hồ sơ**, "
            "xem kết quả định giá mang tính **tham khảo**, "
            "và **không có quyền phê duyệt**."
        ),
        "MANAGER": (
            "Bạn chịu trách nhiệm **xem xét**, "
            "**phê duyệt hoặc override** dựa trên "
            "quy trình và trách nhiệm pháp lý."
        ),
        "AUDITOR": (
            "Bạn có quyền **xem toàn bộ dấu vết**, "
            "log, provenance và khả năng tái lập. "
            "**Không can thiệp quy trình**."
        ),
        "GOVERNANCE": (
            "Bạn chịu trách nhiệm **định nghĩa ranh giới**, "
            "policy và khung pháp lý cho hệ thống."
        ),
    }

    render_safe_markdown(f"""
**Role:** `{role}`  

{role_descriptions.get(role, "Vai trò không xác định.")}
""")


def _render_system_positioning():
    """Explain what the system is and is not."""

    st.subheader("🏛️ Định vị hệ thống")

    render_safe_markdown("""
Hệ thống này là **Decision Support System**, không phải:

- ❌ Công cụ định giá tự động
- ❌ Công cụ phê duyệt
- ❌ Công cụ thay thế con người

AI, Rule và Model chỉ cung cấp **tín hiệu mô tả**,  
**trách nhiệm cuối cùng luôn thuộc về con người**.
""")


def _render_process_overview():
    """
    High-level workflow visualization.
    UI DEMO ONLY – no system state, no decision.
    """

    st.subheader("🔁 Quy trình tổng thể")

    demo_events = [
        {
            "timestamp": "—",
            "actor_type": "AI",
            "actor_id": "system",
            "action": "MODEL_ANALYSIS",
            "description": "Mô hình AI sinh tín hiệu định giá tham khảo"
        },
        {
            "timestamp": "—",
            "actor_type": "RULE",
            "actor_id": "policy_engine",
            "action": "POLICY_CHECK",
            "description": "Áp dụng rule, kiểm soát rủi ro và phạm vi pháp lý"
        },
        {
            "timestamp": "—",
            "actor_type": "HUMAN",
            "actor_id": "valuer",
            "action": "FINAL_REVIEW",
            "description": "Thẩm định viên xem xét và chịu trách nhiệm cuối"
        },
    ]

    render_approval_timeline(demo_events)

    render_safe_markdown("""
Quy trình được thiết kế theo mô hình **maker – checker – auditor**:

- **AI**: tạo tín hiệu (không quyết định)  
- **Rule**: kiểm soát & ràng buộc  
- **Human**: quyết định và chịu trách nhiệm pháp lý
""")



def _render_next_steps(role: str):
    """Guide user to appropriate next actions (navigation hint only)."""

    st.subheader("➡️ Bước tiếp theo")

    if role == "APPRAISER":
        render_safe_markdown("""
- Truy cập **Định giá → Hàng chờ định giá**
- Nhập hồ sơ và gửi yêu cầu
""")
    elif role == "MANAGER":
        render_safe_markdown("""
- Truy cập **Phê duyệt → Hàng chờ phê duyệt**
- Xem xét kết quả và thực hiện quyết định
""")
    elif role == "AUDITOR":
        render_safe_markdown("""
- Truy cập **Kiểm toán**
- Xem trace, provenance và reproducibility
""")
    elif role == "GOVERNANCE":
        render_safe_markdown("""
- Truy cập **Governance**
- Rà soát decision boundary và policy
""")
    else:
        render_safe_markdown("Không có hành động được đề xuất cho vai trò này.")
app_dashboard_view()