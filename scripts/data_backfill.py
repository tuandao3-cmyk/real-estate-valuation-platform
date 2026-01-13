# Module: scripts/data_backfill.py
# Part of Advanced AVM System

# Module: scripts/data_backfill.py
# Chức năng: Sinh 20.000 dữ liệu giả lập (Synthetic Data) chất lượng cao
# Logic: Tuân thủ valuation_policy.md nhưng có cài cắm Data Drift & Spam

import pandas as pd
import numpy as np
import uuid
import random
import os
import json
from datetime import datetime, timedelta
from faker import Faker

# Khởi tạo
fake = Faker('vi_VN')
np.random.seed(42) # Để tái lập kết quả
random.seed(42)

TOTAL_RECORDS = 20000
OUTPUT_DIR = "data/ingest"
os.makedirs(f"{OUTPUT_DIR}/listings", exist_ok=True)
os.makedirs(f"{OUTPUT_DIR}/transactions", exist_ok=True)

# --- 1. CẤU HÌNH THỊ TRƯỜNG (MARKET CONFIG) ---
# Đơn giá đất trung bình (triệu/m2) cho đất mặt ngõ 3m
DISTRICT_BASE_PRICE = {
    "Hoan Kiem": {"mean": 350, "std": 50},
    "Ba Dinh": {"mean": 200, "std": 30},
    "Dong Da": {"mean": 180, "std": 25},
    "Cau Giay": {"mean": 160, "std": 20},
    "Thanh Xuan": {"mean": 140, "std": 15},
    "Tay Ho": {"mean": 190, "std": 30},
    "Hai Ba Trung": {"mean": 170, "std": 25},
    "Hoang Mai": {"mean": 100, "std": 15},
    "Ha Dong": {"mean": 80, "std": 10},
    "Long Bien": {"mean": 90, "std": 12},
    "Nam Tu Liem": {"mean": 110, "std": 15},
    "Bac Tu Liem": {"mean": 95, "std": 12}
}

LEGAL_STATUS = ["so_do", "so_hong", "cho_cap", "hd_mua_ban", "giay_tay", "vi_bang"]
LEGAL_WEIGHTS = [0.60, 0.20, 0.05, 0.10, 0.03, 0.02] # Đa số là sổ đỏ, ít giấy tay

# Hệ số điều chỉnh giá (Theo valuation_policy.md)
FACTORS = {
    "legal": {"so_do": 1.0, "so_hong": 1.0, "cho_cap": 0.9, "hd_mua_ban": 0.85, "giay_tay": 0.5, "vi_bang": 0.4},
    "position": {"mat_pho": 2.2, "phan_lo": 1.3, "ngo_oto": 1.1, "ngo_ba_gac": 1.0, "ngo_xe_may": 0.8},
    "shape": {"vuong": 1.0, "nop_hau": 1.05, "top_hau": 0.85, "meo_mo": 0.8, "chu_L": 0.9},
}

