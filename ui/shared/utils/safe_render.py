# ui/shared/utils/safe_render.py
"""
SAFE RENDERING UTILITY – UI AUDIT CRITICAL
=========================================

⚠️ GOVERNANCE LOCK – MANDATORY
- Tuân thủ tuyệt đối:
  - MASTER_SPEC.md
  - IMPLEMENTATION STATUS – PART 1 & PART 2
- File này là BẮT BUỘC cho mọi render HTML / Markdown trong UI.

📌 MỤC ĐÍCH
- Render nội dung HTML / Markdown theo cách:
    ✔ An toàn (XSS-safe)
    ✔ Audit-friendly
    ✔ Không làm sai lệch nội dung pháp lý
    ✔ Không cho phép executable content

📌 NGUYÊN TẮC CỐT LÕI
- Render ≠ Transform
- Render ≠ Interpret
- UI không được “hiểu” nội dung, chỉ được hiển thị

⛔ CẤM TUYỆT ĐỐI
- ❌ Render script
- ❌ Inline JS / event handler
- ❌ iframe / embed
- ❌ Thay đổi nội dung semantic
"""

from typing import Optional

import html
import markdown
import bleach


# =========================
# ALLOWED TAGS & ATTRIBUTES
# =========================

_ALLOWED_HTML_TAGS = [
    "p", "br",
    "strong", "b", "em", "i", "u",
    "ul", "ol", "li",
    "blockquote",
    "code", "pre",
    "span",
    "h1", "h2", "h3", "h4", "h5", "h6",
    "table", "thead", "tbody", "tr", "th", "td",
]

_ALLOWED_HTML_ATTRIBUTES = {
    "*": ["class", "style"],
}

_ALLOWED_PROTOCOLS = ["http", "https", "mailto"]


# =========================
# SAFE RENDER FUNCTIONS
# =========================

def render_safe_markdown(
    content: Optional[str],
    empty_placeholder: str = "—"
) -> str:
    """
    Render Markdown an toàn cho UI.

    Flow:
    -----
    Raw markdown
        → markdown → HTML
        → sanitize (bleach)
        → return safe HTML string

    Governance Guarantees
    ---------------------
    - Không execute
    - Không inject
    - Không rewrite nội dung
    - Deterministic
    """

    if content is None:
        return empty_placeholder

    stripped = content.strip()
    if stripped == "":
        return empty_placeholder

    # Markdown → HTML (no extensions that allow raw HTML)
    html_content = markdown.markdown(
        stripped,
        extensions=[],
        output_format="html"
    )

    # Sanitize HTML
    safe_html = bleach.clean(
        html_content,
        tags=_ALLOWED_HTML_TAGS,
        attributes=_ALLOWED_HTML_ATTRIBUTES,
        protocols=_ALLOWED_PROTOCOLS,
        strip=True
    )

    return safe_html


def render_safe_html(
    content: Optional[str],
    empty_placeholder: str = "—"
) -> str:
    """
    Render HTML an toàn cho UI.

    📌 Dùng cho:
    - Nội dung đã được sinh từ backend governance-controlled
    - Report
    - Explainability
    - Commentary

    Governance Guarantees
    ---------------------
    - Không script
    - Không inline JS
    - Không dynamic execution
    """

    if content is None:
        return empty_placeholder

    stripped = content.strip()
    if stripped == "":
        return empty_placeholder

    # Escape trước để tránh HTML injection thô
    escaped = html.unescape(stripped)

    safe_html = bleach.clean(
        escaped,
        tags=_ALLOWED_HTML_TAGS,
        attributes=_ALLOWED_HTML_ATTRIBUTES,
        protocols=_ALLOWED_PROTOCOLS,
        strip=True
    )

    return safe_html


def render_plain_text(
    content: Optional[str],
    empty_placeholder: str = "—"
) -> str:
    """
    Render text thuần (escape toàn bộ).

    Dùng cho:
    - Audit log
    - Legal text
    - Reason code
    - Actor comment

    Governance Guarantees
    ---------------------
    - Không HTML
    - Không Markdown
    - Absolute safety
    """

    if content is None:
        return empty_placeholder

    stripped = content.strip()
    if stripped == "":
        return empty_placeholder

    return html.escape(stripped)


"""
📌 AUDIT & LEGAL NOTES
---------------------
- TẤT CẢ nội dung render UI phải đi qua file này.
- Không được dùng:
    ❌ st.markdown(unsafe_allow_html=True) trực tiếp
    ❌ render raw HTML từ user input
    ❌ bypass sanitize layer

- Nếu audit phát hiện UI render bypass:
    → SYSTEM NON-COMPLIANT.

Safe rendering = BẮT BUỘC để:
- Ngăn XSS
- Bảo toàn bằng chứng
- Bảo vệ hệ thống trước tranh tụng

UI được phép hiển thị — không được phép hiểu.
"""
