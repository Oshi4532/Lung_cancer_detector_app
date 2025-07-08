import os
import random
import shutil
#pls ignore this file 




# 📁 ต้นทาง (หลังแตก zip แล้ว)
base_path = "C:/Users/Garado/Downloads/lung-cancer-dataset.v6i.yolov8"
images_dir = os.path.join(base_path, "train/images")
labels_dir = os.path.join(base_path, "train/labels")

# 📁 ปลายทาง (validation)
val_images_dir = os.path.join(base_path, "valid/images")
val_labels_dir = os.path.join(base_path, "valid/labels")

# ✅ สร้างโฟลเดอร์ปลายทาง
os.makedirs(val_images_dir, exist_ok=True)
os.makedirs(val_labels_dir, exist_ok=True)

# 🔢 สัดส่วน validation (10%)
val_ratio = 0.1

# 📋 รายชื่อไฟล์ภาพ
image_files = [f for f in os.listdir(images_dir) if f.endswith(('.jpg', '.png'))]
random.shuffle(image_files)

val_count = int(len(image_files) * val_ratio)
val_images = image_files[:val_count]

for img_name in val_images:
    # 🔁 ชื่อไฟล์ label ต้องตรงกับภาพ (แต่ .txt)
    label_name = os.path.splitext(img_name)[0] + '.txt'

    # 🔃 ย้ายภาพ
    shutil.move(os.path.join(images_dir, img_name), os.path.join(val_images_dir, img_name))
    
    # 🔃 ย้าย label (ถ้ามี)
    src_label_path = os.path.join(labels_dir, label_name)
    dst_label_path = os.path.join(val_labels_dir, label_name)
    
    if os.path.exists(src_label_path):
        shutil.move(src_label_path, dst_label_path)

print(f"✅ Moved {len(val_images)} images to validation set.")
