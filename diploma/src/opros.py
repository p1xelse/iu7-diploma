import matplotlib.pyplot as plt
plt.rcParams['font.size'] = 15


sizes = [60, 26, 14]
labels = ['Цена', 'Безопаность', 'Время ожидания']
colors = ['white', 'white', 'white']

fig1, ax1 = plt.subplots()
wedges, _ = ax1.pie(sizes, labels=[f"{l} - {s}%" for l, s in zip(labels, sizes)], startangle=90, colors=colors, wedgeprops=dict(width=0.7, edgecolor='black', linewidth=2))

hatch_styles = ['-', '+', 'x']
    
for i in range(len(sizes)):
    ax1.patches[i].set_hatch(hatch_styles[i])

ax1.axis('equal')
plt.savefig('output1.png', bbox_inches='tight')  # Сохраняем изображение с учетом размеров объектов