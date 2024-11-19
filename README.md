# 📚 ỨNG DỤNG QUẢN LÝ MƯỢN SÁCH THƯ VIỆN

Ứng dụng này được xây dựng để hỗ trợ quản lý các quy trình trong thư viện như: quản lý sách, độc giả, mượn sách, trả sách, và thống kê. Hệ thống giúp giảm thiểu sai sót và nâng cao hiệu quả quản lý dữ liệu.

## 🛠 TÍNH NĂNG

### 1. **Quản Lý Sách**
* Thêm, sửa, xóa và tìm kiếm sách
* Theo dõi trạng thái sách: còn sẵn, đã mượn, bảo trì, bị mất
* Quản lý thông tin ISBN, thể loại, giá thuê, nhà xuất bản, năm xuất bản

### 2. **Quản Lý Độc Giả**
* Lưu trữ thông tin độc giả: họ tên, địa chỉ, email, loại thẻ
* Xác minh trạng thái thẻ độc giả (còn hạn hoặc hết hạn)
* Kiểm tra số lượng sách đang mượn

### 3. **Mượn Sách**
* Cho phép mượn sách nếu độc giả đủ điều kiện
* Xác nhận trạng thái sách: chỉ cho mượn sách còn sẵn
* Tự động tính ngày trả (14 ngày sau khi mượn)

### 4. **Trả Sách**
* Tính phí phạt cho sách trả trễ (5.000 VND mỗi ngày quá hạn)
* Cập nhật trạng thái sách và lưu thông tin trả sách
* Hiển thị danh sách sách đang mượn của độc giả

### 5. **Thống Kê**
* Tổng hợp thông tin:
   * Tổng số sách, độc giả, sách đang mượn
   * Số lượt mượn sách và tiền phạt
* Vẽ biểu đồ thống kê theo thời gian và thể loại sách

## 🚀 HƯỚNG DẪN CÀI ĐẶT

### Yêu Cầu
1. **Python 3.x**: Cài đặt Python trên hệ thống của bạn
2. **PostgreSQL**: Cài đặt và cấu hình cơ sở dữ liệu PostgreSQL

### Các Bước Cài Đặt
1. Clone dự án:
```bash
git clone https://github.com/DuyTran04/N14_MuonSach
cd N14_MuonSach
```

2. Cài đặt các thư viện Python:
```bash
pip install -r requirements.txt
```

3. Cấu hình cơ sở dữ liệu:
   * Tạo cơ sở dữ liệu mới với tên `muonsach`
   * Chạy script SQL để thiết lập bảng và dữ liệu ban đầu:
```bash
psql -U postgres -d muonsach -f muonsach.sql
```

4. Cập nhật thông tin kết nối cơ sở dữ liệu trong `main.py`:
```python
conn = psycopg2.connect(
    database="muonsach",
    user="postgres",
    password="your-password",
    host="localhost",
    port="5432"
)
```

5. Chạy ứng dụng:
```bash
python main.py
```

## 📂 CẤU TRÚC DỰ ÁN
```
├── main.py         # Tệp chính khởi chạy ứng dụng
├── muonsach.py     # Chức năng mượn sách
├── trasach.py      # Chức năng trả sách
├── quanlysach.py   # Quản lý sách
├── quanlydocgia.py # Quản lý độc giả
├── thongke.py      # Thống kê
├── muonsach.sql    # Tệp SQL cấu hình cơ sở dữ liệu
├── README.md       # Tài liệu hướng dẫn
```

## ⚙️ CÁCH SỬ DỤNG
1. **Menu Chính**:
   * Điều hướng đến các chức năng: quản lý sách, mượn sách, trả sách, thống kê

2. **Mượn Sách**:
   * Nhập mã độc giả và ISBN để mượn sách
   * Kiểm tra điều kiện sách và độc giả trước khi cho mượn

3. **Trả Sách**:
   * Chọn sách từ danh sách đang mượn để trả
   * Tính phí phạt tự động nếu trả sách trễ

4. **Thống Kê**:
   * Xem báo cáo số liệu trực quan thông qua biểu đồ
