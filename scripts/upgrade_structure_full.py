import os

def upgrade_structure():
    print("🏗️ Đang nâng cấp cấu trúc dự án lên chuẩn Enterprise...")
    
    dirs_to_create = [
        "docs/model_governance",
        "docs/risk/stress_scenarios",
        "docs/ops",
        "tests/data_quality",
        "tests/valuation_logic",
        "tests/model_consistency",
        "tests/regression",
        "tests/approval_flow",
        "model_governance",
        "ui/appraiser",
        "ui/manager",
        "ui/reports/signed_reports",
        "ui/shared"
    ]
    
    files_to_create = {
        "docs/model_governance/model_approval_committee.md": "# Hội đồng phê duyệt Model\n",
        "docs/model_governance/champion_challenger_policy.md": "# Chính sách Champion/Challenger\n",
        "docs/risk/stress_scenarios/market_crash_2008.yaml": "scenario_name: Market Crash 2008\nimpact: -30%",
        "docs/risk/stress_scenarios/local_bubble_burst.yaml": "scenario_name: Local Bubble Burst\nimpact: -15%",
        "docs/ops/fallback_policy.md": "# Chính sách Fallback khi AI sập\n",
        "docs/ops/manual_override_threshold.md": "# Ngưỡng can thiệp thủ công\n",
        "ui/appraiser/dashboard.py": "# Dashboard thẩm định viên\n"
    }

    # Tạo thư mục
    for d in dirs_to_create:
        os.makedirs(d, exist_ok=True)
        print(f"✅ Created dir: {d}")

    # Tạo file
    for f, content in files_to_create.items():
        with open(f, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"📄 Created file: {f}")

    print("\n🚀 Cấu trúc đã khớp 100% với bản thiết kế Enterprise!")

if __name__ == "__main__":
    upgrade_structure()