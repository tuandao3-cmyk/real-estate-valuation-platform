# ui/shared/state/session_state.py
"""
CORE STREAMLIT SESSION STATE
============================

⚠️ GOVERNANCE NOTICE
- File này là SINGLE SOURCE OF TRUTH cho session-level state trong UI.
- TUÂN THỦ TUYỆT ĐỐI:
  - MASTER_SPEC.md
  - IMPLEMENTATION STATUS – PART 1 & PART 2

📌 UI chỉ là mô phỏng quy trình thẩm định thật.
📌 Session state ≠ business logic ≠ decision logic.
📌 File này KHÔNG:
    ❌ suy luận
    ❌ validate nghiệp vụ
    ❌ điều hướng quyết định
    ❌ thay đổi valuation outcome

Mọi file UI khác BẮT BUỘC import và dùng state từ đây.
"""

from dataclasses import dataclass
from typing import Optional, Literal
import streamlit as st


# =========================
# ROLE DEFINITION (UI-ONLY)
# =========================

# UserRole = Literal[
#     "appraiser",        # Người thẩm định
#     "reviewer",         # Checker / Manager
#     "admin",            # Quản trị hệ thống
#     "viewer"            # Read-only (audit / training)
# ]

UserRole = Literal[
    "APPRAISER",
    "MANAGER",
    "AUDITOR",
]

# =========================
# SESSION STATE SCHEMA
# =========================

@dataclass(frozen=True)
class UISessionState:
    """
    Immutable view of UI session state.
    Không chứa logic – chỉ chứa dữ liệu hiện tại.
    """

    user: Optional[str]
    role: Optional[UserRole]
    selected_valuation_id: Optional[str]
    navigation: Optional[str]


# =========================
# INTERNAL KEYS (LOCKED)
# =========================

_STATE_KEYS = {
    "user": "ui_user",
    "role": "ui_role",
    "selected_valuation_id": "ui_selected_valuation_id",
    "navigation": "ui_navigation",
}


# =========================
# INITIALIZATION
# =========================

def initialize_session_state() -> None:
    """
    Khởi tạo session state với giá trị None.
    ❌ Không gán mặc định nghiệp vụ
    ❌ Không auto-login
    ❌ Không auto-navigation
    """
    for key in _STATE_KEYS.values():
        if key not in st.session_state:
            st.session_state[key] = None


# =========================
# READ-ONLY ACCESSOR
# =========================

def get_session_state() -> UISessionState:
    """
    Trả về snapshot immutable của session state hiện tại.
    UI layer chỉ được READ, không mutate trực tiếp.
    """
    return UISessionState(
        user=st.session_state.get(_STATE_KEYS["user"]),
        role=st.session_state.get(_STATE_KEYS["role"]),
        selected_valuation_id=st.session_state.get(
            _STATE_KEYS["selected_valuation_id"]
        ),
        navigation=st.session_state.get(_STATE_KEYS["navigation"]),
    )


# =========================
# EXPLICIT SETTERS (UI-ONLY)
# =========================

def set_user(user: str, role: UserRole) -> None:
    """
    Gán thông tin user & role.
    📌 Role ở đây CHỈ phục vụ UI rendering & access gate.
    ❌ Không dùng cho quyết định nghiệp vụ.
    """
    st.session_state[_STATE_KEYS["user"]] = user
    st.session_state[_STATE_KEYS["role"]] = role


def clear_user() -> None:
    """
    Clear user session (logout).
    """
    st.session_state[_STATE_KEYS["user"]] = None
    st.session_state[_STATE_KEYS["role"]] = None
    st.session_state[_STATE_KEYS["selected_valuation_id"]] = None
    st.session_state[_STATE_KEYS["navigation"]] = None


def set_selected_valuation(valuation_id: Optional[str]) -> None:
    """
    Gán valuation đang được xem.
    ❌ Không load data
    ❌ Không trigger workflow
    """
    st.session_state[_STATE_KEYS["selected_valuation_id"]] = valuation_id


def set_navigation(view_name: Optional[str]) -> None:
    """
    Điều hướng UI (page / tab).
    📌 Navigation ≠ workflow step.
    """
    st.session_state[_STATE_KEYS["navigation"]] = view_name


# =========================
# GOVERNANCE GUARD (UI)
# =========================

def assert_session_initialized() -> None:
    """
    Hard guard: đảm bảo session_state đã được init.
    Dùng ở entry point UI (app.py).
    """
    missing = [
        key for key in _STATE_KEYS.values()
        if key not in st.session_state
    ]
    if missing:
        raise RuntimeError(
            f"UI Session State not initialized. Missing keys: {missing}"
        )


"""
📌 LEGAL & AUDIT NOTES
---------------------
- Session state tồn tại trong memory UI session → không phải record pháp lý.
- KHÔNG log session state vào audit trail.
- KHÔNG dùng session state để suy luận hành vi người dùng.
- Mọi quyết định định giá PHẢI dựa trên valuation_dossier & backend workflow.

UI State = Presentation Context Only.
"""
