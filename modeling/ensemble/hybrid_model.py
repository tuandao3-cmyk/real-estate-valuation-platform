# Module: modeling/ensemble/hybrid_model.py
# Chức năng: Kết hợp kết quả từ nhiều Model để tăng độ ổn định

import joblib
import pandas as pd
import numpy as np
import os

class HybridValuationModel:
    def __init__(self):
        # Load models đã train ở Ngày 4
        base_path = "modeling/storage"
        try:
            self.rf_model = joblib.load(f"{base_path}/rf_model_v1.pkl")
            self.knn_model = joblib.load(f"{base_path}/knn_model_v1.pkl")
            self.is_loaded = True
            print("✅ Đã load thành công 2 model định giá.")
        except FileNotFoundError:
            print("❌ Lỗi: Không tìm thấy file model .pkl")
            self.is_loaded = False

    def predict(self, features_df):
        if not self.is_loaded:
            raise Exception("Model chưa được load.")

        # 1. Dự đoán độc lập
        price_rf = self.rf_model.predict(features_df)
        price_knn = self.knn_model.predict(features_df)

        # 2. Hợp nhất (Ensemble Strategy)
        # Random Forest thường tốt hơn ở dữ liệu bảng, nên cho trọng số cao hơn (60%)
        # KNN đóng vai trò tham chiếu so sánh (40%)
        final_price = (0.6 * price_rf) + (0.4 * price_knn)

        return {
            "final_price": final_price[0],
            "details": {
                "hedonic_rf_price": price_rf[0],
                "comparable_knn_price": price_knn[0],
                "confidence_gap": abs(price_rf[0] - price_knn[0]) / final_price[0] # Độ lệch giữa 2 model
            }
        }