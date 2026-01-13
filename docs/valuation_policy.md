# CHÍNH SÁCH ĐỊNH GIÁ TÀI SẢN BẤT ĐỘNG SẢN

# (VALUATION POLICY)

---

**Phiên bản:** 3.0 – Bank‑Grade / Enterprise Standard
**Áp dụng cho:** AVM Real Estate AI Platform
**Phạm vi sử dụng:** Nội bộ Tổ chức tín dụng, Hội đồng tín dụng, Kiểm toán nội bộ, Quản trị rủi ro
**Căn cứ pháp lý:** Tiêu chuẩn Thẩm định giá Việt Nam (TĐGVN 01–13), Basel II/III (Model Risk), thông lệ thẩm định ngân hàng Việt Nam

---

## I. MỤC ĐÍCH VÀ PHẠM VI ÁP DỤNG

### 1.1. Mục đích

Tài liệu này quy định **nguyên tắc, giới hạn và cơ chế quản trị** đối với hoạt động định giá bất động sản được hỗ trợ bởi hệ thống AVM (Automated Valuation Model).

Chính sách này nhằm:

- Đảm bảo kết quả định giá phù hợp quy định pháp luật Việt Nam
- Kiểm soát rủi ro mô hình (Model Risk)
- Phân định rõ trách nhiệm giữa hệ thống AI và con người
- Ngăn ngừa việc sử dụng kết quả định giá sai mục đích

### 1.2. Phạm vi áp dụng

Chính sách áp dụng cho:

- Định giá phục vụ tín dụng ngân hàng
- Định giá tài sản bảo đảm
- Định giá tham khảo phục vụ quản trị rủi ro

Không áp dụng trực tiếp cho:

- Mua bán dân sự ngoài hệ thống ngân hàng
- Đầu cơ, môi giới, quảng cáo giá

---

## II. NGUYÊN TẮC ĐỊNH GIÁ CỐT LÕI

### 2.1. Nguyên tắc phù hợp pháp luật

Mọi kết quả định giá phải:

- Phù hợp Tiêu chuẩn Thẩm định giá Việt Nam
- Không trái quy định của pháp luật đất đai, nhà ở, kinh doanh BĐS
- Không thay thế trách nhiệm pháp lý của thẩm định viên

### 2.2. Nguyên tắc thận trọng (Prudence Principle)

Hệ thống AVM được thiết kế theo hướng **bảo thủ**, ưu tiên:

- Hạn chế định giá cao hơn giá trị thị trường
- Giảm thiểu rủi ro mất vốn cho tổ chức tín dụng

### 2.3. Nguyên tắc không tự quyết định (Non‑Autonomous Decision)

- Hệ thống AVM **không có quyền tự phê duyệt giá trị tài sản**
- Giá trị cuối cùng chỉ có hiệu lực khi được con người xem xét và chấp thuận theo thẩm quyền

### 2.4. Nguyên tắc minh bạch và truy vết

Mỗi kết quả định giá phải:

- Có thể giải thích được (Explainable)
- Có nhật ký dữ liệu và phiên bản mô hình
- Có khả năng truy vết ngược (Audit trail)

---

## III. ĐỊNH NGHĨA GIÁ TRỊ ĐƯỢC SỬ DỤNG

### 3.1. Giá trị thị trường (Market Value)

Giá trị thị trường là mức giá ước tính của tài sản tại thời điểm định giá, trong điều kiện:

- Giao dịch tự nguyện
- Bên mua – bên bán có đầy đủ thông tin
- Không chịu áp lực bất thường

### 3.2. Giá trị xử lý rủi ro (Risk‑Adjusted Value)

Giá trị xử lý rủi ro là giá trị thị trường sau khi xem xét các yếu tố:

- Thanh khoản
- Pháp lý
- Quy hoạch
- Vị trí đặc thù

Giá trị này **chỉ mang tính tham khảo** cho quản trị rủi ro nội bộ.

### 3.3. Giá trị không được phép sử dụng

Hệ thống **không cung cấp** và **không công nhận**:

- Giá đầu cơ
- Giá kỳ vọng tương lai
- Giá quảng cáo môi giới

---

## IV. CÁC PHƯƠNG PHÁP ĐỊNH GIÁ ĐƯỢC PHÉP

### 4.1. Phương pháp so sánh thị trường

Được áp dụng khi:

- Có đủ dữ liệu giao dịch hoặc chào bán phù hợp
- Tài sản có tính phổ biến

Phương pháp này được ưu tiên trong hệ thống AVM.

