"""
ui/navigation.py

ROLE
----
Central UI navigation registry.

LEGAL & GOVERNANCE POSITIONING
------------------------------
- Defines available pages per role
- Enforces maker–checker & audit separation at UI level
- No business logic, no valuation logic, no inference

COMPLIANCE
----------
✔ MASTER_SPEC.md
✔ IMPLEMENTATION STATUS PHẦN 1
✔ IMPLEMENTATION STATUS PHẦN 2
"""

import streamlit as st

from ui.shared.auth.role_guard import get_current_role

# =========================
# NAVIGATION REGISTRY
# =========================

NAVIGATION = {
    "VALUATION": {
        "label": "Định giá",
        "roles": ["APPRAISER"],
        "pages": [
            {
                "label": "Hàng chờ định giá",
                "module": "ui.appraiser.pages.valuation_queue",
                "entry": "valuation_queue_view",
            },
            {
                "label": "Hồ sơ định giá",
                "module": "ui.appraiser.pages.valuation_detail",
                "entry": "valuation_detail_view",
            },
        ],
    },
    "MANAGEMENT": {
        "label": "Phê duyệt",
        "roles": ["MANAGER"],
        "pages": [
            {
                "label": "Hàng chờ phê duyệt",
                "module": "ui.manager.pages.approval_queue",
                "entry": "approval_queue_view",
            },
            {
                "label": "Xử lý override",
                "module": "ui.manager.pages.override_view",
                "entry": "override_view",
            },
            {
                "label": "Nhật ký kiểm soát",
                "module": "ui.manager.pages.audit_log",
                "entry": "audit_log_view",
            },
        ],
    },
    "GOVERNANCE": {
        "label": "Governance",
        "roles": ["GOVERNANCE", "AUDITOR"],
        "pages": [
            {
                "label": "Decision Boundary",
                "module": "ui.governance.pages.decision_boundary_view",
                "entry": "decision_boundary_view",
            },
            {
                "label": "Phạm vi sử dụng mô hình",
                "module": "ui.governance.pages.model_usage_scope",
                "entry": "model_usage_scope_view",
            },
            {
                "label": "Quy tắc override",
                "module": "ui.governance.pages.override_rules_view",
                "entry": "override_rules_view",
            },
            {
                "label": "Mapping pháp lý",
                "module": "ui.governance.pages.regulatory_mapping_view",
                "entry": "regulatory_mapping_view",
            },
            {
                "label": "Tuyên bố trách nhiệm",
                "module": "ui.governance.pages.liability_notice",
                "entry": "liability_notice_view",
            },
        ],
    },
    "AUDIT": {
        "label": "Kiểm toán",
        "roles": ["AUDITOR"],
        "pages": [
            {
                "label": "Dấu vết định giá",
                "module": "ui.audit.pages.valuation_trace_view",
                "entry": "valuation_trace_view",
            },
            {
                "label": "Kích hoạt mô hình",
                "module": "ui.audit.pages.model_activation_log",
                "entry": "model_activation_log_view",
            },
            {
                "label": "Nguồn gốc dữ liệu",
                "module": "ui.audit.pages.data_provenance_view",
                "entry": "data_provenance_view",
            },
            {
                "label": "Tái lập kết quả",
                "module": "ui.audit.pages.reproducibility_view",
                "entry": "reproducibility_view",
            },
        ],
    },
}

# =========================
# NAVIGATION RENDERER
# =========================

def render_navigation():
    """
    Render sidebar navigation based on current user role.

    GUARANTEES
    ----------
    - Role-based visibility
    - No dynamic privilege escalation
    - Deterministic menu structure
    """

    role = get_current_role()

    st.sidebar.title("📂 Chức năng")

    for section_key, section in NAVIGATION.items():
        if role not in section["roles"]:
            continue

        with st.sidebar.expander(section["label"], expanded=True):
            for page in section["pages"]:
                if st.button(page["label"], key=f"{section_key}:{page['entry']}"):
                    _load_page(page)


def _load_page(page: dict):
    """
    Dynamically import and render a page.

    SECURITY NOTE
    -------------
    - Module & entry are predefined constants
    - No user-controlled import paths
    """

    module = __import__(page["module"], fromlist=[page["entry"]])
    view_fn = getattr(module, page["entry"])
    view_fn()
