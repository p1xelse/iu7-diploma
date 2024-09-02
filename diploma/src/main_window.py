from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QDoubleSpinBox, QLineEdit, QRadioButton)
import sys
import app.main
import images_window

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = uic.loadUi("./ui/untitled.ui", self)
        
        # Определим виджеты.
        self.photo_button = self.findChild(QPushButton, 'choice_photo')
        self.video_button = self.findChild(QPushButton, 'choice_video')
        self.mode_photo_radioButton = self.findChild(QRadioButton, 'mode_photo_radioButton')
        self.mode_video_radioButton = self.findChild(QRadioButton, 'mode_video_radioButton')
        self.calc_button = self.findChild(QPushButton, 'calc')
        self.files_label = self.findChild(QLabel, 'choiced_files_label')
        self.assessment = self.findChild(QLineEdit, 'assessment_line')
        self.show_images_button = self.findChild(QPushButton, 'show_images_button')
        
        # Веса
        self.texting_right_spin = self.findChild(QDoubleSpinBox, 'texting_right_spin')
        self.talking_right_spin = self.findChild(QDoubleSpinBox, 'talking_right_spin')
        self.texting_left_spin = self.findChild(QDoubleSpinBox, 'texting_left_spin')
        self.talking_left_spin = self.findChild(QDoubleSpinBox, 'talking_left_spin')
        self.operating_radio_spin = self.findChild(QDoubleSpinBox, 'operation_radio_spin')
        self.drinking_spin = self.findChild(QDoubleSpinBox, 'drink_spin')
        self.reaching_begind_spin = self.findChild(QDoubleSpinBox, 'behind_spin')
        self.hair_and_makeup_spin = self.findChild(QDoubleSpinBox, 'makeup_spin')
        self.talking_to_passenger = self.findChild(QDoubleSpinBox, 'talking_passanger_spin')
    
        
        # Обработчики
        self.photo_button.clicked.connect(self.photo_button_clicked)
        self.video_button.clicked.connect(self.video_button_clicked)
        self.mode_photo_radioButton.toggled.connect(
            self.on_radio_toggled
            )
        self.mode_video_radioButton.toggled.connect(
            self.on_radio_toggled
            )
        self.on_radio_toggled()
        self.calc_button.clicked.connect(self.calc_button_clicked)
        self.show_images_button.clicked.connect(
            self.show_images_button_clicked
            )
        
        # Контекст.
        self.mode = None
        self.file_path = ''
        self.classes_images = []
        
    def photo_button_clicked(self):
        folder_dialog = QFileDialog()
        folder_path = folder_dialog.getExistingDirectory(self, 'Выбрать папку с фото')

        if folder_path:
            self.files_label.setText("Выбрана папка с фото: " + folder_path)
            self.mode = app.main.DriverMode.PHOTO
            self.file_path = folder_path

    def video_button_clicked(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Выбрать видео', '', 'Video files (*.mp4 *.avi)')

        if file_path:
            self.files_label.setText("Выбрано видео: " + file_path)
            self.mode = app.main.DriverMode.VIDEO
            self.file_path = file_path

    def calc_button_clicked(self):
        classes_weights = self.__get_classes_weights()
        print(f'calc: file:{self.file_path}, weights:{classes_weights}')
        cfg = app.main.DriverSafetyGetterConfig(classes_weights, self.mode, self.file_path)
        getter = app.main.DriverSafetyAssessmentGetter(cfg)
        assessment = getter.get_driver_safety_assessment()
        print(f'assesment: {assessment}')
        self.assessment.setText(f"{assessment:.2f}")
        self.classes_images = getter.get_classes_images()

    def on_radio_toggled(self):
        if self.mode_photo_radioButton.isChecked():
            self.photo_button.setVisible(True)
            self.video_button.setVisible(False)
        elif self.mode_video_radioButton.isChecked():
            self.photo_button.setVisible(False)
            self.video_button.setVisible(True)
        
    def __get_classes_weights(self):
        classes_weights= {
            'texting - right': self.texting_right_spin.value(),
            'talking on the phone - right': self.talking_right_spin.value(),
            'texting - left': self.texting_left_spin.value(),
            'talking on the phone - left': self.talking_left_spin.value(),
            'operating the radio': self.operating_radio_spin.value(),
            'drinking': self.drinking_spin.value(),
            'reaching behind': self.reaching_begind_spin.value(),
            'hair and makeup': self.hair_and_makeup_spin.value(),
            'talking to passenger': self.talking_to_passenger.value(),
        }
        
        return classes_weights
    
    def show_images_button_clicked(self):
        self.img_window = images_window.GalleryWindow(self.classes_images)
        self.img_window.show()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == '__main__':
    sys.exit(main())