### 4.2. Phương pháp chi phí

Được áp dụng để:

- Tham chiếu giá trị công trình xây dựng
- Tách giá trị đất và công trình

### 4.3. Phương pháp thu nhập

Được sử dụng trong trường hợp:

- Tài sản tạo ra dòng tiền ổn định
- Có dữ liệu cho thuê đáng tin cậy

Kết quả phương pháp này **không được sử dụng độc lập**.

---

## V. CÁC PHƯƠNG PHÁP KHÔNG ĐƯỢC PHÉP

Hệ thống AVM **không được phép**:

- Tự động suy diễn giá từ tin đồn thị trường
- Sử dụng dữ liệu không kiểm chứng
- Áp dụng phong thủy làm yếu tố quyết định

---

## VI. QUẢN TRỊ RỦI RO PHÁP LÝ

### 6.1. Nguyên tắc pháp lý chung

Chỉ định giá các tài sản có:

- Tình trạng pháp lý rõ ràng
- Có khả năng xử lý tài sản khi cần thiết

### 6.2. Các trường hợp loại trừ bắt buộc

Hệ thống phải tự động loại trừ:

- Giấy tay, vi bằng
- Tài sản tranh chấp
- Tài sản bị kê biên

---

## VII. RỦI RO QUY HOẠCH

### 7.1. Nguyên tắc tiếp cận

- Quy hoạch là yếu tố rủi ro, không phải yếu tố tạo giá trị
- Diện tích không được công nhận không được tính giá trị đất ở

### 7.2. Xử lý thông tin quy hoạch

- Thông tin quy hoạch chỉ mang tính tham khảo
- Bắt buộc xác minh thủ công trong các trường hợp nhạy cảm

---

## VIII. RỦI RO VỊ TRÍ ĐẶC THÙ

### 8.1. Quan điểm chính sách

- Yếu tố vị trí đặc thù chỉ được xem là yếu tố **tham khảo nghiệp vụ**
- Không được AI sử dụng làm quyết định định lượng cuối cùng

### 8.2. Trách nhiệm đánh giá

- Việc đánh giá tác động vị trí thuộc trách nhiệm thẩm định viên

---

## IX. KIỂM SOÁT CHẤT LƯỢNG DỮ LIỆU

### 9.1. Nguồn dữ liệu

- Dữ liệu giao dịch
- Dữ liệu chào bán
- Dữ liệu công khai

### 9.2. Nguyên tắc sử dụng dữ liệu

- Ưu tiên dữ liệu đã kiểm chứng
- Không sử dụng dữ liệu bất thường

---

## X. CƠ CHẾ ĐÁNH GIÁ ĐỘ TIN CẬY

### 10.1. Mục đích

Điểm tin cậy được sử dụng để:

- Hỗ trợ phân luồng xử lý hồ sơ
- Không dùng làm quyết định giá

### 10.2. Nguyên tắc

- Điểm tin cậy phản ánh chất lượng dữ liệu
- Không phản ánh mức độ sinh lời

---

## XI. PHÂN LUỒNG XỬ LÝ HỒ SƠ

### 11.1. Hồ sơ đủ điều kiện hỗ trợ AVM

- Pháp lý rõ ràng
- Dữ liệu thị trường đầy đủ

### 11.2. Hồ sơ bắt buộc xử lý thủ công

- Tài sản dị biệt
- Tài sản thiếu dữ liệu

---

## XII. TRÁCH NHIỆM VÀ THẨM QUYỀN

### 12.1. Trách nhiệm hệ thống

- Tính toán
- Gợi ý
- Cảnh báo rủi ro

### 12.2. Trách nhiệm con người

- Quyết định cuối cùng
- Chịu trách nhiệm pháp lý

---

## XIII. QUẢN TRỊ MÔ HÌNH (MODEL GOVERNANCE)

### 13.1. Phiên bản mô hình

- Mỗi kết quả định giá phải gắn với phiên bản mô hình

### 13.2. Kiểm định định kỳ

- Mô hình phải được rà soát định kỳ

---

## XIV. KIỂM TOÁN VÀ BÁO CÁO

### 14.1. Kiểm toán nội bộ

- Có quyền truy xuất toàn bộ log

### 14.2. Báo cáo sai lệch

- Bắt buộc báo cáo khi phát hiện sai lệch lớn

---

## XV. GIỚI HẠN TRÁCH NHIỆM

- Hệ thống AVM không thay thế thẩm định viên
- Nhà phát triển không chịu trách nhiệm quyết định tín dụng

