# REGULATORY MAPPING

_Document initialized automatically._

# REGULATORY MAPPING

## HỆ THỐNG ADVANCED AVM – HYBRID AI + THẨM ĐỊNH THỦ CÔNG

---

**Phiên bản:** 1.0
**Ngày hiệu lực:** …/…/20…
**Phạm vi áp dụng:** Toàn bộ hệ thống định giá BĐS sử dụng Advanced AVM
**Đối tượng sử dụng:** Ngân hàng, Quỹ đầu tư, Đơn vị Due Diligence, Kiểm toán nội bộ/độc lập

---

## 1. MỤC ĐÍCH TÀI LIỆU

Tài liệu này được xây dựng nhằm:

- Mapping đầy đủ các **yêu cầu pháp lý và chuẩn mực nghề nghiệp tại Việt Nam** với thiết kế và vận hành của hệ thống Advanced AVM.
- Chứng minh rằng hệ thống:

  - Tuân thủ Luật Đất đai và các nguyên tắc pháp luật liên quan;
  - Phù hợp với Tiêu chuẩn Thẩm định giá Việt Nam;
  - Phù hợp với tinh thần các Thông tư hướng dẫn thẩm định giá, tín dụng và quản trị rủi ro;
  - Không chuyển giao trách nhiệm pháp lý cho AI hoặc LLM.

- Làm cơ sở phục vụ:

  - Phê duyệt nội bộ;
  - Kiểm toán;
  - Thanh tra, hậu kiểm;
  - Due Diligence trong giao dịch tài chính.

---

## 2. NGUYÊN TẮC TUÂN THỦ CỐT LÕI

Hệ thống Advanced AVM được thiết kế dựa trên các nguyên tắc tuân thủ sau:

1. **AI chỉ là công cụ hỗ trợ** – không phải chủ thể pháp lý.
2. **Thẩm định viên chịu trách nhiệm cuối cùng** về kết quả định giá.
3. **LLM không đưa ra kết luận giá trị** và không có quyền phê duyệt.
4. **Mọi quyết định trọng yếu đều có sự tham gia của con người.**
5. **Có khả năng giải trình, truy vết và tái lập** tại mọi thời điểm.

---

## 3. PHẠM VI QUY ĐỊNH ĐƯỢC MAPPING

Tài liệu này tập trung vào ba nhóm quy định chính:

1. Luật Đất đai và các nguyên tắc pháp lý liên quan đến quyền sử dụng đất.
2. Tiêu chuẩn Thẩm định giá Việt Nam.
3. Các Thông tư và hướng dẫn liên quan đến thẩm định giá, tín dụng và quản trị rủi ro.

---

# PHẦN I – MAPPING THEO LUẬT ĐẤT ĐAI

## 4. NGUYÊN TẮC CHUNG CỦA LUẬT ĐẤT ĐAI

| Quy định                           | Yêu cầu                                        | Cách hệ thống đáp ứng                                            |
| ---------------------------------- | ---------------------------------------------- | ---------------------------------------------------------------- |
| Quyền sử dụng đất là quyền tài sản | Chỉ định giá tài sản có quyền sử dụng hợp pháp | Hệ thống bắt buộc kiểm tra tình trạng pháp lý trước khi định giá |
| Đất thuộc sở hữu toàn dân          | Không suy diễn quyền sở hữu ngoài pháp luật    | AVM chỉ phản ánh quyền sử dụng đất hợp pháp                      |
| Sử dụng đất đúng mục đích          | Giá trị phụ thuộc mục đích sử dụng             | Schema dữ liệu phân loại rõ mục đích sử dụng                     |

---

## 5. TÌNH TRẠNG PHÁP LÝ THỬA ĐẤT

| Quy định                    | Yêu cầu                               | Cách hệ thống đáp ứng            |
| --------------------------- | ------------------------------------- | -------------------------------- |
| Có Giấy chứng nhận hợp pháp | Điều kiện tiên quyết để định giá      | Hồ sơ thiếu GCN → dừng quy trình |
| Không tranh chấp            | Tài sản tranh chấp không đủ điều kiện | Cờ rủi ro pháp lý bắt buộc       |
| Không bị kê biên            | Phải loại trừ tài sản bị hạn chế      | Checklist pháp lý bắt buộc       |

---

## 6. QUY HOẠCH VÀ HẠN CHẾ SỬ DỤNG ĐẤT

| Quy định           | Yêu cầu                           | Cách hệ thống đáp ứng                |
| ------------------ | --------------------------------- | ------------------------------------ |
| Tuân thủ quy hoạch | Không định giá vượt quyền sử dụng | Diện tích dính quy hoạch bị loại trừ |
| Lộ giới, hành lang | Phải phản ánh giảm giá trị        | Áp dụng hệ số điều chỉnh bắt buộc    |
| Quy hoạch treo     | Phản ánh rủi ro                   | Risk flag trong báo cáo              |

