import numpy as np
import app.main
import app.get_images
import matplotlib.pyplot as plt
import time
import tensorflow as tf


def count_time(): 
    cfg = app.main.DriverSafetyGetterConfig(app.main.default_classes_weights, app.main.DriverMode.PHOTO, "./demo_data/imgs")
    getter = app.main.DriverSafetyAssessmentGetter(cfg)
    x = np.arange(1, 520, 20)
    execution_times = []

    for x_i in x:
        print(f"x = {x_i}/520")
        start_time = time.time()
        getter.get_driver_safety_assessment(x_i)
        end_time = time.time()
        execution_time = end_time - start_time
        execution_times.append(execution_time)

    plt.bar(x, execution_times, width=15)
    plt.title('Зависимость времени выполнения от количества изображений')
    plt.xlabel('Количество изображений')
    plt.ylabel('Время выполнения (секунды)')
    plt.savefig('benchmark_results/count_time_bench.pdf', format='pdf')
    
    
def get_test_generator(base_dir_train, target_size=(224, 224)):    
    validation_ds = tf.keras.preprocessing.image_dataset_from_directory(
        base_dir_train,
        label_mode='int',
        seed=123,
        image_size=target_size,
        batch_size=100
    )
    
    normalization_layer = tf.keras.layers.experimental.preprocessing.Rescaling(1./255)
    normalized_validation_ds = validation_ds.map(lambda x, y: (normalization_layer(x), y))
    AUTOTUNE = tf.data.AUTOTUNE
    normalized_validation_ds = normalized_validation_ds.cache().prefetch(buffer_size=AUTOTUNE)

    return normalized_validation_ds.take(500)

def size_accurancy():
    model = tf.keras.models.load_model('./working/aug.keras')
    x_sizes = [20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 224]
    x_sizes_str = []
    y_acc = []
    for size in x_sizes:
        test_ds = get_test_generator(f"./data/bench/{size}_{size}", (224,224))
        res = model.evaluate(test_ds)
        y = res[4] * 100
        x_sizes_str.append(f'{size}x{size}')
        y_acc.append(y)
    fig, ax = plt.subplots(figsize=(10, 7), gridspec_kw={'bottom': 0.136})

    ax.hlines(y_acc[x_sizes_str.index('80x80')], xmin=-5, xmax=x_sizes_str.index('80x80'), color='r', linestyle='--')

    # Рисуем вертикальную линию до значения y_acc[index]
    ax.vlines(x_sizes_str.index('80x80'), ymin=0, ymax=y_acc[x_sizes_str.index('80x80')], color='r', linestyle='--')
    
    ax.text(0, y_acc[3], f'{y_acc[3]:.0f}', color='r', verticalalignment='bottom')
    
    ax.plot(x_sizes_str, y_acc, marker='o')
    plt.xticks(rotation=45)  # Поворот значений по оси x на 45 градусов для избежания перекрытия
    plt.title('Зависимость точности модели от исходного размера изображения')
    plt.xlabel('Размер изображений (пиксели)')
    plt.ylabel('Точность модели (%)')
    # plt.show()
    plt.savefig('benchmark_results/sizes_acc_bench.pdf', format='pdf')
    
# count_time()
size_accurancy()