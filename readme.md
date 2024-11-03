Đây là source code server nhận diện khuôn mặt gồm có các chức năng: 
- Train
- Thêm/Xóa ảnh
- Kiểm tra tên 
- Test nhận diện bằng camera thiết bị **(Đang phát triển, hiện tại chưa có)

Để sử dụng được cần có các thư viện, với cú pháp như sau:
- pip install face_recognition pickle json


Người dùng khi muốn sử dụng cần chỉnh sửa các file trong folder Photos-001 chứa ảnh và các name, name_path trong known_faces.json
Có thể sử dụng các cách sau:
1. Thay đổi trực tiếp trên file source
2. Chạy server rồi chỉnh sửa theo ý muốn