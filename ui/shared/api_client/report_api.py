# ui/shared/api_client/report_api.py
"""
REPORT API CLIENT – UI LAYER ONLY
================================

🚫 GOVERNANCE LOCK – DO NOT VIOLATE
- Tuân thủ tuyệt đối:
  - MASTER_SPEC.md
  - IMPLEMENTATION STATUS – PART 1 & PART 2

📌 MỤC ĐÍCH
- Client API thuần cho Report / Explanation layer
- UI chỉ làm nhiệm vụ:
    ✔ Gửi request
    ✔ Nhận response
    ✔ Không can thiệp nội dung

📌 VAI TRÒ THEO MASTER_SPEC
- Report = hậu xử lý trình bày
- Không ảnh hưởng:
    ❌ Giá trị
    ❌ Quyết định
    ❌ Confidence
"""

from typing import Any, Dict, Optional

import requests


# =========================
# CONFIGURATION
# =========================

DEFAULT_TIMEOUT_SECONDS = 30


class ReportAPIClient:
    """
    Thin HTTP client cho Report / Explanation Backend.

    📌 Stateless
    📌 No retry
    📌 No cache
    """

    def __init__(self, base_url: str, api_key: Optional[str] = None) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    # =========================
    # INTERNAL
    # =========================

    def _headers(self) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        response = requests.post(
            url,
            json=payload,
            headers=self._headers(),
            timeout=DEFAULT_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        return response.json()

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        response = requests.get(
            url,
            params=params,
            headers=self._headers(),
            timeout=DEFAULT_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        return response.json()

    # =========================
    # PUBLIC API METHODS
    # =========================

    def generate_report(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call /generate_report

        📌 Backend chịu trách nhiệm:
        - Assemble report
        - LLM explanation (nếu có)
        - Governance & audit compliance

        UI chỉ truyền payload.
        """
        return self._post("/generate_report", payload)

    def get_report(self, report_id: str) -> Dict[str, Any]:
        """
        Call /get_report

        📌 Trả về:
        - Nội dung report đã snapshot
        - Immutable cho audit

        UI không chỉnh sửa nội dung.
        """
        return self._get(
            "/get_report",
            params={"report_id": report_id},
        )


"""
📌 AUDIT NOTE
-------------
- UI KHÔNG được:
    ❌ Tự sinh report
    ❌ Sửa text report
    ❌ Tự gọi LLM

- Mọi report hiển thị:
    → Backend sinh
    → UI render qua safe_render.py

Report = trình bày
Decision = con người
AI = hỗ trợ, không kết luận
"""
