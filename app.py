from flask import Flask, render_template, request, jsonify
from model import train_model, load_names_from_json, recognize_face, load_people_from_json, save_people_to_json, is_duplicate_image
import os
import shutil

json_path = 'known_faces.json'
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/train', methods=['POST'])
def train():
    train_model()
    return "Training Complete"

@app.route('/train_complete')
def train_complete():
    return render_template('train_complete.html')

@app.route('/check_name', methods=['GET'])
def check_name():
    names = load_names_from_json(json_path)
    return jsonify(names=names)  # Trả về danh sách tên dưới dạng JSON

@app.route('/upload', methods=['POST'])
def upload():
    name = request.form.get('name')
    image = request.files.get('image')

    if image:
        image.save(os.path.join(os.getcwd(), 'temp.jpg')) #Lưu ảnh tạm thời

        test_image_path = 'temp.jpg'
        names = recognize_face(test_image_path)
        
        #Không có khuôn mặt 
        if names == "No_face":
            return render_template('result.html', result="Không nhận diện được khuôn mặt trong ảnh")
        
        #Có mặt nhưng chưa có tên
        if names == "Unknown":
            people = load_people_from_json(json_path)

            new_folder_path = os.path.join('Photos-001', name)
            os.makedirs(new_folder_path, exist_ok=True)

            new_image_path = os.path.join(new_folder_path, f"{name}.jpg")
            shutil.copy(test_image_path, new_image_path)
            
            # Form: "image_path": "Photos-001/Messi"
            people.append({"name": name, "image_path": f"Photos-001/{name}"})

            save_people_to_json(people, json_path)

            return render_template('result.html', result=f"Đã nhận diện thành công, tạo mới với tên:{name}")
        
        #Tên, mặt trùng nhau
        if names == name:
            #Set vị trí lưu ảnh
            existing_folder_path = os.path.join('Photos-001', name)
            os.makedirs(existing_folder_path, exist_ok=True)

            #Kiểm tra ảnh trùng lặp
            if is_duplicate_image(existing_folder_path, test_image_path):
                return render_template('result.html', result=f"Ảnh của {name} đã có trên hệ thống")
            
            #Thêm ảnh vào với tên và số đếm nhằm tránh trùng lặp
            count_image = len(os.listdir(existing_folder_path)) + 1
            new_image_path = os.path.join(existing_folder_path, f"{name}_{count_image}.jpg")
            shutil.copy(test_image_path, new_image_path)

            return render_template('result.html', result=f"Đã có tên và mặt trùng khớp, thêm ảnh vào {name}")
        
        #Mặt trùng nhưng khác tên
        elif names != name:
            return render_template('change_name.html', current_name=names, new_name=name) 

        #Còn lại
        return render_template('result.html', result=f"Không thể xử lý")

@app.route('/change_name', methods=['POST'])
def change_name():
    current_name = request.form.get('current_name')
    new_name = request.form.get('new_name')
    action = request.form.get('action')

    people = load_people_from_json(json_path)
    current_folder_path = os.path.join('Photos-001', current_name)

    if action == 'keep':
        # Giữ nguyên tên hiện tại
        return render_template('result.html', result=f"Giữ tên hiện tại: {current_name}")
    
    elif action == 'change':
        # Cập nhật tên, path trong Json
        for person in people:
            if person['name'] == current_name:
                person['name'] = new_name
                person['image_path'] = f"Photos-001/{new_name}"
                break

        save_people_to_json(people, json_path)

        #Đổi tên thư mục theo tên mới
        new_folder_path = os.path.join('Photos-001', new_name)
        os.rename(current_folder_path, new_folder_path)

        #Đổi tên ảnh theo tên mới
        for filename in os.listdir(new_folder_path):
            if filename.startswith(current_name):
                new_file_path = os.path.join(new_folder_path, filename.replace(current_name, new_name, 1))
                old_file_path = os.path.join(new_folder_path, filename)
                os.rename(old_file_path, new_file_path)
        
        return render_template('result.html', result=f"Đã thay đổi tên từ {current_name} thành {new_name}. Vui lòng nhấn Train lại")

    return render_template('result.html', result="Không thể thực hiện thao tác")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1234)