---

## XVI. HIỆU LỰC THI HÀNH

Chính sách này có hiệu lực kể từ ngày ban hành và là tài liệu nền tảng cho toàn bộ hoạt động định giá bất động sản trong hệ thống AVM.

---

<!-- # CHÍNH SÁCH ĐỊNH GIÁ & PHƯƠNG PHÁP LUẬN (VALUATION POLICY & METHODOLOGY)

**Phiên bản:** 2.0 (Enterprise Standard)
**Áp dụng cho:** Hệ thống AVM Real Estate AI Platform
**Tham chiếu:** Tiêu chuẩn Thẩm định giá Việt Nam (TĐGVN 01 - TĐGVN 13)

---

## 1. NGUYÊN TẮC QUẢN TRỊ RỦI RO & ĐỊNH NGHĨA GIÁ TRỊ

### 1.1. Cơ sở giá trị

Hệ thống cung cấp 02 loại giá trị cho mỗi hồ sơ:

1.  **Giá trị thị trường (Market Value - MV):** Mức giá ước tính tài sản được giao dịch trên thị trường mở, trong điều kiện thương mại bình thường, bên mua và bên bán có đủ thông tin và hành động tự nguyện.
2.  **Giá trị thanh lý cưỡng chế (Forced Sale Value - FSV):** Mức giá ước tính có thể thu hồi nhanh (trong vòng 3-6 tháng).
    - _Công thức:_ $FSV = MV \times LiquidityDiscountFactor$
    - _Hệ số mặc định:_ 0.85 (Nhà phố), 0.90 (Chung cư), 0.70 (Đất nền tỉnh).

### 1.2. Nguyên tắc thận trọng (Prudence Principle)

Trong trường hợp các phương pháp định giá cho ra kết quả chênh lệch:

- Nếu độ lệch chuẩn (StdDev) < 10%: Lấy giá trị trung bình có trọng số (Weighted Average).
- Nếu độ lệch chuẩn (StdDev) > 10%: Lấy giá trị cận dưới (Lower Bound) của khoảng tin cậy 90%.

---

## 2. CHI TIẾT CÁC PHƯƠNG PHÁP ĐỊNH GIÁ (MODEL LOGIC)

Hệ thống sử dụng mô hình lai (Hybrid Valuation) kết hợp giữa các phương pháp sau:

### 2.1. Phương pháp So sánh (Market Comparison Approach) - _Trọng số cao nhất_

Áp dụng cho: Nhà phố, Chung cư, Đất nền.

**Quy tắc chọn Tài sản so sánh (TSSS):**

- **Số lượng:** Tối thiểu 03, tối đa 05 TSSS.
- **Phạm vi:**
  - Nội thành: Bán kính 500m - 1km.
  - Ngoại thành: Bán kính 2km - 3km.
- **Thời gian:** Dữ liệu giao dịch/chào bán trong vòng 6 tháng gần nhất.

**Lưới điều chỉnh (Adjustment Grid):**
Hệ thống tự động tính toán tỷ lệ điều chỉnh theo ma trận sau:

| Yếu tố so sánh       | Mức điều chỉnh tối đa cho phép | Logic Code                                           |
| :------------------- | :----------------------------- | :--------------------------------------------------- |
| **Quy mô diện tích** | +/- 15%                        | Logarithmic scaling (Diện tích nhỏ đơn giá cao hơn). |
| **Vị trí (Hẻm/Phố)** | +/- 30%                        | Dựa trên độ rộng hẻm và khoảng cách ra đường chính.  |
| **Mặt tiền**         | +/- 10%                        | Thưởng hệ số nếu mặt tiền > 5m.                      |
| **Hình dáng đất**    | -20% đến 0%                    | Trừ nếu méo mó, tóp hậu, hình tam giác.              |
| **Pháp lý**          | -100% đến 0%                   | Xem mục 3.                                           |

### 2.2. Phương pháp Chi phí (Cost Approach)

Áp dụng cho: Nhà phố, Biệt thự (để tách giá trị đất & công trình).

- **Giá trị BĐS = Giá trị Đất (theo so sánh) + Giá trị Công trình còn lại**
- **Giá trị Công trình còn lại = Diện tích sàn xây dựng $\times$ Đơn giá xây mới $\times$ Tỷ lệ chất lượng còn lại.**
  - _Đơn giá xây mới (Standard):_
    - Nhà cấp 4: 3.5 - 4.0 triệu/m2.
    - Nhà phố kiên cố (BTCT): 6.0 - 7.0 triệu/m2.
    - Biệt thự cao cấp: > 10.0 triệu/m2.
  - _Khấu hao (Depreciation):_ Theo phương pháp đường thẳng, tuổi thọ kinh tế 50 năm.