def generate_synthetic_data(n_rows):
    print(f"🔄 Đang sinh {n_rows} bản ghi với logic phức tạp...")
    data = []
    
    # Tạo danh sách district theo tỷ trọng (Quận trung tâm ít hàng hơn quận mới)
    districts = list(DISTRICT_BASE_PRICE.keys())
    district_choices = np.random.choice(districts, n_rows, p=[0.05, 0.08, 0.1, 0.12, 0.12, 0.05, 0.1, 0.1, 0.1, 0.08, 0.05, 0.05])

    for i in range(n_rows):
        dist = district_choices[i]
        
        # 1. Sinh đặc điểm BĐS (Features)
        # Diện tích: Phân phối Log-normal (Nhiều nhà nhỏ 30-50m2, ít nhà to)
        area = int(np.random.lognormal(mean=3.6, sigma=0.4)) 
        area = max(15, min(area, 200)) # Clip từ 15m2 đến 200m2
        
        width = round(area / (random.uniform(3, 20)), 1) # Mặt tiền
        width = max(2.5, min(width, 10.0))
        
        # Vị trí & Ngõ
        position_type = np.random.choice(
            ["mat_pho", "phan_lo", "ngo_oto", "ngo_ba_gac", "ngo_xe_may"], 
            p=[0.05, 0.05, 0.15, 0.45, 0.30]
        )
        
        # Ngõ: Logic thực tế (Mặt phố thì ngõ to, ngõ xe máy thì ngõ nhỏ)
        if position_type == "mat_pho":
            alley_width = random.uniform(8, 20)
        elif position_type == "ngo_oto":
            alley_width = random.uniform(3.5, 6)
        elif position_type == "ngo_ba_gac":
            alley_width = random.uniform(2.5, 3.4)
        else:
            alley_width = random.uniform(1.0, 2.4)

        # Pháp lý
        legal = np.random.choice(LEGAL_STATUS, p=LEGAL_WEIGHTS)

        # Hình dáng
        shape = np.random.choice(list(FACTORS["shape"].keys()))

        # Nhà ở (Construction)
        floors = np.random.randint(1, 8)
        if position_type == "mat_pho" and floors < 3: floors = np.random.randint(3, 9) # Mặt phố thường xây cao
        
        house_quality = random.uniform(0.3, 1.0) # 1.0 là nhà mới

        # 2. TÍNH GIÁ TRỊ THỰC (TRUE VALUE) - Dựa trên Valuation Policy
        base_price_per_m2 = np.random.normal(DISTRICT_BASE_PRICE[dist]["mean"], DISTRICT_BASE_PRICE[dist]["std"])
        
        # Áp dụng các hệ số
        adj_price = base_price_per_m2 * FACTORS["position"][position_type] * FACTORS["legal"][legal] * FACTORS["shape"][shape]
        
        # Cộng giá trị xây dựng (Giả sử 5tr/m2 sàn x Khấu hao)
        construction_val = (area * floors * 5 * house_quality) 
        land_val = adj_price * area
        
        true_total_price_billion = (land_val + construction_val) / 1000

        # 3. TẠO GIÁ CHÀO (LISTING PRICE) - Có yếu tố cảm tính/thổi giá
        # Giá chào thường cao hơn giá trị thực 5-15%
        markup = random.uniform(0.95, 1.25) 
        listing_price = round(true_total_price_billion * markup, 2)

        # --- TẠO NHIỄU & SPAM (QUAN TRỌNG CHO MODEL) ---
        is_spam = 0
        anomaly_type = "none"
        
        rand_prob = random.random()
        
        # Case 1: Tin ảo giá siêu rẻ (Clickbait) - 2%
        if rand_prob < 0.02:
            listing_price = listing_price * 0.5 
            is_spam = 1
            anomaly_type = "clickbait_low_price"
            
        # Case 2: Tin ngáo giá (Overpriced) - 3%
        elif rand_prob < 0.05:
            listing_price = listing_price * 1.8
            anomaly_type = "overpriced"
        
        # Case 3: Trùng lặp (Duplicate) - Sẽ xử lý copy dòng này ở bước sau
        
        # Case 4: Sai lệch thông tin (Diện tích trên tin khác thực tế) - 5%
        display_area = area
        if rand_prob > 0.95:
            display_area = area * 1.2 # Khai khống diện tích
            anomaly_type = "area_mismatch"

        # Text generation (Sơ sài)
        title = f"Bán nhà {dist}, {display_area}m2, {floors} tầng, giá {listing_price} tỷ"
        if is_spam:
            title = f"CỰC SỐC!! CẮT LỖ SÂU {dist.upper()} {display_area}M2 CHỈ {listing_price} TỶ"

        record = {
            "id": str(uuid.uuid4()),
            "posted_date": (datetime.now() - timedelta(days=random.randint(0, 180))).strftime("%Y-%m-%d"),
            "district": dist,
            "ward": "Phường Giả Định",
            "street": fake.street_name(),
            "address_full": f"{random.randint(1,999)} {fake.street_name()}, {dist}, Hà Nội",
            "position": position_type,
            "legal_status": legal,
            "area_book": area,          # Diện tích sổ
            "area_usage": display_area, # Diện tích sử dụng (tin rao)
            "width": width,
            "length": round(area/width, 1),
            "floors": floors,
            "bedrooms": min(floors * 2, 10),
            "alley_width": round(alley_width, 1),
            "house_quality": round(house_quality * 100, 0),
            "price_billion": listing_price,
            "price_per_m2_million": round((listing_price * 1000) / display_area, 1),
            "lat": 21.0 + random.uniform(-0.05, 0.05), # Toạ độ Hà Nội
            "lng": 105.8 + random.uniform(-0.05, 0.05),
            "source": random.choice(["batdongsan", "chotot", "alonhadat", "facebook_group"]),
            "contact_phone": fake.phone_number(),
            "description": f"{title}. Liên hệ chính chủ. Miễn trung gian.",
            "is_spam_label": is_spam, # Label dùng để test model Trust
            "anomaly_type": anomaly_type
        }
        data.append(record)

    # --- INJECT DUPLICATES (Tạo tin trùng lặp) ---
    # Copy 10% dữ liệu và đổi ID, đổi nhẹ giá để giả lập Môi giới copy bài nhau
    n_dupes = int(n_rows * 0.1)
    print(f"👯 Đang tạo {n_dupes} tin trùng lặp (Copy-paste spam)...")
    for i in range(n_dupes):
        original = data[i].copy()
        original["id"] = str(uuid.uuid4()) # ID mới
        original["source"] = "copy_paste_broker"
        # Giá thay đổi nhẹ (do làm tròn hoặc kê giá)
        original["price_billion"] = round(original["price_billion"] * random.uniform(0.98, 1.02), 2)
        original["posted_date"] = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d")
        original["anomaly_type"] = "duplicate"
        data.append(original)

    return pd.DataFrame(data)

