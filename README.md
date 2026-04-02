# 🛒 Sales Management System - Django

Hệ thống quản lý bán hàng đa nền tảng được xây dựng bằng **Django**, hỗ trợ quản lý sản phẩm, đơn hàng, khách hàng, kho hàng và báo cáo doanh thu.

## 📌 Giới thiệu
Đây là dự án web quản lý bán hàng được phát triển nhằm hỗ trợ doanh nghiệp hoặc cửa hàng trong việc:
- Quản lý sản phẩm
- Theo dõi đơn hàng
- Quản lý khách hàng
- Kiểm soát tồn kho
- Thống kê doanh thu
- Quản trị hệ thống thông qua trang Admin

Dự án được thiết kế theo mô hình dễ mở rộng, có thể phát triển thêm phiên bản Mobile trong tương lai.

---

## 🚀 Tính năng chính

### 🛍️ Quản lý sản phẩm
- Thêm / sửa / xóa sản phẩm
- Quản lý mã sản phẩm
- Quản lý giá bán
- Quản lý số lượng tồn kho
- Upload hình ảnh sản phẩm
- Phân loại theo danh mục
- Tìm kiếm sản phẩm bằng AJAX

### 📦 Quản lý đơn hàng
- Tạo đơn hàng mới
- Cập nhật trạng thái đơn hàng
- Theo dõi lịch sử giao dịch
- Quản lý thông tin giao hàng
- Hỗ trợ đặt hàng và đặt bàn

### 👤 Quản lý khách hàng
- Lưu thông tin khách hàng
- Tìm kiếm theo tên hoặc số điện thoại
- Theo dõi lịch sử mua hàng

### 🏬 Quản lý kho hàng
- Theo dõi số lượng tồn kho
- Tự động cập nhật khi phát sinh giao dịch
- Cảnh báo khi sản phẩm sắp hết hàng

### 📊 Báo cáo và thống kê
- Báo cáo doanh thu theo ngày / tuần / tháng
- Thống kê sản phẩm bán chạy
- Biểu đồ doanh số trực quan

### 🔐 Xác thực người dùng
- Đăng ký tài khoản
- Đăng nhập / đăng xuất
- Phân quyền Admin và User

### 💬 Tính năng bổ sung
- Bình luận / đánh giá sản phẩm
- Gợi ý tìm kiếm bằng AJAX

---

## 🛠️ Công nghệ sử dụng

- **Backend:** Python, Django
- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **AJAX:** Tìm kiếm động
- **Database:** MySQL
- **Version Control:** Git, GitHub

---

## 📂 Cấu trúc dự án

```bash
sales-management/
│── products/
│── orders/
│── customers/
│── inventory/
│── reports/
│── templates/
│── static/
│── manage.py
│── README.md
```

---

## ⚙️ Cài đặt và chạy dự án

### 1. Clone project
```bash
git clone https://github.com/Giakhanh-77/django-sales-management.git
cd django-sales-management
```

### 2. Chạy server
```bash
python manage.py runserver
```

---

## 🌟 Mục tiêu dự án
Dự án được xây dựng nhằm nâng cao kỹ năng:
- Django Framework
- Thiết kế cơ sở dữ liệu
- CRUD operations
- AJAX
- Quản lý nghiệp vụ bán hàng thực tế

---

## 👨‍💻 Tác giả
**Gia Khánh**  
Sinh viên Công nghệ Thông tin  
GitHub: https://github.com/Giakhanh-77
