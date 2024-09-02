import cv2
import os
from PIL import Image
import matplotlib.pyplot as plt

def get_images_from_video(path_to_video, interval_sec):
    video_capture = cv2.VideoCapture(path_to_video)
    frame_rate = video_capture.get(cv2.CAP_PROP_FPS)
    images = []
    current_frame = 0
    while True:
        success, frame = video_capture.read()
        if not success:
            break
        if current_frame % int(frame_rate * interval_sec) == 0:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
            pil_image = Image.fromarray(rgb_frame)
            images.append(pil_image)
        current_frame += 1
    video_capture.release()
    return images

def get_images_from_folder(path_to_images):
    images = []
    for filename in os.listdir(path_to_images):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(path_to_images, filename)
            img = Image.open(image_path)
            images.append(img)
    return images
