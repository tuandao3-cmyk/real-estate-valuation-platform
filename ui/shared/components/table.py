# ui/shared/components/table.py
"""
TABLE COMPONENT – READ-ONLY DATA PRESENTATION
=============================================

🚫 GOVERNANCE LOCK – STRICT COMPLIANCE
- Tuân thủ tuyệt đối:
  - MASTER_SPEC.md
  - IMPLEMENTATION STATUS – PART 1 & PART 2

📌 MỤC ĐÍCH
- Hiển thị dữ liệu dạng bảng trong UI
- Phục vụ:
    ✔ Trình bày kết quả
    ✔ Minh bạch dữ liệu
    ✔ Audit & review

📌 NGUYÊN TẮC BẤT DI BẤT DỊCH
- Table ≠ Analytics
- Table ≠ Ranking
- Table ≠ Decision support logic

UI CHỈ ĐƯỢC:
- Render dữ liệu đã có
- Không sort nghiệp vụ
- Không filter nghiệp vụ
- Không tính toán

📌 Đây là lớp VIEW THUẦN TÚY.
"""

import streamlit as st
import pandas as pd
from typing import List, Dict, Optional


# =========================
# RENDER FUNCTION
# =========================

def render_table(
    data: List[Dict],
    columns: Optional[List[str]] = None,
    caption: Optional[str] = None,
) -> None:
    """
    Render bảng dữ liệu read-only.

    Parameters
    ----------
    data : List[Dict]
        Dữ liệu đã được backend chuẩn hóa.
        UI không được chỉnh sửa nội dung.

    columns : List[str] | None
        Danh sách cột cần hiển thị theo thứ tự.
        Nếu None → hiển thị toàn bộ key.

    caption : str | None
        Ghi chú mô tả bảng (trung lập, không diễn giải).

    GOVERNANCE NOTES
    ----------------
    - Không suy luận dữ liệu
    - Không biến đổi giá trị
    - Không thêm cột dẫn dắt
    """

    if not data:
        st.info("No data available to display.")
        return

    try:
        df = pd.DataFrame(data)
    except Exception:
        st.error("Invalid table data format.")
        return

    if columns:
        # Chỉ chọn cột tồn tại – không tự tạo
        valid_columns = [c for c in columns if c in df.columns]
        df = df[valid_columns]

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )

    if caption:
        st.markdown(
            f"""
            <div style="font-size: 0.85em; color: #666; margin-top: 0.25em;">
                {caption}
            </div>
            """,
            unsafe_allow_html=True,
        )


"""
📌 AUDIT & LEGAL NOTES
---------------------
- Component này:
    ✔ Chỉ dùng để hiển thị dữ liệu
    ✔ Phù hợp cho valuation, report, audit UI
    ✔ Không mang tính diễn giải

- Component này KHÔNG ĐƯỢC:
    ❌ dùng để so sánh hơn / kém
    ❌ gán ý nghĩa “tốt / xấu”
    ❌ thay thế báo cáo chính thức

Nguyên tắc pháp lý:
"Bảng để xem – không để kết luận."

Human đọc.  
System trình bày.
"""
