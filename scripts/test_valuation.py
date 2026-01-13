# Module: scripts/test_valuation.py
# Chức năng: Script test nhanh luồng định giá

import sys
import os

# Thêm đường dẫn project
sys.path.append(os.getcwd())

from valuation_engine.workflow.valuation_flow import ValuationEngine

def run_test():
    engine = ValuationEngine()
    
    # 1. Test Case 1: Nhà phố xịn (Sổ đỏ, Mặt phố)
    print("--- CASE 1: Nhà đẹp ---")
    case_good = {
        "id": "TEST-001",
        "district": "Cau Giay",
        "area_book": 50,
        "width": 5.0,
        "length": 10.0,
        "floors": 4,
        "alley_width": 10.0, # Mặt phố
        "house_quality": 80,
        "position": "mat_pho",
        "legal_status": "so_do" # Hệ số 1.0
    }
    result_1 = engine.process_request(case_good)
    print(result_1)

    # 2. Test Case 2: Nhà pháp lý yếu (Hợp đồng mua bán)
    print("\n--- CASE 2: Pháp lý yếu ---")
    case_risk = {
        "id": "TEST-002",
        "district": "Cau Giay", # Cùng khu vực để so sánh
        "area_book": 50,
        "width": 5.0,
        "length": 10.0,
        "floors": 4,
        "alley_width": 10.0, 
        "house_quality": 80,
        "position": "mat_pho",
        "legal_status": "hd_mua_ban" # Hệ số 0.9
    }
    result_2 = engine.process_request(case_risk)
    print(f"Giá Case 1 (Sổ đỏ): {result_1['valuation_result']['market_value_suggested']} tỷ")
    print(f"Giá Case 2 (HĐMB):  {result_2['valuation_result']['market_value_suggested']} tỷ")
    
    # 3. Test Case 3: Giấy tay (Từ chối)
    print("\n--- CASE 3: Giấy tay ---")
    case_reject = case_good.copy()
    case_reject['legal_status'] = "giay_tay"
    print(engine.process_request(case_reject))

if __name__ == "__main__":
    run_test()