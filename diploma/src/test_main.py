from PIL import Image
import tensorflow as tf
import numpy as np


# Step 1: Load the image
image_path = './img_3.jpg'  # Replace with the path to your image file
original_image = Image.open(image_path)
resized_image = original_image.resize((224, 224))
if resized_image.mode != 'RGB':
    resized_image = resized_image.convert('RGB')

# Step 3: Load the model
model = tf.keras.models.load_model('./working/aug.keras')  # Replace with the path to your model file

# Step 4: Model Inference
input_data = tf.expand_dims(tf.image.convert_image_dtype(resized_image, tf.float32), 0)
predictions = model.predict(input_data)

# Do something with the predictions

first_output = predictions[0][0]

col = {
    'c0': 'safe driving',
    'c1': 'texting - right',
    'c2': 'talking on the phone - right',
    'c3': 'texting - left',
    'c4': 'talking on the phone - left',
    'c5': 'operating the radio',
    'c6': 'drinking',
    'c7': 'reaching behind',
    'c8': 'hair and makeup',
    'c9': 'talking to passenger'
}

prediction_array = np.array(first_output)

# Найдите индекс наибольшего элемента в массиве предсказаний
predicted_class_index = np.argmax(prediction_array)

# Используйте словарь col, чтобы получить соответствующий класс
predicted_class = col[f'c{predicted_class_index}']

print(predicted_class)
