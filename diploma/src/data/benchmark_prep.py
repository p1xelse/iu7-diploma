import os
import random
from PIL import Image

def prep_size(size):
    # Путь к исходной папке с изображениями по классам
    source_folder = "./train/"

    # Путь к новой папке для сохранения измененных изображений
    destination_folder = f"./bench/{size}_{size}"

    # Размер, до которого нужно уменьшить изображения
    target_size = (size, size)

    # Функция для ресайза изображений и сохранения их в новую папку
    def resize_images_and_save(class_folder, destination_class_folder):
        # Получаем список изображений в папке класса
        images = os.listdir(class_folder)
        # Выбираем случайные 20 изображений, если в папке есть больше
        selected_images = random.sample(images, min(20, len(images)))
        
        # Создаем папку для класса в новой папке, если ее еще нет
        if not os.path.exists(destination_class_folder):
            os.makedirs(destination_class_folder)

        # Ресайз и сохранение каждого изображения
        for image_name in selected_images:
            image_path = os.path.join(class_folder, image_name)
            with Image.open(image_path) as img:
                resized_img = img.resize(target_size)
                destination_path = os.path.join(destination_class_folder, image_name)
                resized_img.save(destination_path)

    # Перебор каждой папки класса в исходной папке
    for class_name in os.listdir(source_folder):
        class_folder = os.path.join(source_folder, class_name)
        destination_class_folder = os.path.join(destination_folder, class_name)
        resize_images_and_save(class_folder, destination_class_folder)

for i in range(20, 221, 20):
    prep_size(i)