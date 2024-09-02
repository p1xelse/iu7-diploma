import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QScrollArea,
    QHBoxLayout,
    QMainWindow,
    QSpacerItem,
    QSizePolicy,
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from PIL import Image
from io import BytesIO

classes_en_ru_mapping = {
    "safe driving": "Cосредоточен",
    "texting - right": "Печатает (правая рука)",
    "talking on the phone - right": "Разговаривает по телефону (правая рука)",
    "texting - left": "Печатает (левая рука)",
    "talking on the phone - left": "Разговаривает по телефону (левая рука)",
    "operating the radio": "Управляет радио",
    "drinking": "Пьет",
    "reaching behind": "Тянется назад",
    "hair and makeup": "Делает прическу/макияж",
    "talking to passenger": "Разговаривает с пассажиром",
}


class GalleryWindow(QWidget):
    def __init__(self, images):
        super().__init__()
        self.images = images  # Словарь с изображениями
        self.total_elements = sum(len(images) for images in self.images.values())
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: white;")
        layout = QVBoxLayout()

        scroll = QScrollArea()  # Создание области прокрутки
        widget = QWidget()  # Главный виджет, содержащий все остальные виджеты
        scroll.setWidget(
            widget
        )  # Установка виджета в качестве содержимого области прокрутки
        scroll.setWidgetResizable(True)  # Разрешение изменения размера виджета

        vbox = QVBoxLayout()  # Вертикальное расположение для всех элементов

        for class_name, imgs in self.images.items():  # Перебор всех классов изображений
            label = QLabel(
                f"{classes_en_ru_mapping[class_name]}"+
                f"[{len(imgs)}/{self.total_elements}]"
            )
            label.setAlignment(Qt.AlignCenter)
            vbox.addWidget(label)

            imgs_in_row = 4
            row_counter = 0
            hbox = QHBoxLayout()
            hbox.setSpacing(0)
            hbox.setContentsMargins(0, 0, 0, 0)

            for img in imgs:
                if row_counter >= imgs_in_row:
                    vbox.addLayout(hbox)
                    hbox = QHBoxLayout()
                    row_counter = 0

                pixmap = QPixmap.fromImage(
                    self.convert_pil_image_to_qimage(img)
                )  # Создание изображения
                img_label = QLabel(self)  # Создание метки для изображения
                img_label.setPixmap(pixmap)  # Установка изображения в метку
                hbox.addWidget(
                    img_label
                )  # Добавление метки в горизонтальное расположение
                row_counter += 1  # Увеличение счетчика изображений в строке

            if row_counter > 0 and row_counter < 4:
                spacer = QSpacerItem(
                    100, 100, QSizePolicy.Expanding, QSizePolicy.Minimum
                )
                hbox.addSpacerItem(spacer)
            if (
                row_counter > 0
            ):  # Проверка, есть ли необработанные изображения после выхода из цикла
                vbox.addLayout(
                    hbox
                )  # Добавление последнего горизонтального расположения в вертикальное

        widget.setLayout(
            vbox
        )  # Установка вертикального расположения в качестве основного для виджета
        layout.addWidget(
            scroll
        )  # Добавление области прокрутки в основное вертикальное расположение
        self.setLayout(
            layout
        )  # Установка основного вертикального расположения для self
        self.setWindowTitle("Классы изображений")  # Задание заголовка окна
        self.resize(600, 400)  # Установка начального размера окна

    def convert_pil_image_to_qimage(self, pil_image):
        pil_image = pil_image.resize((100, 100))
        image_data = BytesIO()
        pil_image.save(image_data, format="PNG")
        qimage = QImage()
        qimage.loadFromData(image_data.getvalue())
        return qimage