---

# PHẦN II – MAPPING THEO TIÊU CHUẨN THẨM ĐỊNH GIÁ VIỆT NAM

## 7. NGUYÊN TẮC CƠ BẢN TRONG THẨM ĐỊNH GIÁ

| Tiêu chuẩn | Yêu cầu                     | Cách hệ thống đáp ứng                |
| ---------- | --------------------------- | ------------------------------------ |
| Khách quan | Không thiên lệch            | AI xử lý dữ liệu, con người kết luận |
| Độc lập    | Không xung đột lợi ích      | Phân tách vai trò rõ ràng            |
| Thận trọng | Ưu tiên an toàn             | Chọn kịch bản bảo thủ                |
| Phù hợp    | Phương pháp phù hợp tài sản | Rule-based activation                |

---

## 8. NGUYÊN TẮC SỬ DỤNG CAO NHẤT VÀ TỐT NHẤT

| Tiêu chuẩn                | Yêu cầu                  | Cách hệ thống đáp ứng             |
| ------------------------- | ------------------------ | --------------------------------- |
| Dựa trên pháp lý hiện tại | Không giả định trái phép | AVM khóa giả định chuyển mục đích |
| Có tính khả thi           | Không suy đoán viển vông | Chỉ dùng dữ liệu đã xảy ra        |

---

## 9. PHƯƠNG PHÁP SO SÁNH

| Quy định             | Yêu cầu        | Cách hệ thống đáp ứng     |
| -------------------- | -------------- | ------------------------- |
| TSSS tương đồng      | So sánh hợp lý | Bộ lọc đa tiêu chí        |
| Điều chỉnh có căn cứ | Có giải trình  | Adjustment grid minh bạch |
| Dữ liệu cập nhật     | Không lỗi thời | Giới hạn thời gian        |

---

## 10. PHƯƠNG PHÁP CHI PHÍ

| Quy định              | Yêu cầu          | Cách hệ thống đáp ứng |
| --------------------- | ---------------- | --------------------- |
| Tách đất – công trình | Không gộp        | Module tách riêng     |
| Khấu hao hợp lý       | Phản ánh thực tế | Khấu hao chuẩn hóa    |

---

## 11. PHƯƠNG PHÁP THU NHẬP

| Quy định             | Yêu cầu            | Cách hệ thống đáp ứng          |
| -------------------- | ------------------ | ------------------------------ |
| Có dòng tiền ổn định | Điều kiện bắt buộc | Nếu không đủ → không kích hoạt |
| Tỷ suất hợp lý       | Không tùy tiện     | Cap rate theo thị trường       |

---

# PHẦN III – MAPPING THEO THÔNG TƯ LIÊN QUAN

## 12. NGUYÊN TẮC ĐỊNH GIÁ PHỤC VỤ TÍN DỤNG

| Nguyên tắc              | Yêu cầu                 | Cách hệ thống đáp ứng  |
| ----------------------- | ----------------------- | ---------------------- |
| Quản trị rủi ro         | Không chạy theo giá cao | Confidence & Risk band |
| Không phụ thuộc mô hình | Có review thủ công      | Human-in-the-loop      |
| Có hồ sơ lưu trữ        | Phục vụ hậu kiểm        | Audit trail đầy đủ     |

---

## 13. NGUYÊN TẮC QUẢN TRỊ RỦI RO MÔ HÌNH

| Nguyên tắc         | Yêu cầu         | Cách hệ thống đáp ứng |
| ------------------ | --------------- | --------------------- |
| Không hộp đen      | Có giải thích   | Lưu input/output      |
| Kiểm soát sai lệch | Phát hiện drift | Monitoring định kỳ    |
| Có cơ chế dừng     | Ngăn rủi ro     | Kill-switch nghiệp vụ |

---

## 14. TRÁCH NHIỆM PHÁP LÝ

| Chủ thể        | Trách nhiệm                        |
| -------------- | ---------------------------------- |
| AI / AVM       | Không chịu trách nhiệm pháp lý     |
| LLM            | Hỗ trợ diễn giải, không quyết định |
| Thẩm định viên | Chịu trách nhiệm chuyên môn        |
| Doanh nghiệp   | Chịu trách nhiệm pháp lý           |

---

## 15. KẾT LUẬN TUÂN THỦ

Hệ thống Advanced AVM:

- Phù hợp với Luật Đất đai;
- Tuân thủ Tiêu chuẩn Thẩm định giá Việt Nam;
- Phù hợp tinh thần các Thông tư liên quan;
- Đủ điều kiện sử dụng trong môi trường ngân hàng, quỹ và DD;
- Không chuyển giao trách nhiệm cho AI.

**Giá trị định giá cuối cùng luôn là kết quả của thẩm định viên có thẩm quyền.**
