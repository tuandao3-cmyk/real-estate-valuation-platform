# ui/shared/utils/format_date.py
"""
DATE FORMATTING UTILITY – UI ONLY
================================

⚠️ GOVERNANCE LOCK
- Tuân thủ tuyệt đối:
  - MASTER_SPEC.md
  - IMPLEMENTATION STATUS – PART 1 & PART 2

📌 VAI TRÒ
- Format ngày / thời gian để HIỂN THỊ UI
- Không tham gia logic nghiệp vụ
- Không ảnh hưởng audit / valuation

⛔ CẤM TUYỆT ĐỐI
- ❌ So sánh thời gian
- ❌ Tính toán ngày (delta, aging, SLA…)
- ❌ Suy luận trạng thái (expired, valid, stale…)
- ❌ Thay đổi timezone logic hệ thống

Format ≠ Logic ≠ Decision
"""

from datetime import datetime, date
from typing import Optional, Union

DateLike = Union[datetime, date, str]


def format_date(
    value: Optional[DateLike],
    fmt: str = "%d/%m/%Y",
    empty_placeholder: str = "—"
) -> str:
    """
    Format ngày để hiển thị UI.

    Parameters
    ----------
    value:
        datetime | date | ISO string | string đã format sẵn
        ⚠️ Được coi là ALREADY-DETERMINED timestamp.
    fmt:
        Chuỗi format datetime (default: DD/MM/YYYY).
    empty_placeholder:
        Chuỗi hiển thị khi value None / invalid.

    Returns
    -------
    str
        Chuỗi ngày đã format để hiển thị.

    Governance Guarantees
    ---------------------
    - Không timezone conversion
    - Không normalize
    - Không validate nghiệp vụ
    - Chỉ parse & format presentation
    """

    if value is None:
        return empty_placeholder

    try:
        # datetime hoặc date
        if isinstance(value, datetime):
            return value.strftime(fmt)

        if isinstance(value, date):
            return value.strftime(fmt)

        # string input
        if isinstance(value, str):
            stripped = value.strip()
            if stripped == "":
                return empty_placeholder

            # Thử parse ISO-8601 (YYYY-MM-DD hoặc full timestamp)
            try:
                parsed = datetime.fromisoformat(stripped)
                return parsed.strftime(fmt)
            except ValueError:
                # Nếu không parse được → coi như string hiển thị sẵn
                return stripped

        # Kiểu dữ liệu không hỗ trợ
        return empty_placeholder

    except Exception:
        # Fail-safe: UI không được crash
        return empty_placeholder


"""
📌 AUDIT & LEGAL NOTES
---------------------
- File này KHÔNG được dùng trong:
    ❌ valuation_flow
    ❌ feature pipeline
    ❌ model / rule / approval logic

- Format ngày chỉ mang tính thẩm mỹ UI.
- Thứ tự thời gian, hiệu lực pháp lý, SLA:
    → phải do backend / governance quyết định.

Date formatting = cosmetic representation only.
"""
