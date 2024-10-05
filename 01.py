import cv2
import os
import time

# Tạo đối tượng camera
cap = cv2.VideoCapture(0)

# Tải mô hình phát hiện khuôn mặt từ OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

face_id = input('\n Nhap ten ==>  ')
main_folder = "dataset"
new_folder_path = os.path.join(main_folder, face_id)

if not os.path.exists(new_folder_path):
    os.makedirs(new_folder_path)
    print(f"Thư mục '{new_folder_path}' đã được tạo thành công!")
else:
    print(f"Thư mục '{new_folder_path}' đã tồn tại.")

cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video width
cam.set(4, 480) # set video height
count = 0
start = time.time()

while True:
    # Đọc frame từ camera
    ret, frame = cap.read()

    if not ret:
        print("Không thể nhận diện camera!")
        break

    # Chuyển đổi ảnh sang ảnh xám
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Phát hiện khuôn mặt trong ảnh
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    # Vẽ hình chữ nhật quanh các khuôn mặt được phát hiện
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Hiển thị ảnh với khuôn mặt được phát hiện
    cv2.imshow('Video', frame)
    current_time = time.time()
    for (x, y, w, h) in faces:
        # Cắt vùng mặt từ ảnh gốc
        face_img = gray[y:y + h, x:x + w]
        if(current_time-start > 1):
            # Lưu ảnh mặt dưới dạng ảnh xám
            cv2.imwrite("dataset/" + str(face_id) + "/" + str(count) + ".jpg", face_img)
            start = current_time
            print(current_time-start)
            count+=1
    

    # Thoát khỏi chương trình khi nhấn phím 'q'1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()
