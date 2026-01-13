# ui/shared/state/feature_flags.py
"""
UI FEATURE FLAGS – GOVERNANCE CONTROLLED
======================================

⚠️ GOVERNANCE LOCK
- Tuân thủ tuyệt đối:
  - MASTER_SPEC.md
  - IMPLEMENTATION STATUS – PART 1 & PART 2
- File này là CẤP CỜ (feature toggle) cho UI layer.
- Feature flag UI ≠ năng lực hệ thống ≠ quyền nghiệp vụ.

📌 Mục đích:
- Bật / tắt hiển thị hoặc khả năng thao tác UI
- Phản ánh trạng thái governance, rollout, kiểm soát rủi ro
- KHÔNG:
    ❌ kích hoạt logic backend
    ❌ override rule engine
    ❌ mở quyền quyết định định giá
"""

from dataclasses import dataclass


# =========================
# FEATURE FLAG SCHEMA
# =========================

@dataclass(frozen=True)
class UIFeatureFlags:
    """
    Immutable UI feature flags.

    📌 Flags chỉ ảnh hưởng presentation & interaction,
    không ảnh hưởng valuation workflow.
    """

    # Override UI (request override form)
    enable_override: bool = False

    # Hiển thị confidence breakdown chi tiết
    enable_confidence_details: bool = True

    # Hiển thị explainability (read-only)
    enable_explainability_panel: bool = True

    # Cho phép xem drift / stability report (audit view)
    enable_model_diagnostics: bool = False

    # Cho phép truy cập trang admin UI
    enable_admin_view: bool = False

    # Hiển thị tier routing detail
    enable_tier_visibility: bool = True


# =========================
# SINGLETON ACCESSOR
# =========================

def get_ui_feature_flags() -> UIFeatureFlags:
    """
    Trả về bộ feature flags hiện tại của UI.

    📌 Hiện tại:
    - Flags được hard-code theo governance freeze.
    - KHÔNG load từ env
    - KHÔNG toggle runtime bởi user
    """
    return UIFeatureFlags()


"""
📌 LEGAL & AUDIT NOTES
---------------------
- Feature flag UI không được ghi vào audit log định giá.
- Feature flag UI không được serialize vào valuation_dossier.
- Bật flag ≠ cấp quyền nghiệp vụ.
- Mọi hành động nhạy cảm (override, approval):
    → Backend + human responsibility quyết định.

UI Feature Flags = Governance-Driven Presentation Control Only.
"""
