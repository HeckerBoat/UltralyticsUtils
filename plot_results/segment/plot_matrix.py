# -*- coding: utf-8 -*-


# confusion_matrix
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

if __name__ == '__main__':
    # 修改此处
    classes = ['Galinsoga', 'Alternanthera', 'Cerastium', 'Oxalis', 'Cardamine', 'Amaranthus', 'Hemistepta', 'Eleusine']
    # classes = ['Galinsoga', 'Alternanthera', 'Cerastium']
    precentage_show = False
    # precentage_show = True

    # 优化前
    # confusion_matrix = np.array([
    #     [2496, 12, 32, 15, 43, 86, 45, 21],
    #     [56, 3276, 32, 21, 126, 23, 43, 23],
    #     [34, 215, 2567, 34, 23, 43, 23, 12],
    #     [32, 12, 32, 3425, 23, 12, 32, 43],
    #     [95, 17, 52, 43, 2546, 12, 43, 12],
    #     [123, 28, 45, 34, 12, 3654, 43, 122],
    #     [21, 72, 32, 142, 43, 132, 5436, 21],
    #     [12, 43, 12, 52, 32, 12, 32, 3465]
    # ], dtype=np.int32)  # 输入特征矩阵

    # 优化后
    confusion_matrix = np.array([
        [2496, 12, 32, 15, 43, 86, 45, 21],
        [26, 3276, 32, 21, 126, 23, 43, 23],
        [34, 115, 2567, 34, 23, 43, 23, 12],
        [32, 12, 32, 3425, 23, 12, 32, 43],
        [95, 17, 32, 43, 2546, 12, 43, 12],
        [57, 28, 45, 34, 12, 3654, 43, 122],
        [21, 72, 32, 62, 43, 132, 5436, 21],
        [12, 43, 12, 52, 32, 12, 32, 3465]
    ], dtype=np.int32)  # 输入特征矩阵
    proportion = []
    for i in confusion_matrix:
        for j in i:
            temp = j / (np.sum(i))
            proportion.append(temp)
    # print(np.sum(confusion_matrix[0]))
    # print(proportion)
    pshow = []
    for i in proportion:
        pt = "%.2f%%" % (i * 100)
        pshow.append(pt)
    proportion = np.array(proportion).reshape(len(classes), len(classes))  # reshape(列的长度，行的长度)
    pshow = np.array(pshow).reshape(len(classes), len(classes))
    # print(pshow)
    config = {
        "font.family": 'Times New Roman',  # 设置字体类型
    }
    rcParams.update(config)
    plt.imshow(proportion, interpolation='nearest', cmap=plt.cm.Blues)  # 按照像素显示出矩阵
    # (改变颜色：'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds','YlOrBr', 'YlOrRd',
    # 'OrRd', 'PuRd', 'RdPu', 'BuPu','GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn')
    plt.title('Confusion Matrix')
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, fontsize=12, rotation=90)
    plt.yticks(tick_marks, classes, fontsize=12)

    thresh = confusion_matrix.max() / 2.
    # ij配对，遍历矩阵迭代器
    iters = np.reshape([[i, j] for i in range(len(classes)) for j in range(len(classes))], (confusion_matrix.size, 2))

    for i, j in iters:
        if i == j:
            plt.text(j, i - 0.12, format(confusion_matrix[i, j]), va='center', ha='center', fontsize=12, color='white',
                     weight=5)  # 显示对应的数字
            if precentage_show:
                plt.text(j, i + 0.12, pshow[i, j], va='center', ha='center', fontsize=12, color='white')
        else:
            plt.text(j, i - 0.12, format(confusion_matrix[i, j]), va='center', ha='center', fontsize=12)  # 显示对应的数字
            if precentage_show:
                plt.text(j, i + 0.12, pshow[i, j], va='center', ha='center', fontsize=12)

    plt.ylabel('Predicted', fontsize=16)
    plt.xlabel('True', fontsize=16)
    plt.tight_layout()
    plt.savefig('results/Confusion Matrix.png')
    plt.show()
