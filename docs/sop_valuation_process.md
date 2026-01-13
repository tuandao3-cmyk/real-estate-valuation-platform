# SOP VALUATION PROCESS

_Document initialized automatically._

# SOP ĐỊNH GIÁ BẤT ĐỘNG SẢN

## (STANDARD OPERATING PROCEDURE – HYBRID AVM + THẨM ĐỊNH THỦ CÔNG)

---

**Phiên bản:** 1.0 (Internal Use – Audit Ready)
**Áp dụng cho:** Công ty Thẩm định giá / Đơn vị triển khai AVM cho Ngân hàng, Quỹ, Due Diligence
**Phạm vi:** Định giá BĐS phục vụ tín dụng, đầu tư, tham chiếu và DD
**Căn cứ:** Tiêu chuẩn Thẩm định giá Việt Nam (TĐGVN), Quy chế quản trị rủi ro mô hình nội bộ

---

## I. MỤC ĐÍCH & NGUYÊN TẮC CHUNG

### 1. Mục đích SOP

Tài liệu này quy định **quy trình tác nghiệp chuẩn** cho hoạt động định giá bất động sản sử dụng **mô hình lai (Hybrid AVM)**, kết hợp giữa:

- Hệ thống phân tích tự động (AVM)
- Thẩm định viên có chứng chỉ hành nghề
- Cơ chế phê duyệt và kiểm soát nội bộ

Mục tiêu của SOP:

- Đảm bảo **tính nhất quán** trong quy trình định giá
- Đảm bảo **tuân thủ tiêu chuẩn thẩm định giá Việt Nam**
- Đảm bảo **truy vết được (traceability)** toàn bộ quyết định
- Ngăn chặn việc hiểu nhầm **AI là chủ thể định giá**

---

### 2. Nguyên tắc cốt lõi

1. **AI không phải thẩm định viên**
2. **AI không ra quyết định giá**
3. **Mọi giá trị cuối cùng đều do con người chịu trách nhiệm**
4. **Mọi bước đều phải để lại audit trail**
5. **Không có định giá "tự động hoàn toàn" đối với tài sản có rủi ro**

---

## II. TỔNG QUAN QUY TRÌNH ĐỊNH GIÁ

### 1. Sơ đồ tổng quát quy trình

```
Khách hàng / Ngân hàng
        ↓
[1] Nhận hồ sơ
        ↓
[2] Kiểm tra pháp lý
        ↓
[3] Phân tích thị trường
        ↓
[4] AVM xử lý & phân tích
        ↓
[5] Thẩm định viên review
        ↓
[6] Phê duyệt nội bộ
        ↓
[7] Lập & phát hành báo cáo
```

---

### 2. Phân vai tổng quát

| Chủ thể               | Vai trò trong SOP                      |
| --------------------- | -------------------------------------- |
| Hệ thống AVM          | Phân tích dữ liệu, gợi ý, cảnh báo     |
| LLM                   | Soạn thảo nhận xét, chuẩn hóa ngôn ngữ |
| Thẩm định viên        | Đánh giá chuyên môn, quyết định giá    |
| Trưởng bộ phận        | Phê duyệt nghiệp vụ                    |
| Hội đồng / Khách hàng | Quyết định sử dụng kết quả             |

---

## III. QUY TRÌNH CHI TIẾT THEO TỪNG BƯỚC

---

## BƯỚC 1: NHẬN HỒ SƠ ĐỊNH GIÁ

### 1.1. Mục tiêu

- Ghi nhận đầy đủ thông tin đầu vào
- Đảm bảo hồ sơ đủ điều kiện để xử lý tiếp
- Tránh tiếp nhận hồ sơ không đủ căn cứ pháp lý

---

### 1.2. Thành phần hồ sơ

Hồ sơ định giá tối thiểu bao gồm:

- Đơn yêu cầu định giá
- Thông tin mục đích định giá
- Hồ sơ pháp lý tài sản (bản sao)
- Thông tin người sử dụng kết quả

---

### 1.3. Vai trò hệ thống AI

- Tự động kiểm tra checklist hồ sơ
- Phân loại mục đích định giá
- Gán mã hồ sơ và timestamp

**Lưu ý:** AI **không đánh giá giá trị** tại bước này.

---

### 1.4. Điểm kiểm soát thủ công

