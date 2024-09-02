import tensorflow as tf
import keras
from keras.optimizers import SGD
from keras.callbacks import LearningRateScheduler
from keras.models import load_model
import math
from model import GoogleNet
import argparse

epochs = 200
batch_size = 100
    
def get_generators(base_dir_train, target_size=(224, 224)):
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        base_dir_train,
        validation_split=0.2,
        subset="training",
        seed=123,
        label_mode='int',
        image_size=target_size,
        batch_size=batch_size
    )
    
    validation_ds = tf.keras.preprocessing.image_dataset_from_directory(
        base_dir_train,
        validation_split=0.2,
        subset="validation",
        label_mode='int',
        seed=123,
        image_size=target_size,
        batch_size=batch_size
    )
    
    
    class_names = train_ds.class_names
    print(class_names)
    print("before aug: ", train_ds.cardinality().numpy() * batch_size)
    
    data_augmentation = keras.Sequential(
        [
            tf.keras.layers.experimental
                .preprocessing.RandomFlip("horizontal"),
            tf.keras.layers.experimental
                .preprocessing.RandomRotation(0.1),
            tf.keras.layers.experimental
                .preprocessing.RandomZoom(0.1),
        ]
    )
    
    train_ds = train_ds.map(lambda x, y: (data_augmentation(x), y), num_parallel_calls=tf.data.AUTOTUNE)
    
    normalization_layer = tf.keras.layers.experimental.preprocessing.Rescaling(1./255)
    normalized_train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
    normalized_validation_ds = validation_ds.map(lambda x, y: (normalization_layer(x), y))
    
    AUTOTUNE = tf.data.AUTOTUNE

    normalized_train_ds = normalized_train_ds.cache().prefetch(buffer_size=AUTOTUNE)
    normalized_validation_ds = normalized_validation_ds.cache().prefetch(buffer_size=AUTOTUNE)

    return normalized_train_ds.take(3000), normalized_validation_ds.take(500)

def train(dataset_dir = "./data/train", is_add_train = False):
    num_classes = 10
    img_rows,img_cols = 224, 224

    train_ds, test_ds = get_generators(dataset_dir, (img_rows,img_cols))

    initial_lrate = 0.01

    def decay(epoch, steps=100):
        initial_lrate = 0.01
        drop = 0.96
        epochs_drop = 8
        lrate = initial_lrate * math.pow(drop, math.floor((1+epoch)/epochs_drop))
        return lrate


    sgd = SGD(learning_rate=initial_lrate, momentum=0.9, nesterov=False)

    lr_sc = LearningRateScheduler(decay, verbose=1)

    if not is_add_train:
        model = GoogleNet()
        model.compile(loss=keras.losses.sparse_categorical_crossentropy, loss_weights=[1, 0.3, 0.3], optimizer=sgd, metrics=['accuracy'])
    else:
        model = load_model('model.keras')

    # Moddel Training
    train_ds = train_ds.map(lambda x, y: (x, (y, y, y)))
    test_ds = test_ds.map(lambda x, y: (x, (y, y, y)))


    history = model.fit(
        train_ds,
        validation_data=test_ds,
        epochs=epochs,
        batch_size=batch_size,
        callbacks=[lr_sc]
    )

    model.save('model.keras')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    teeth = True

    parser.add_argument('-d', '--dataset', default='./data/train', help='Путь к набору данных')
    parser.add_argument('-m', '--mode', default='train', help='Режим работы: train/add_train (обучение/дообучение)')

    args = parser.parse_args()

    if args.mode == 'train':
        print('Running training:')
        train(args.dataset, is_add_train=False)
    elif args.mode == 'add_train':
        print('Running additional training:')
        train(args.dataset, is_add_train=True)