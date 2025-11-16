# Image Caption Generator - Ứng dụng sinh mô tả ảnh tự động

## 📖 Giới thiệu

**Image Caption Generator** là một ứng dụng web thông minh sử dụng trí tuệ nhân tạo để tự động tạo mô tả văn bản cho hình ảnh. Ứng dụng kết hợp sức mạnh của mạng nơ-ron tích chập (CNN) để hiểu nội dung hình ảnh và mạng LSTM để sinh ra mô tả ngôn ngữ tự nhiên.

## 🎯 Tính năng nổi bật

### 🤖 Sinh mô tả tự động thông minh
- **AI Power**: Sử dụng mô hình CNN-LSTM đã được huấn luyện chuyên sâu
- **Độ chính xác cao**: Đạt BLEU-1 score 0.65 trên tập test
- **Xử lý nhanh**: Thời gian sinh mô tả trung bình chỉ 3.2 giây
- **Đa dạng ảnh**: Hỗ trợ nhiều loại ảnh và ngữ cảnh khác nhau

### 🖼️ Upload ảnh thông minh
- **Kéo-thả trực quan**: Giao diện kéo-thả file thân thiện
- **Preview tức thì**: Xem trước ảnh ngay lập tức
- **Validation thông minh**: Tự động kiểm tra định dạng và kích thước
- **Hỗ trợ đa dạng**: JPG, PNG, JPEG (tối đa 5MB)

### ✏️ Hệ thống phản hồi thông minh
- **Approve Caption**: Dễ dàng phê duyệt mô tả chính xác
- **Correct Caption**: Chỉnh sửa mô tả chưa hoàn hảo
- **AI Learning**: Hệ thống học hỏi từ phản hồi người dùng
- **Data Collection**: Thu thập dữ liệu chất lượng cao cho training

### 📊 Dashboard thống kê
- **Real-time Analytics**: Theo dõi hiệu suất hệ thống thời gian thực
- **Visual Reports**: Báo cáo trực quan với biểu đồ
- **Performance Metrics**: Đánh giá chất lượng mô tả
- **User Insights**: Phân tích hành vi người dùng

## 🛠️ Công nghệ sử dụng

### Backend Framework
- **Django**: Web framework mạnh mẽ và bảo mật
- **Python 3.9**: Ngôn ngữ lập trình chính
- **TensorFlow/Keras**: Framework AI/Deep Learning
- **SQLitet3**: Database chính thức
- **Django REST Framework**: Xây dựng API

### Frontend Technology
- **HTML5**: Cấu trúc trang web hiện đại
- **CSS3**: Styling với animations mượt mà
- **JavaScript**: Xử lý tương tác người dùng
- **Responsive Design**: Tương thích mọi thiết bị

### AI/ML Architecture
- **Feature Extraction**: 16 (pre-trained trên ImageNet)
- **Sequence Generation**: LSTM với attention mechanism
- **Model Architecture**: Encoder-Decoder với CNN-LSTM
- **Training Dataset**: Flickr8k (8,091 ảnh với 40,455 mô tả)

## 📦 Cài đặt và Triển khai

### Yêu cầu hệ thống
- Python 3.8 hoặc cao hơn
- TensorFlow 2.8+
- Django 4.0+
- RAM: 4GB (tối thiểu), 8GB (khuyến nghị)
- Storage: 2GB dung lượng trống

### Bước 1: Clone repository
```bash
git clone https://github.com/your-username/image-caption-generator.git
cd image-caption-generator
```

### Bước 2: Thiết lập và kích hoạt môi trường ảo
```bash
# Tạo môi trường ảo
python -m venv name_venv

# Kích hoạt
# Window
venv\Scripts\activate
# Trên Linux/Mac:
source venv/bin/activate
```

### Bước 3: Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### Bước 4: Cấu hình DB
```bash
# Tạo migrations
python manage.py makemigrations

# Áp dụng migrations
python manage.py migrate

# Tạo superuser (tùy chọn)
python manage.py createsuperuser
```

### Bước 5: Chạy ứng dụng
```bash
python manage.py runserver
```

Truy cập ứng dụng: http://localhost:8000