def main():
    print("🚀 Bắt đầu sinh dữ liệu Listing & Transaction...")
    
    # 1. Sinh Listings (Dữ liệu rao bán - Có rác)
    df_listings = generate_synthetic_data(TOTAL_RECORDS)
    
    # Save listings
    listing_path = f"{OUTPUT_DIR}/listings/raw_listings.csv"
    df_listings.to_csv(listing_path, index=False)
    print(f"✅ Đã lưu {len(df_listings)} Listings tại: {listing_path}")

    # 2. Sinh Transactions (Dữ liệu giao dịch thật - Sạch hơn, ít hơn)
    # Lấy 30% từ Listing biến thành Transaction (khớp lệnh)
    # Giá transaction thường thấp hơn giá Listing khoảng 5-10% (thương lượng)
    df_transactions = df_listings.sample(frac=0.3).copy()
    df_transactions["transaction_id"] = [str(uuid.uuid4()) for _ in range(len(df_transactions))]
    df_transactions["closed_price"] = df_transactions["price_billion"] * np.random.uniform(0.85, 0.98, len(df_transactions))
    df_transactions["closed_date"] = pd.to_datetime(df_transactions["posted_date"]) + pd.to_timedelta(np.random.randint(10, 90), unit='D')
    
    # Transaction thì không có spam
    df_transactions = df_transactions[df_transactions["is_spam_label"] == 0]
    
    trans_path = f"{OUTPUT_DIR}/transactions/confirmed_sales.csv"
    df_transactions.to_csv(trans_path, index=False)
    print(f"✅ Đã lưu {len(df_transactions)} Transactions tại: {trans_path}")
    
    print("\n📊 THỐNG KÊ DỮ LIỆU:")
    print(f"- Listings count: {len(df_listings)}")
    print(f"- Spam/Fraud rate: {df_listings['is_spam_label'].mean() * 100:.2f}%")
    print(f"- Transactions count: {len(df_transactions)}")
    print("- Sample Data:")
    print(df_listings[['district', 'price_billion', 'area_book', 'position', 'legal_status', 'anomaly_type']].head(5))

if __name__ == "__main__":
    main()