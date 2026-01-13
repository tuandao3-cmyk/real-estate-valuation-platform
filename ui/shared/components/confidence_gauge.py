# ui/shared/components/confidence_gauge.py
"""
CONFIDENCE GAUGE – DESCRIPTIVE UI COMPONENT
==========================================

🚫 GOVERNANCE LOCK – STRICT COMPLIANCE
- Tuân thủ tuyệt đối:
  - MASTER_SPEC.md
  - IMPLEMENTATION STATUS – PART 1 & PART 2

📌 MỤC ĐÍCH
- Hiển thị confidence score dưới dạng trực quan cho UI
- Chỉ mang tính MÔ TẢ trạng thái dữ liệu & mức độ đồng thuận mô hình

📌 NGUYÊN TẮC BẮT BUỘC
- Confidence ≠ Accuracy
- Confidence ≠ Approval
- Confidence ≠ Correctness
- Confidence là WORKFLOW SIGNAL, không phải kết luận

📌 UI CHỈ HIỂN THỊ – KHÔNG DIỄN GIẢI
- Không dùng từ:
  ❌ “cao / thấp là tốt / xấu”
  ❌ “đáng tin”
  ❌ “có thể dùng”
"""

import streamlit as st
from typing import Optional


# =========================
# INTERNAL COLOR MAPPING
# =========================
# 📌 Màu sắc CHỈ mang tính trực quan, không semantic judgement
_CONFIDENCE_COLOR = {
    "LOW": "#d62728",      # đỏ nhạt – attention required
    "MEDIUM": "#ff7f0e",   # cam – neutral
    "HIGH": "#2ca02c",     # xanh – descriptive only
}


# =========================
# RENDER FUNCTION
# =========================

def render_confidence_gauge(
    confidence_score: Optional[float],
    confidence_band: Optional[str],
) -> None:
    """
    Render confidence gauge.

    Parameters
    ----------
    confidence_score : float | None
        Giá trị confidence (0.0 – 1.0) do backend trả về.
        UI không được chỉnh sửa, làm tròn hay suy luận.

    confidence_band : str | None
        Nhãn mô tả (LOW / MEDIUM / HIGH) từ ensemble output.

    GOVERNANCE NOTES
    ----------------
    - UI không tính toán confidence
    - UI không gán threshold
    - UI không quyết định hành động
    """

    st.subheader("Confidence (Descriptive Signal)")

    if confidence_score is None or confidence_band is None:
        st.info("Confidence signal is not available for this valuation.")
        return

    # Clamp hiển thị để tránh lỗi UI, KHÔNG phải xử lý logic
    display_value = max(0.0, min(1.0, confidence_score))

    color = _CONFIDENCE_COLOR.get(confidence_band.upper(), "#7f7f7f")

    # =========================
    # PROGRESS BAR (VISUAL ONLY)
    # =========================
    st.progress(display_value)

    # =========================
    # TEXTUAL DISPLAY
    # =========================
    st.markdown(
        f"""
        **Confidence Band:** `{confidence_band.upper()}`  
        **Confidence Score:** `{display_value:.2f}`

        <div style="font-size: 0.85em; color: {color};">
        This confidence indicator describes data quality and model agreement only.
        It does not imply correctness, approval, or valuation acceptance.
        </div>
        """,
        unsafe_allow_html=True,
    )


"""
📌 AUDIT & LEGAL NOTES
---------------------
- Component này:
    ✔ Được phép xuất hiện trong valuation view
    ✔ Được phép xuất hiện trong manager / audit view

- Component này KHÔNG ĐƯỢC:
    ❌ gợi ý quyết định
    ❌ ánh xạ trực tiếp sang workflow action
    ❌ ẩn dispersion hoặc uncertainty

Nguyên tắc pháp lý:
"Confidence để hiểu – không để chốt."

Human judgment là bắt buộc.
"""
