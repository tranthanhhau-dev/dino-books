# 🦖📚 TIỆM SÁCH DINO
### Website Bán Sách Tiếng Anh Cũ Tuyển Chọn Cho Thiếu Nhi & Trẻ Vị Thành Niên

Chào mừng bạn đến với **Tiệm Sách Dino**! Đây là hệ thống web app thương mại điện tử hoàn chỉnh, hiện đại, được thiết kế chuyên biệt cho việc kinh doanh dòng **sách tiếng Anh cũ (secondhand)** cho trẻ em từ 0 - 16 tuổi.

---

## 🎨 1. Logo Thương Hiệu "Tiệm Sách Dino"
- **Ý tưởng:** Bé khủng long Dino xanh đáng yêu đội mũ thám hiểm / đeo kính thông thái đang say mê đọc cuốn sách tiếng Anh rực rỡ, xung quanh là thiên nhiên tươi mát, lá cây xanh và những ngôi sao sáng tượng trưng cho tri thức và niềm vui học tập.
- **Tông màu chủ đạo:** Các sắc xanh tươi sáng, năng động (xanh lá cây Dino Emerald/Green, xanh ngọc Teal, xanh đại dương Sky/Ocean Blue) tạo cảm giác tươi mới, thân thiện, tràn đầy sức sống.
- **Vị trí file logo:**
  - `store/static/images/logo.png`

---

## 🌟 2. Các Tính Năng Hiện Đại Của Website

### A. Dành Cho Khách Hàng (Phụ Huynh & Học Sinh)
1. **Trang chủ ấm cúng, trực quan:**
   - Hero banner bắt mắt, slogan "Sách hay cho bé - Giá hời cho mẹ".
   - Bộ chọn độ tuổi nhanh dạng pill card: 0-3 tuổi, 4-6 tuổi, 7-9 tuổi, 10-12 tuổi, 13+ Teen.
   - Mục **"Giá Hời Hôm Nay"** (Hot Deals giảm sâu đến 70%).
   - Mục **"Sách Mới Vừa Lên Kệ"** cập nhật liên tục.
   - **Bảng Quy Chuẩn Đánh Giá Tình Trạng Sách**: Minh bạch từng mức độ mới (Like New 98-99%, Rất tốt 90-95%, Tốt 80-85%, Khá 70-75%) giúp ba mẹ hoàn toàn yên tâm khi mua sách cũ.
   - Cam kết đổi trả 3 ngày nếu sách không đúng mô tả thực tế.

2. **Kho sách & Bộ lọc đa tiêu chí (Smart Filter):**
   - Lọc theo **Độ tuổi** (0-3, 4-6, 7-9, 10-12, 13+).
   - Lọc theo **Thể loại** (Board Books, Picture Books, Phonics, Early Readers, Chapter Books, Graphic Novels, Young Adult, STEM...).
   - Lọc theo **Tình trạng sách cũ** (Độ mới % rõ ràng).
   - Lọc theo **Loại bìa** (Bìa bồi cứng, Bìa cứng Hardcover, Bìa mềm Paperback).
   - Lọc theo **Khoảng giá** & Sắp xếp (Mới nhất, Giá tăng dần, Giá giảm dần, Độ mới cao nhất, Lượt xem).

3. **Trang chi tiết sách tối ưu cho sách secondhand:**
   - Bộ ảnh chụp thực tế từng góc cạnh (Bìa trước, bìa sau, gáy sách, trang ruột bên trong).
   - Đánh giá cụ thể tình trạng cuốn sách đang bán (Ví dụ: "Gáy nguyên vẹn, ruột sạch tinh, không viết vẽ").
   - So sánh giá thanh lý với giá bìa gốc (% tiết kiệm).
   - Thông số chi tiết: Trình độ đọc (Lexile / Guided Reading / CEFR), Nhà xuất bản (Oxford, Usborne, Scholastic...), Số trang, Năm xuất bản, ISBN.
   - Nút **"Yêu cầu Tiệm Dino quay video thật cuốn này qua Zalo"**.

4. **Giỏ hàng & Thanh toán tiện lợi (COD):**
   - Thanh tiến trình **Freeship toàn quốc** (Mua thêm ...đ để được miễn phí ship).
   - Hỗ trợ thanh toán **COD (Tiền mặt khi nhận sách)**: Nhận sách tại nhà, được mở hộp đồng kiểm tra chất lượng thực tế trước khi thanh toán cho bưu tá, không cần chuyển khoản hay quét mã phức tạp.

5. **Tra cứu tiến độ đơn hàng trực tuyến:**
   - Khách chỉ cần nhập Số điện thoại hoặc Mã đơn hàng để xem thanh trạng thái đơn: *Đã nhận đơn &rarr; Đã xác nhận &rarr; Đang gói sách &rarr; Đang giao hàng &rarr; Hoàn thành*.
   - Hiển thị mã vận đơn bưu cục (GHTK / Viettel Post).

6. **Chức năng Ký Gửi & Thu Mua Sách Cũ:**
   - Trang tiếp nhận thông tin từ phụ huynh muốn bán lại hoặc ký gửi sách của bé đã đọc xong.
   - Giúp tiệm luôn có nguồn sách tiếng Anh cũ chất lượng dồi dào.

---

### B. Dành Cho Chủ Tiệm (Quản Trị Viên)
Truy cập qua đường dẫn: `http://127.0.0.1:8088/admin/`
- **Tài khoản mặc định:** `admin`
- **Mật khẩu:** `admindino123`

Các chức năng quản trị:
- **Thêm/Sửa/Xóa sách:** Upload ảnh chụp thật, nhập tình trạng độ mới %, giá bán, tồn kho, phân loại thể loại, độ tuổi, cấp độ đọc.
- **Quản lý Đơn hàng:** Xem danh sách đơn, cập nhật trạng thái thanh toán, đổi trạng thái đơn (Chờ xử lý, Đã xác nhận, Đang gói sách, Đang giao hàng, Hoàn thành), nhập mã vận đơn.
- **Quản lý Ký gửi / Thu mua:** Tiếp nhận thông tin phụ huynh gửi ảnh sách cũ thanh lý để liên hệ báo giá.
- **Quản lý Thể loại, Nhóm tuổi, Tình trạng sách.**

---

## 🚀 3. Hướng Dẫn Khởi Động Website

### Cách 1: Chạy file nhanh (Khuyên dùng)
- Nhấp đúp chuột vào file `run.bat`.
- Trình duyệt sẽ tự động mở trang web tại `http://127.0.0.1:8088`.

### Cách 2: Khởi động qua dòng lệnh PowerShell / Terminal
```powershell
python manage.py runserver 0.0.0.0:8088
```

---

## 🛠️ 4. Công Nghệ Sử Dụng
- **Backend:** Python 3.12/3.14, Django 6.1.1, SQLite3 (không cần cài đặt database riêng, dữ liệu lưu ngay trong file `db.sqlite3`).
- **Frontend:** HTML5 Semantic, Tailwind CSS v3, Lucide Icons, Google Fonts (Quicksand & Nunito).
- **Phương thức thanh toán:** COD (Thanh toán tiền mặt khi nhận hàng, đồng kiểm tra sách).
- **Responsive:** Tối ưu mượt mà 100% trên điện thoại di động (có thanh menu điều hướng bottom bar cho mobile) và máy tính bảng, desktop.