### 2.3. Phương pháp Thu nhập (Income Approach) - _Tham khảo_

Áp dụng cho: BĐS đang cho thuê, Tòa nhà văn phòng.

- Công thức: $V = NOI / CapRate$
- _CapRate (Tỷ suất vốn hóa):_
  _ Nhà phố nội thành: 2.5% - 3.5%.
  _ Chung cư: 4.5% - 5.5%.

---

## 3. CÁC QUY TẮC KHẤU TRỪ RỦI RO ĐẶC THÙ (VIETNAM SPECIFIC RULES)

Đây là phần **Logic cứng (Hard Rules)** mà hệ thống AI bắt buộc phải áp dụng để tránh định giá sai.

### 3.1. Rủi ro Pháp lý (Legal Risk)

| Tình trạng pháp lý                       | Hành động của Hệ thống    | Hệ số Điều chỉnh (Adjustment) |
| :--------------------------------------- | :------------------------ | :---------------------------- |
| **Sổ đỏ/Sổ hồng đầy đủ (Cá nhân)**       | Chấp nhận                 | 1.00 (Base)                   |
| **Sổ hồng (Chủ đầu tư - chưa sang tên)** | Chấp nhận có điều kiện    | 0.95                          |
| **Hợp đồng mua bán (Dự án uy tín)**      | Chấp nhận                 | 0.90                          |
| **Đang chờ cấp sổ (Có giấy hẹn)**        | Flag: Cần xác minh        | 0.90                          |
| **Giấy tay / Vi bằng / Sổ chung**        | **TỪ CHỐI (AUTO REJECT)** | N/A                           |
| **Đang bị kê biên / Tranh chấp**         | **TỪ CHỐI (AUTO REJECT)** | N/A                           |

### 3.2. Rủi ro Quy hoạch (Zoning Risk)

- **Quy hoạch giao thông (Lộ giới):** Diện tích nằm trong lộ giới không được công nhận giá trị đất ở. Chỉ tính 10% giá trị (đền bù hoa màu) hoặc 0% tùy chính sách ngân hàng.
- **Quy hoạch treo:** Áp dụng mức giảm giá **20% - 30%** so với thị trường.

### 3.3. Rủi ro Vị trí & Phong thủy (Location & Feng Shui)

Các yếu tố này được phát hiện qua `listing_intelligence` (xử lý ảnh/bản đồ) và áp dụng trừ giá:

- **Đường đâm (T-junction):** Trừ 10% - 15%.
- **Gần nghĩa trang, đình chùa (<50m):** Trừ 10%.
- **Gần trạm biến áp, bãi rác:** Trừ 5% - 10%.
- **Ngõ cụt (cuối ngõ):** Trừ 5%.
- **Tóp hậu (Rear width < Front width):** Trừ theo tỷ lệ tóp, tối đa 15%.
- **Hẻm xe máy (< 2.0m):** Đơn giá đất thấp hơn 20% so với hẻm xe hơi.

---

## 4. CƠ CHẾ KIỂM SOÁT MÔ HÌNH (MODEL GOVERNANCE)

### 4.1. Độ tin cậy (Confidence Score)

Mỗi định giá phải đi kèm một điểm tin cậy (0.0 - 1.0).

- **High Confidence (> 0.8):** Dữ liệu TSSS phong phú, độ lệch chuẩn thấp, pháp lý sạch. -> _Đề xuất duyệt tự động (L1)._
- **Medium Confidence (0.5 - 0.8):** Dữ liệu ít hoặc phân tán. -> _Yêu cầu Thẩm định viên review._
- **Low Confidence (< 0.5):** Không đủ dữ liệu hoặc tài sản dị biệt. -> _Chuyển hồ sơ sang định giá thủ công hoàn toàn._

### 4.2. Flag cảnh báo gian lận (Fraud Flags)

Hệ thống sẽ Flag hồ sơ nếu:

1.  Giá trị định giá cao hơn giá chào bán trung bình khu vực > 30% (Nghi vấn đẩy giá trục lợi).
2.  Lịch sử giao dịch của BĐS thay đổi chủ sở hữu > 3 lần trong 6 tháng (Nghi vấn lướt sóng/thổi giá). -->
