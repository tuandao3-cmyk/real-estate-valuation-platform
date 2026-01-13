# ui/shared/state/role_state.py
"""
UI ROLE STATE DEFINITION
=======================

⚠️ GOVERNANCE LOCK
- Tuân thủ tuyệt đối:
  - MASTER_SPEC.md
  - IMPLEMENTATION STATUS – PART 1 & PART 2
- File này CHỈ định nghĩa role cho UI layer.
- Role UI ≠ Role nghiệp vụ ≠ Quyền quyết định định giá.

📌 Mục tiêu:
- Chuẩn hóa role để render UI, kiểm soát hiển thị màn hình
- Phục vụ maker–checker–audit simulation
- KHÔNG dùng cho:
    ❌ quyết định giá
    ❌ override logic
    ❌ bypass workflow backend
"""

from enum import Enum
from typing import Set


# =========================
# ROLE ENUM (UI-ONLY)
# =========================

class UIRole(str, Enum):
    """
    Định nghĩa role người dùng trong UI.

    📌 Đây là role hiển thị & điều hướng,
    KHÔNG phải role pháp lý trong hệ thống định giá.
    """

    APPRAISER = "appraiser"
    MANAGER = "manager"
    AUDITOR = "auditor"


# =========================
# ROLE GROUPING (UI ACCESS)
# =========================

# Các role được phép xem valuation detail
ROLE_CAN_VIEW_VALUATION: Set[UIRole] = {
    UIRole.APPRAISER,
    UIRole.MANAGER,
    UIRole.AUDITOR,
}

# Các role được phép thực hiện hành động review / approve UI
# (⚠️ Chỉ là UI action – backend vẫn kiểm soát tuyệt đối)
ROLE_CAN_REVIEW: Set[UIRole] = {
    UIRole.MANAGER,
}

# Các role chỉ được read-only
ROLE_READ_ONLY: Set[UIRole] = {
    UIRole.AUDITOR,
}


# =========================
# HELPER FUNCTIONS (PURE)
# =========================

def is_read_only(role: UIRole) -> bool:
    """
    Kiểm tra role có phải read-only hay không.
    """
    return role in ROLE_READ_ONLY


def can_review(role: UIRole) -> bool:
    """
    Kiểm tra role có quyền review UI hay không.
    📌 Review UI ≠ approve valuation.
    """
    return role in ROLE_CAN_REVIEW


def can_view_valuation(role: UIRole) -> bool:
    """
    Kiểm tra role có được xem valuation hay không.
    """
    return role in ROLE_CAN_VIEW_VALUATION


"""
📌 LEGAL & AUDIT NOTES
---------------------
- Role UI chỉ ảnh hưởng:
    - Hiển thị component
    - Enable / disable nút bấm
- Mọi quyết định định giá, phê duyệt, override:
    → Backend + Human accountability
- Không được serialize role UI vào valuation_dossier.

UI Role = Presentation Constraint Only.
"""
