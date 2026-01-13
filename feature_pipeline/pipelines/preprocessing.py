# Module: feature_pipeline/pipelines/preprocessing.py
# Chức năng: Biến đổi dữ liệu thô thành Vector để Model hiểu
# FIX: Đã loại bỏ 'shape' do dữ liệu đầu vào bị thiếu cột này

import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

def build_preprocessor():
    # 1. Các cột số (Diện tích, Mặt tiền, Ngõ...)
    numeric_features = ['area_book', 'width', 'length', 'floors', 'alley_width', 'house_quality']
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')), # Điền giá trị thiếu bằng trung vị
        ('scaler', StandardScaler()) # Chuẩn hóa về dạng phân phối chuẩn (Mean=0, Std=1)
    ])

    # 2. Các cột phân loại (Quận, Hướng, Pháp lý...)
    # ĐÃ BỎ 'shape' RA KHỎI DANH SÁCH
    categorical_features = ['district', 'position', 'legal_status'] 
    
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False)) # Mã hóa 1-hot
    ])

    # 3. Tổng hợp lại
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])
    
    return preprocessor