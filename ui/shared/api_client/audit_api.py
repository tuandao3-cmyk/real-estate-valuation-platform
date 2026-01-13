# ui/shared/api_client/audit_api.py
"""
AUDIT API CLIENT – UI TRANSPORT LAYER ONLY
=========================================

🚫 GOVERNANCE LOCK – DO NOT VIOLATE
- Tuân thủ tuyệt đối:
  - MASTER_SPEC.md
  - IMPLEMENTATION STATUS – PART 1 & PART 2

📌 MỤC ĐÍCH
- Client API THUẦN cho Audit / Compliance layer
- UI chỉ được phép:
    ✔ Gửi request
    ✔ Nhận response
    ✔ Hiển thị nguyên trạng

⛔ TUYỆT ĐỐI KHÔNG
- ❌ Xử lý nghiệp vụ audit
- ❌ Suy luận rủi ro
- ❌ Diễn giải log
- ❌ Sửa / gộp / lọc dữ liệu audit

Audit = Evidence
UI = Viewer
"""

from typing import Any, Dict, Optional

import requests


# =========================
# CONFIGURATION
# =========================

DEFAULT_TIMEOUT_SECONDS = 30


class AuditAPIClient:
    """
    Thin HTTP client cho Audit Backend.

    📌 Stateless
    📌 Deterministic
    📌 Không cache
    📌 Không retry
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
    # PUBLIC AUDIT ENDPOINTS
    # =========================

    def get_audit_trail(self, valuation_id: str) -> Dict[str, Any]:
        """
        Call /audit/trail

        📌 Trả về:
        - Full audit trail cho một valuation
        - Immutable
        - Court-defensible

        UI chỉ được hiển thị.
        """
        return self._get(
            "/audit/trail",
            params={"valuation_id": valuation_id},
        )

    def get_override_log(self, valuation_id: str) -> Dict[str, Any]:
        """
        Call /audit/override_log

        📌 Trả về:
        - Override history
        - Reason codes
        - Actor + timestamp

        UI không được suy diễn ý nghĩa.
        """
        return self._get(
            "/audit/override_log",
            params={"valuation_id": valuation_id},
        )

    def submit_audit_comment(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call /audit/comment

        📌 Dùng cho:
        - Auditor note
        - Review comment
        - Compliance remark

        Backend chịu trách nhiệm validate & persist.
        """
        return self._post("/audit/comment", payload)


"""
📌 AUDIT & COMPLIANCE NOTE
-------------------------
- Mọi dữ liệu audit:
    ✔ Sinh ở backend
    ✔ Snapshot
    ✔ Không được UI chỉnh sửa

- UI hiển thị audit:
    → BẮT BUỘC render qua safe_render.py

- Nếu UI:
    ❌ Lọc audit log
    ❌ Tóm tắt audit log
    ❌ Tự kết luận từ audit log

→ SYSTEM NON-COMPLIANT

Audit tồn tại để chứng minh,
không tồn tại để thuyết phục.
"""
