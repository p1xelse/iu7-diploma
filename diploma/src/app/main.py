from enum import Enum

from . import get_images
import tensorflow as tf
import numpy as np

import matplotlib.pyplot as plt

classes = {
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

default_classes_weights= {
    'texting - right': 1,
    'talking on the phone - right': 1,
    'texting - left': 1,
    'talking on the phone - left': 1,
    'operating the radio': 1,
    'drinking': 1,
    'reaching behind': 1,
    'hair and makeup': 1,
    'talking to passenger': 1,
}

class DriverMode(Enum):
    VIDEO = "video"
    PHOTO = "photo"
    
class DriverSafetyGetterConfig:
    def __init__(self, classes_weights, mode: DriverMode, path_to_files, interval_sec=1):
        self.classes_weights = classes_weights
        self.mode = mode
        self.path_to_files = path_to_files
        self.interval_sec = interval_sec if mode == DriverMode.VIDEO else None

class DriverSafetyAssessmentGetter:
    def __init__(self, cfg: DriverSafetyGetterConfig):
        self.cfg = cfg
        self.model = tf.keras.models.load_model('./working/aug.keras')
        
        self.images = []
        self.input_datas = []
        self.classes_count= {
            'safe driving': 0,
            'texting - right': 0,
            'talking on the phone - right': 0,
            'texting - left': 0,
            'talking on the phone - left': 0,
            'operating the radio': 0,
            'drinking': 0,
            'reaching behind': 0,
            'hair and makeup': 0,
            'talking to passenger': 0,
        }
        self.classes_images = {
            'safe driving': [],
            'texting - right': [],
            'talking on the phone - right': [],
            'texting - left': [],
            'talking on the phone - left': [],
            'operating the radio': [],
            'drinking': [],
            'reaching behind': [],
            'hair and makeup': [],
            'talking to passenger': [],
        }
        
    def get_driver_safety_assessment(self, limit=100): #TODO убрать лимит после исследовательской
        self.__set_images()
        self.__prepare_input_datas()
        self.input_datas = self.input_datas[:limit] # TODO: убрать
        
        for i, input_data in enumerate(self.input_datas):
            prediction = self.model.predict(input_data)
            predicted_class = self.__get_class_by_prediction(prediction)
            self.classes_images[predicted_class].append(self.images[i])
            self.classes_count[predicted_class] += 1
            
        # for image in classes_images['talking to passenger']:
        #     plt.imshow(image)
        #     plt.show()
        
        return self.__get_assessment_by_classes_count()
    
    def get_classes_images(self):
        return self.classes_images
    
    def __get_assessment_by_classes_count(self):
        print(self.classes_count)
        assesment = 100
        k = len(self.input_datas) / assesment
        for class_name, weight in self.cfg.classes_weights.items():
            assesment -= (self.classes_count[class_name] / k) * weight
        print(assesment)
        return assesment
    
    def __set_images(self):
        cfg = self.cfg
        if cfg.mode == DriverMode.VIDEO:
            self.images = get_images.get_images_from_video(
                path_to_video=cfg.path_to_files, interval_sec=cfg.interval_sec
                )
        elif cfg.mode == DriverMode.PHOTO:
            self.images = get_images.get_images_from_folder(
                path_to_images=cfg.path_to_files
                )

    def __prepare_input_datas(self):
        input_datas = []
        for i in self.images:
            prepared_image = i.resize((224, 224))
            if prepared_image.mode != 'RGB':
                prepared_image = prepared_image.convert('RGB')
            input_data = tf.expand_dims(tf.image.convert_image_dtype(prepared_image, tf.float32), 0)
            input_datas.append(input_data)
        self.input_datas = input_datas
        
    def __get_class_by_prediction(self, prediction):
        first_output = prediction[0][0]
        prediction_array = np.array(first_output)
        # Найдите индекс наибольшего элемента в массиве предсказаний
        predicted_class_index = np.argmax(prediction_array)
        predicted_class = classes[f'c{predicted_class_index}']
        return predicted_class


# cfg = DriverSafetyGetterConfig(classes_weights, DriverMode.PHOTO, './demo_data/imgs')
# getter = DriverSafetyAssessmentGetter(cfg)

# getter.get_driver_safety_assessment()