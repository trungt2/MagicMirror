import face_recognition
import os
import json
import pickle
import hashlib
import numpy as np

#Xử lý thêm tên vào file
def save_people_to_json(people, json_path):
    with open(json_path, 'w') as file:
        json.dump({"people": people}, file, indent=4)

#  Phần xử lý huấn luyện mô hình từ file đã được set up
def load_people_from_json(json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)
    return data['people']

def load_names_from_json(json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)
    # Trích xuất danh sách tên
    names = [person['name'] for person in data['people']]
    return names

def train_faces(people):
    known_face_encodings = []
    known_face_names = []

    for person in people:
        name = person['name']
        image_path = person['image_path']
        
        # Tải ảnh từ thư mục
        for img_file in os.listdir(image_path):
            if img_file.endswith('.jpg') or img_file.endswith('.png'):
                full_image_path = os.path.join(image_path, img_file)
                image = face_recognition.load_image_file(full_image_path)
                encoding = face_recognition.face_encodings(image)
                
                if encoding:
                    known_face_encodings.append(encoding[0])
                    known_face_names.append(name)

    return known_face_encodings, known_face_names

def save_encodings_to_file(encodings, names, output_file):
    with open(output_file, 'wb') as file:
        pickle.dump((encodings, names), file)

def train_model(json_path='known_faces.json', output_file='face_encodings.pkl'):
    people = load_people_from_json(json_path)
    known_face_encodings, known_face_names = train_faces(people)
    save_encodings_to_file(known_face_encodings, known_face_names, output_file)
    print('Success')


# Phần xử lý nhận diện mặt
input_file = 'face_encodings.pkl'

def load_encodings_from_file(input_file):
    with open(input_file, 'rb') as file:
        return pickle.load(file)

def recognize_face(test_image_path):
    known_face_encodings, known_face_names = load_encodings_from_file('face_encodings.pkl')  #Load file train 

    test_image = face_recognition.load_image_file(test_image_path) # Load ảnh cần so sánh
    test_face_encodings = face_recognition.face_encodings(test_image) # Huấn luyện mặt 

    if not test_face_encodings:
        return "No_face"
    
    for test_encoding in test_face_encodings:
        distances = face_recognition.face_distance(known_face_encodings, test_encoding)
        
        best_match_index = np.argmin(distances)
        name = "Unknown"

        # Kiểm tra độ chính xác
        if distances[best_match_index] < 0.5:
            name = known_face_names[best_match_index]

    return name

def calculate_image_hash(image_path):
    hasher = hashlib.md5()
    with open(image_path, 'rb') as img_file:
        buf = img_file.read()
        hasher.update(buf)
    return hasher.hexdigest()

def is_duplicate_image(folder_path, image_path):
    #Kiểm tra ảnh đã có chưa
    image_hash = calculate_image_hash(image_path)
    for file_name in os.listdir(folder_path):
        existing_image_path = os.path.join(folder_path, file_name)
        if os.path.isfile(existing_image_path):
            if calculate_image_hash(existing_image_path) == image_hash:
                return True
    return False