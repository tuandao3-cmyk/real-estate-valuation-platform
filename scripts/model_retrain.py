# Module: scripts/model_retrain.py
# Part of Advanced AVM System

# Module: scripts/model_retrain.py
# Chức năng: Huấn luyện và đóng gói Model (MLOps Standard)

import sys
import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_percentage_error, r2_score

# Thêm đường dẫn để import được các module trong project
sys.path.append(os.getcwd())

from feature_pipeline.pipelines.preprocessing import build_preprocessor
from modeling.registry.model_factory import get_model

def train_system():
    print("🚀 BẮT ĐẦU QUÁ TRÌNH HUẤN LUYỆN HỆ THỐNG ĐỊNH GIÁ...")
    
    # 1. Load dữ liệu sạch
    data_path = "data/ingest/listings/final_training_data.csv"
    if not os.path.exists(data_path):
        print("❌ Lỗi: Không tìm thấy file dữ liệu. Hãy chạy pipeline Ngày 3 trước.")
        return

    df = pd.read_csv(data_path)
    
    # Tách biến mục tiêu (Target): Giá trị tỷ đồng
    X = df.drop(columns=['price_billion', 'id', 'description', 'address_full', 'price_per_m2', 'is_anomaly', 'anomaly_reason', 'posted_date'])
    y = df['price_billion']
    
    # Chia train/test (80% học, 20% thi)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print(f"📊 Dữ liệu huấn luyện: {len(X_train)} bản ghi")
    print(f"📊 Dữ liệu kiểm thử: {len(X_test)} bản ghi")

    # Tạo thư mục lưu model
    os.makedirs("modeling/storage", exist_ok=True)

    # --- MODEL 1: RANDOM FOREST (HEDONIC) ---
    print("\n🏗️  Đang train Model 1: Random Forest (Hedonic)...")
    rf_pipeline = Pipeline(steps=[
        ('preprocessor', build_preprocessor()),
        ('regressor', get_model('random_forest'))
    ])
    
    rf_pipeline.fit(X_train, y_train)
    
    # Đánh giá
    y_pred_rf = rf_pipeline.predict(X_test)
    mape_rf = mean_absolute_percentage_error(y_test, y_pred_rf)
    print(f"✅ Random Forest MAPE (Sai số trung bình): {mape_rf:.2%}")
    
    # Lưu model
    joblib.dump(rf_pipeline, "modeling/storage/rf_model_v1.pkl")
    
    # --- MODEL 2: KNN (COMPARABLE) ---
    print("\n🏗️  Đang train Model 2: KNN (Comparable Sales)...")
    knn_pipeline = Pipeline(steps=[
        ('preprocessor', build_preprocessor()),
        ('regressor', get_model('knn'))
    ])
    
    knn_pipeline.fit(X_train, y_train)
    
    # Đánh giá
    y_pred_knn = knn_pipeline.predict(X_test)
    mape_knn = mean_absolute_percentage_error(y_test, y_pred_knn)
    print(f"✅ KNN MAPE (Sai số trung bình): {mape_knn:.2%}")
    
    # Lưu model
    joblib.dump(knn_pipeline, "modeling/storage/knn_model_v1.pkl")

    print("\n🎉 HUẤN LUYỆN HOÀN TẤT!")
    print(f"💾 Models đã được lưu tại: modeling/storage/")

if __name__ == "__main__":
    train_system()