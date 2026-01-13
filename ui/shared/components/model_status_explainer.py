# ui/shared/components/model_status_explainer.py
"""
MODEL STATUS EXPLAINER – GOVERNANCE UI COMPONENT
===============================================

🚫 GOVERNANCE LOCK – STRICT COMPLIANCE
- Tuân thủ tuyệt đối:
  - MASTER_SPEC.md
  - IMPLEMENTATION STATUS – PART 1 & PART 2

📌 MỤC ĐÍCH
- Giải thích Ý NGHĨA của trạng thái model (✅ ⚠️ ❌) cho user
- Phục vụ:
    ✔ Appraiser (hiểu giới hạn tín hiệu)
    ✔ Manager (hiểu rủi ro vận hành)
    ✔ Auditor (đối chiếu legal meaning)

📌 NGUYÊN TẮC CỐT LÕI
- Explanation ≠ justification
- Explanation ≠ approval
- Explanation ≠ recommendation
- Ngôn ngữ TRUNG LẬP – PHÁP LÝ AN TOÀN

UI giải thích biểu tượng, KHÔNG giải thích giá.
"""

import streamlit as st
from enum import Enum


class ModelStatus(str, Enum):
    """
    Đồng bộ với model_status.py
    ❌ Không tự ý thêm trạng thái
    """
    OK = "OK"
    WARNING = "WARNING"
    ERROR = "ERROR"


# =========================
# EXPLANATION REGISTRY
# =========================

_STATUS_EXPLANATION = {
    ModelStatus.OK: {
        "icon": "✅",
        "title": "Status: OK",
        "description": (
            "Model hoặc artifact hoạt động trong phạm vi kỹ thuật "
            "đã được định nghĩa. Không phát hiện vi phạm schema, "
            "version hoặc governance constraint tại thời điểm chạy."
        ),
        "legal_note": (
            "Status OK không đồng nghĩa với việc kết quả là chính xác, "
            "được phê duyệt hoặc được phép dùng làm quyết định định giá."
        ),
    },
    ModelStatus.WARNING: {
        "icon": "⚠️",
        "title": "Status: WARNING",
        "description": (
            "Model hoặc artifact vẫn hợp lệ về mặt kỹ thuật, "
            "nhưng tồn tại tín hiệu cần human review "
            "(ví dụ: coverage thấp, dispersion cao, signal phụ thuộc giả định)."
        ),
        "legal_note": (
            "Warning là tín hiệu chú ý, không phải lỗi, "
            "và không tự động chặn workflow."
        ),
    },
    ModelStatus.ERROR: {
        "icon": "❌",
        "title": "Status: ERROR",
        "description": (
            "Model hoặc artifact không thỏa điều kiện sử dụng "
            "(vi phạm schema, version mismatch, thiếu artifact, "
            "hoặc bị governance gate chặn)."
        ),
        "legal_note": (
            "Status ERROR yêu cầu human intervention. "
            "UI không được phép suy luận hay đề xuất hành động khắc phục."
        ),
    },
}


# =========================
# RENDER FUNCTION
# =========================

def render_model_status_explainer(status: ModelStatus) -> None:
    """
    Render phần giải thích trạng thái model.

    Parameters
    ----------
    status : ModelStatus
        Trạng thái đã được backend / dossier xác định.

    📌 GOVERNANCE NOTE
    - Giải thích mang tính định nghĩa
    - Không gắn với output cụ thể
    - Không dẫn dắt quyết định
    """

    if status not in _STATUS_EXPLANATION:
        return

    cfg = _STATUS_EXPLANATION[status]

    with st.expander(f"{cfg['icon']} {cfg['title']} – What does this mean?"):
        st.markdown(
            f"""
            **Technical Meaning**

            {cfg['description']}

            **Governance / Legal Note**

            _{cfg['legal_note']}_
            """
        )


"""
📌 AUDIT & LEGAL NOTES
---------------------
- Component này:
    ✔ Được phép dùng trong valuation UI
    ✔ Được phép dùng trong audit / admin UI

- Component này KHÔNG ĐƯỢC:
    ❌ gắn với outcome giá
    ❌ so sánh model
    ❌ gợi ý chọn / bỏ model
    ❌ dùng ngôn ngữ "an toàn", "tốt", "đáng tin"

Auditor-friendly principle:
"Biểu tượng nói lên trạng thái kỹ thuật,
giải thích nói lên giới hạn pháp lý."

UI giải thích – Human chịu trách nhiệm.
"""
