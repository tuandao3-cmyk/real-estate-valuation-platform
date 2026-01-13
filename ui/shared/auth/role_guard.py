# ui/shared/auth/role_guard.py
"""
ROLE GUARD – UI-LEVEL ACCESS CONTROL (NON-AUTH)
==============================================

🚫 GOVERNANCE LOCK – STRICT COMPLIANCE
Tuân thủ tuyệt đối:
- MASTER_SPEC.md
- IMPLEMENTATION STATUS – PART 1 & PART 2

📌 MỤC ĐÍCH
- Bảo vệ UI component / page theo ROLE
- Phản ánh đúng Maker–Checker–Auditor workflow
- NGĂN truy cập sai vai ở tầng giao diện

📌 NGUYÊN TẮC PHÁP LÝ & KỸ THUẬT
- Đây KHÔNG phải hệ thống phân quyền thật
- KHÔNG thay thế backend authorization
- KHÔNG quyết định nghiệp vụ hay phê duyệt

👉 Role Guard chỉ để:
    ✔ Ẩn / hiện UI
    ✔ Chặn thao tác nhạy cảm trên giao diện
    ✔ Phục vụ audit & UX đúng chuẩn ngân hàng
"""

import streamlit as st
from typing import Iterable, Optional

from ui.shared.state.session_state import get_session_state
from ui.shared.state.role_state import UIRole


# =========================
# CORE ROLE CHECK
# =========================
def get_current_role() -> Optional[str]:
    """
    Return current UI role from session.

    - Read-only
    - No inference
    - No fallback
    """
    return get_session_state()

def has_role(allowed_roles: Iterable[UIRole]) -> bool:
    """
    Kiểm tra role hiện tại có nằm trong danh sách cho phép hay không.

    Parameters
    ----------
    allowed_roles : Iterable[Role]
        Danh sách role được phép truy cập.

    Returns
    -------
    bool
        True nếu role hợp lệ, False nếu không.

    GOVERNANCE
    ----------
    - Không fallback
    - Không suy đoán role
    - Role phải tồn tại rõ ràng trong session
    """

    current_role = get_session_state()

    if current_role is None:
        return False

    return any(current_role == role.value for role in allowed_roles)


# =========================
# UI GUARD RENDER
# =========================

def require_role(
    allowed_roles: Iterable[UIRole],
    message: Optional[str] = None,
) -> bool:
    """
    Guard UI theo role.
    Nếu không đủ quyền → hiển thị cảnh báo & dừng render.

    Parameters
    ----------
    allowed_roles : Iterable[Role]
        Role được phép.
    message : Optional[str]
        Thông báo tuỳ chỉnh.

    Returns
    -------
    bool
        True nếu được phép tiếp tục render, False nếu bị chặn.

    USAGE
    -----
    if not require_role([Role.MANAGER]):
        return
    """

    if has_role(allowed_roles):
        return True

    st.warning(
        message
        or "You do not have permission to access this section."
    )
    return False


# =========================
# STRICT BLOCK (AUDIT-SAFE)
# =========================

def block_if_not_role(
    allowed_roles: Iterable[UIRole],
    message: Optional[str] = None,
) -> None:
    """
    Chặn tuyệt đối UI nếu role không hợp lệ.
    Dùng cho các màn hình nhạy cảm (override, approval).

    GOVERNANCE
    ----------
    - Không cho UI tiếp tục render
    - Phù hợp audit / kiểm soát nội bộ
    """

    if has_role(allowed_roles):
        return

    st.error(
        message
        or "Access denied due to role restriction."
    )
    st.stop()


"""
📌 AUDIT & COMPLIANCE NOTES
--------------------------
- Role Guard:
    ✔ Chỉ hoạt động ở UI
    ✔ Không can thiệp dữ liệu
    ✔ Không ảnh hưởng quyết định định giá

- Nếu UI bị bypass:
    👉 Backend vẫn phải chặn

Nguyên tắc vàng:
"UI phản ánh governance – Backend thực thi governance."

LLM ❌ không quyết role  
UI ❌ không quyết quyền  
Backend ✔ quyết định cuối cùng
"""
