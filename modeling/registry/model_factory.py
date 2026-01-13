# Module: modeling/registry/model_factory.py
# Chức năng: Kho chứa các thuật toán định giá

from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor

def get_model(model_type='random_forest'):
    """
    Trả về model theo yêu cầu
    """
    if model_type == 'random_forest':
        # Model này giỏi nắm bắt quy luật phi tuyến tính (Non-linear)
        # Vd: Nhà 100m2 giá không chỉ gấp đôi nhà 50m2 mà có thể gấp 2.2 lần
        return RandomForestRegressor(
            n_estimators=100,
            max_depth=15,
            random_state=42,
            n_jobs=-1
        )
    
    elif model_type == 'knn':
        # Model này mô phỏng phương pháp so sánh (Comparable)
        # Tìm 5 thằng láng giềng gần nhất về mặt đặc điểm
        return KNeighborsRegressor(
            n_neighbors=5,
            weights='distance', # Thằng nào giống hơn thì trọng số cao hơn
            metric='manhattan'  # Khoảng cách Manhattan tốt cho dữ liệu đô thị (dạng bàn cờ)
        )
    
    else:
        raise ValueError(f"Model type {model_type} not supported")