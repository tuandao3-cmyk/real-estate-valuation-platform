# ui/shared/api_client/governance_api.py
"""
GOVERNANCE API CLIENT – UI TRANSPORT LAYER ONLY
==============================================

🚫 GOVERNANCE LOCK – DO NOT VIOLATE
- Tuân thủ tuyệt đối:
  - MASTER_SPEC.md
  - IMPLEMENTATION STATUS – PART 1 & PART 2

📌 MỤC ĐÍCH
- Client API THUẦN cho Governance / Policy layer
- UI chỉ được phép:
    ✔ Gửi request
    ✔ Nhận response thô
    ✔ Hiển thị theo đúng snapshot

⛔ TUYỆT ĐỐI CẤM
- ❌ Diễn giải rule
- ❌ Áp dụng policy ở UI
- ❌ Suy luận approval
- ❌ Bypass governance backend

Governance = Law
UI = Messenger
"""

from typing import Any, Dict, Optional

import requests


# =========================
# CONFIGURATION
# =========================

DEFAULT_TIMEOUT_SECONDS = 30


class GovernanceAPIClient:
    """
    Thin HTTP client cho Governance Backend.

    📌 Stateless
    📌 Deterministic
    📌 No cache
    📌 No retry
    """

    def __init__(self, base_url: str, api_key: Optional[str] = None) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    # =========================
    # INTERNAL HELPERS
    # =========================

    def _headers(self) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        response = requests.get(
            url,
            params=params,
            headers=self._headers(),
            timeout=DEFAULT_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        return response.json()

    def _post(
        self,
        path: str,
        payload: Dict[str, Any],
    ) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        response = requests.post(
            url,
            json=payload,
            headers=self._headers(),
            timeout=DEFAULT_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        return response.json()

    # =========================
    # PUBLIC GOVERNANCE ENDPOINTS
    # =========================

    def get_feature_flags(self) -> Dict[str, Any]:
        """
        Call /governance/feature_flags

        📌 Trả về:
        - Feature flag snapshot
        - Role-based UI control
        - Governance-driven

        UI chỉ đọc – không override.
        """
        return self._get("/governance/feature_flags")

    def get_role_permissions(self, role: str) -> Dict[str, Any]:
        """
        Call /governance/role_permissions

        📌 Trả về:
        - Allowed actions theo role
        - Immutable snapshot cho audit
        """
        return self._get(
            "/governance/role_permissions",
            params={"role": role},
        )

    def submit_override_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call /governance/override_request

        📌 Dùng cho:
        - Gửi yêu cầu override (UI action)
        - Backend quyết định accept / reject

        UI KHÔNG được:
        - Tự approve
        - Tự bypass rule
        """
        return self._post("/governance/override_request", payload)


"""
📌 AUDIT & GOVERNANCE NOTE
-------------------------
- Governance logic tồn tại DUY NHẤT ở backend.
- UI chỉ là:
    ✔ Transport
    ✔ Viewer
    ✔ Action submitter

- Nếu UI:
    ❌ Hardcode rule
    ❌ Enable override trái phép
    ❌ Quyết định thay governance

→ VALUATION INVALID (MASTER_SPEC §11)

Governance không để “thuận tiện”,
Governance để bảo vệ hệ thống.
"""
