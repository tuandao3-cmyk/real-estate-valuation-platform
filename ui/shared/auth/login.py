# ui/shared/auth/login.py
"""
LOGIN UI – GOVERNANCE-SAFE AUTH ENTRY
====================================

🚫 GOVERNANCE LOCK – STRICT COMPLIANCE
Tuân thủ tuyệt đối:
- MASTER_SPEC.md
- IMPLEMENTATION STATUS – PART 1 & PART 2

📌 MỤC ĐÍCH
- Cung cấp giao diện đăng nhập cho người dùng UI
- Thiết lập session cơ bản:
    ✔ user
    ✔ role

📌 NGUYÊN TẮC CỐT LÕI
- UI chỉ thu thập thông tin
- KHÔNG:
    ❌ xác thực bảo mật thật
    ❌ sinh token
    ❌ kiểm tra quyền nghiệp vụ
    ❌ gọi DB trực tiếp

👉 Xác thực THẬT phải nằm ở backend / gateway.
File này chỉ là ENTRY VIEW cho Streamlit.
"""

import streamlit as st
from typing import Optional

from ui.shared.state.session_state import (
    set_user,
    
)
from ui.shared.state.role_state import UIRole


# =========================
# LOGIN FORM
# =========================

def render_login() -> Optional[str]:
    """
    Render form đăng nhập UI.

    Returns
    -------
    Optional[str]
        username nếu login thành công, None nếu chưa.

    GOVERNANCE
    ----------
    - Không validate mật khẩu
    - Không suy luận role
    - Role phải được chọn rõ ràng
    """

    st.title("🔐 Login")

    with st.form("login_form"):
        username = st.text_input(
            "Username",
            placeholder="Enter your username",
        )

        role = st.selectbox(
            "Role",
            options=[
                UIRole.APPRAISER.value,
                UIRole.MANAGER.value,
                UIRole.AUDITOR.value,
            ],
            help="Role is assigned externally. UI does not decide permissions.",
        )

        submitted = st.form_submit_button("Login")

    if not submitted:
        return None

    if not username:
        st.warning("Username is required.")
        return None

    # =========================
    # SESSION STATE SETUP
    # =========================
    # 🚫 UI chỉ set state – không auth logic

    set_user(
    user=username,
    role=role,   # role string từ selectbox
)

    st.success("Login successful.")
    return username


# =========================
# LOGOUT
# =========================

def logout() -> None:
    """
    Clear session login state.

    GOVERNANCE
    ----------
    - Chỉ xoá session UI
    - Không revoke token
    - Không ghi audit
    """

    for key in ["user", "role"]:
        if key in st.session_state:
            del st.session_state[key]

    st.info("Logged out.")


"""
📌 AUDIT & LEGAL NOTES
---------------------
- Login UI này:
    ✔ Phục vụ demo / internal tool
    ✔ Phân vai rõ ràng cho review
    ✔ Không mang tính xác thực pháp lý

- KHÔNG ĐƯỢC:
    ❌ dùng làm hệ thống login sản xuất
    ❌ dựa vào để phân quyền backend
    ❌ thay thế IAM / SSO

Nguyên tắc pháp lý:
"UI nhận vai – Backend quyết quyền."

Human chọn vai.  
System ghi nhận.
"""
