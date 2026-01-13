# ui/shared/api_client/valuation_api.py
"""
VALUATION API CLIENT – UI LAYER ONLY
===================================

🚫 GOVERNANCE LOCK – DO NOT VIOLATE
- Tuân thủ tuyệt đối:
  - MASTER_SPEC.md
  - IMPLEMENTATION STATUS – PART 1 & PART 2

📌 MỤC ĐÍCH
- File này CHỈ làm nhiệm vụ:
    ✔ Gọi API backend
    ✔ Truyền request
    ✔ Nhận response thô

⛔ TUYỆT ĐỐI KHÔNG ĐƯỢC
- ❌ Xử lý nghiệp vụ
- ❌ Suy luận kết quả
- ❌ Diễn giải dữ liệu
- ❌ Gộp / chỉnh sửa output
- ❌ Fallback logic

UI ≠ Decision
UI ≠ Model
UI ≠ Rule Engine
"""

from typing import Any, Dict, Optional

import requests


# =========================
# CONFIGURATION
# =========================

DEFAULT_TIMEOUT_SECONDS = 30


class ValuationAPIClient:
    """
    Thin HTTP client cho Valuation Backend.

    📌 Vai trò:
    - UI → Backend bridge
    - Stateless
    - Deterministic

    📌 Không cache
    📌 Không retry
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

    def predict(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call /predict

        📌 Backend chịu trách nhiệm:
        - Validation
        - Model execution
        - Rule enforcement
        - Governance

        UI chỉ truyền payload và nhận kết quả.
        """
        return self._post("/predict", payload)

    def get_dossier(self, valuation_id: str) -> Dict[str, Any]:
        """
        Call /get_dossier

        📌 Trả về:
        - valuation_dossier.json (snapshot)
        - Single Source of Truth

        UI không được chỉnh sửa nội dung dossier.
        """
        return self._get(
            "/get_dossier",
            params={"valuation_id": valuation_id},
        )


"""
📌 AUDIT NOTE
-------------
- Mọi API call từ UI PHẢI đi qua client này.
- Không được:
    ❌ Gọi requests trực tiếp ở page / component
    ❌ Hardcode endpoint ở UI logic
    ❌ Inject fallback khi API lỗi

Nếu cần xử lý lỗi:
→ Thực hiện ở layer hiển thị (message only)
→ Không được thay đổi dữ liệu trả về

UI = transport + presentation
Backend = logic + decision
"""
