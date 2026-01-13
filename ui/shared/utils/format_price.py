# ui/shared/utils/format_price.py
"""
PRICE FORMATTING UTILITY – UI ONLY
=================================

⚠️ GOVERNANCE LOCK
- Tuân thủ:
  - MASTER_SPEC.md
  - IMPLEMENTATION STATUS – PART 1 & PART 2
- File này CHỈ dùng cho UI presentation.

📌 NGUYÊN TẮC CỐT LÕI
- Format hiển thị tiền tệ
- KHÔNG:
    ❌ tính toán số học
    ❌ làm tròn mang ý nghĩa nghiệp vụ
    ❌ suy luận giá trị
    ❌ điều chỉnh output model

Format ≠ Transform ≠ Calculation
"""


from typing import Optional, Union


NumberLike = Union[int, float, str]


def format_price(
    value: Optional[NumberLike],
    currency: str = "VND",
    empty_placeholder: str = "—"
) -> str:
    """
    Format giá tiền để HIỂN THỊ UI.

    Parameters
    ----------
    value:
        Giá trị đầu vào (int / float / numeric string).
        ⚠️ Được coi là ALREADY-COMPUTED value.
    currency:
        Mã tiền tệ hiển thị (default: VND).
    empty_placeholder:
        Chuỗi hiển thị khi value None / rỗng.

    Returns
    -------
    str
        Chuỗi đã format để hiển thị UI.

    Governance Guarantees
    ---------------------
    - Không xử lý số học
    - Không scale, không convert, không round logic
    - Chỉ format string
    """

    if value is None:
        return empty_placeholder

    try:
        # Chuyển sang string số để format,
        # KHÔNG thay đổi giá trị toán học
        numeric_str = str(value)

        # Tách phần thập phân (nếu có)
        if "." in numeric_str:
            integer_part, decimal_part = numeric_str.split(".", 1)
        else:
            integer_part, decimal_part = numeric_str, None

        # Loại bỏ ký tự không phải số ở phần integer
        cleaned_integer = "".join(ch for ch in integer_part if ch.isdigit())

        if cleaned_integer == "":
            return empty_placeholder

        # Thêm dấu phân cách hàng nghìn
        formatted_integer = "{:,}".format(int(cleaned_integer))

        if decimal_part:
            formatted_value = f"{formatted_integer}.{decimal_part}"
        else:
            formatted_value = formatted_integer

        # Chuẩn hiển thị theo VND / generic
        if currency.upper() == "VND":
            return f"{formatted_value} ₫"
        else:
            return f"{formatted_value} {currency.upper()}"

    except Exception:
        # Fail-safe: UI không được crash vì format
        return empty_placeholder


"""
📌 AUDIT & LEGAL NOTES
---------------------
- Hàm này không được dùng trong:
    ❌ model
    ❌ feature pipeline
    ❌ valuation engine
- Chỉ dùng tại UI layer.

Price formatting = cosmetic presentation.
Không mang ý nghĩa nghiệp vụ hay pháp lý.
"""
