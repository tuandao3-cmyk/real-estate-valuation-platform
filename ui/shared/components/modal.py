# ui/shared/components/modal.py
"""
MODAL COMPONENT – GOVERNANCE-SAFE UI OVERLAY
============================================

🚫 GOVERNANCE LOCK – STRICT COMPLIANCE
Tuân thủ tuyệt đối:
- MASTER_SPEC.md
- IMPLEMENTATION STATUS – PART 1 & PART 2

📌 MỤC ĐÍCH
- Hiển thị thông tin chi tiết / giải thích bổ sung trong UI
- Dùng cho:
    ✔ Explanation
    ✔ Disclosure
    ✔ Audit context
    ✔ Human review support

📌 NGUYÊN TẮC BẤT DI BẤT DỊCH
- Modal ≠ Decision
- Modal ≠ Approval
- Modal ≠ Action trigger

UI CHỈ ĐƯỢC:
- Hiển thị nội dung đã có
- Đóng / mở theo thao tác người dùng
- Không chứa logic nghiệp vụ
- Không tự sinh nội dung suy luận

📌 Đây là VIEW-ONLY OVERLAY.
"""

import streamlit as st
from typing import Optional


# =========================
# MODAL RENDERER
# =========================

def render_modal(
    title: str,
    content: str,
    key: str,
    width: str = "medium",
    disclaimer: Optional[str] = None,
) -> None:
    """
    Render modal dialog an toàn cho audit.

    Parameters
    ----------
    title : str
        Tiêu đề modal (mô tả trung lập).

    content : str
        Nội dung hiển thị (HTML / Markdown đã được kiểm soát).
        ❌ Không suy luận
        ❌ Không prescriptive language

    key : str
        Key duy nhất để quản lý state mở/đóng.

    width : str
        small | medium | large

    disclaimer : str | None
        Ghi chú pháp lý / governance (nếu có).

    GOVERNANCE NOTES
    ----------------
    - Modal chỉ phục vụ đọc
    - Không chứa button hành động nghiệp vụ
    - Không ghi state ra ngoài UI
    """

    if key not in st.session_state:
        st.session_state[key] = False

    if st.session_state[key]:
        with st.modal(title, key=f"{key}_modal"):
            st.markdown(content)

            if disclaimer:
                st.markdown(
                    f"""
                    <div style="
                        margin-top: 1em;
                        padding: 0.75em;
                        background-color: #f8f9fa;
                        border-left: 4px solid #999;
                        font-size: 0.85em;
                        color: #555;
                    ">
                        {disclaimer}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown("---")
            if st.button("Close", key=f"{key}_close"):
                st.session_state[key] = False


# =========================
# MODAL TRIGGER
# =========================

def modal_trigger(
    label: str,
    key: str,
    help_text: Optional[str] = None,
) -> None:
    """
    Render nút mở modal.

    Parameters
    ----------
    label : str
        Nhãn nút (trung lập, không mệnh lệnh).

    key : str
        Key modal tương ứng.

    help_text : str | None
        Tooltip mô tả (tuỳ chọn).

    GOVERNANCE
    ----------
    - Button chỉ mở UI
    - Không kích hoạt workflow
    - Không ghi log nghiệp vụ
    """

    if st.button(label, help=help_text, key=f"{key}_open"):
        st.session_state[key] = True


"""
📌 AUDIT & LEGAL NOTES
---------------------
- Modal dùng để:
    ✔ Cung cấp ngữ cảnh
    ✔ Giải thích kết quả
    ✔ Trình bày giới hạn hệ thống

- Modal KHÔNG ĐƯỢC:
    ❌ dùng để yêu cầu phê duyệt
    ❌ gợi ý quyết định
    ❌ thay thế hồ sơ chính thức

Nguyên tắc pháp lý:
"Modal để hiểu – không để quyết."

Human đọc.  
System trình bày.
"""