- Nhân viên tiếp nhận xác nhận hồ sơ hợp lệ
- Ký xác nhận tiếp nhận trên hệ thống

---

## BƯỚC 2: KIỂM TRA PHÁP LÝ TÀI SẢN

### 2.1. Mục tiêu

- Xác định tính hợp pháp của tài sản
- Phát hiện sớm rủi ro không thể định giá

---

### 2.2. Nội dung kiểm tra

- Loại giấy chứng nhận
- Chủ sở hữu
- Hạn chế quyền sử dụng
- Tình trạng tranh chấp, kê biên

---

### 2.3. Vai trò hệ thống AVM

- Đối chiếu loại pháp lý với rule engine
- Gắn nhãn rủi ro (Legal Risk Flag)
- Tự động **TỪ CHỐI** hồ sơ thuộc danh mục cấm

---

### 2.4. Vai trò thẩm định viên

- Xác minh nội dung pháp lý phức tạp
- Quyết định có tiếp tục định giá hay không

---

### 2.5. Audit trail

- Lưu trạng thái pháp lý
- Lưu quyết định chấp nhận / từ chối
- Lưu người chịu trách nhiệm

---

## BƯỚC 3: PHÂN TÍCH THỊ TRƯỜNG

### 3.1. Mục tiêu

- Hiểu bối cảnh thị trường tại thời điểm định giá
- Tránh sử dụng dữ liệu không phù hợp

---

### 3.2. Nội dung phân tích

- Xu hướng giá khu vực
- Thanh khoản
- Nguồn cung – cầu
- Biến động bất thường

---

### 3.3. Vai trò hệ thống AVM

- Tổng hợp dữ liệu giao dịch
- Chuẩn hóa dữ liệu so sánh
- Phát hiện outlier

---

### 3.4. Vai trò LLM

- Tóm tắt diễn biến thị trường
- Chuẩn hóa ngôn ngữ nhận xét

**LLM không được phép đưa ra kết luận giá.**

---

## BƯỚC 4: AVM XỬ LÝ & PHÂN TÍCH

### 4.1. Mục tiêu

- Hỗ trợ thẩm định viên bằng phân tích định lượng

---

### 4.2. Phạm vi xử lý của AVM

- Phương pháp so sánh
- Phương pháp chi phí
- Phương pháp thu nhập (nếu phù hợp)

---

### 4.3. Nguyên tắc vận hành

- AVM chỉ tạo **kết quả trung gian**
- AVM không sinh "giá trị cuối cùng"

---

### 4.4. Kết quả AVM cung cấp

- Khoảng giá tham chiếu
- Confidence Score
- Danh sách rủi ro

---

## BƯỚC 5: THẨM ĐỊNH VIÊN REVIEW

### 5.1. Mục tiêu

- Áp dụng chuyên môn con người
- Điều chỉnh các yếu tố AI không nhận diện được

---

### 5.2. Nội dung review

- Soát lại TSSS
- Kiểm tra logic điều chỉnh
- Đánh giá hiện trường (nếu cần)

---

### 5.3. Quyền override

- Thẩm định viên có toàn quyền ghi đè kết quả AVM
- Mọi override phải có lý do và bằng chứng

---

## BƯỚC 6: PHÊ DUYỆT NỘI BỘ

### 6.1. Mục tiêu

- Kiểm soát rủi ro cấp tổ chức

---

### 6.2. Cấp phê duyệt

- Cấp 1: Trưởng bộ phận
- Cấp 2: Hội đồng (nếu có)

---

### 6.3. Nội dung phê duyệt

- Phù hợp mục đích định giá
- Tuân thủ SOP
- Rủi ro đã được phản ánh đầy đủ

---

## BƯỚC 7: LẬP & PHÁT HÀNH BÁO CÁO

### 7.1. Mục tiêu

- Phát hành chứng thư đúng chuẩn

---

### 7.2. Vai trò LLM

- Soạn thảo nhận xét
- Chuẩn hóa câu chữ

---

### 7.3. Trách nhiệm ký

- Thẩm định viên ký
- Người đại diện pháp luật chịu trách nhiệm

---

## IV. KIỂM SOÁT & TUÂN THỦ

- Mọi hồ sơ đều có audit trail
- Định kỳ rà soát SOP
- Không sử dụng SOP cho mục đích ngoài phạm vi

---

**KẾT THÚC SOP**
