import pickle

import matplotlib.pyplot as plt
import numpy as np


def main():
    with open('../train/history.hist', 'rb') as f:
        data = pickle.load(f)

    plt.rcParams['font.family'] = 'Times New Roman'

    plt.figure(0)
    plt.plot(data['output_accuracy'], color='green')
    plt.title(f"Точность модели на обучающих данных (максимальное значение: {max(data['output_accuracy']):.3f})")
    plt.ylabel('Точность (у.e.)')
    plt.xlabel('Эпоха')
    plt.savefig('train_accuracy.pdf', format='pdf')

    plt.figure(1)
    plt.plot(data['val_output_accuracy'], color='green')
    plt.title(f"Точность модели на валидационных данных (максимальное значение: {max(data['val_output_accuracy']):.3f})")
    plt.ylabel('Точность (у.e.)')
    plt.xlabel('Эпоха')
    plt.savefig('val_accuracy.pdf', format='pdf')

    # x = ['100%', '75%', '50%', '25%']
    # y1 = [17.5, 13.18, 11.48, 10.46]
    # y2 = [14.4, 12.68, 11.03, 10.37]

    # plt.figure(2)
    # plt.bar(x, y1, color='red')
    # plt.bar(x, y2, color='green')
    # plt.title('Зависимость времени работы приложения от размера снимка')
    # plt.xlabel('Размер снимка, % от исходного')
    # plt.ylabel('Время работы приложения, сек.')
    # plt.legend(['С классификацией', 'Без классификации'])
    # plt.savefig('run.svg', format='svg')


if __name__ == '__main__':
    main()
