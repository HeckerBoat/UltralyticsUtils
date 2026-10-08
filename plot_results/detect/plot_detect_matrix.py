# -*- coding: utf-8 -*-


# confusion_matrix
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

if __name__ == '__main__':
    # 修改此处
    classes = ['Galinsoga parviflora', 'Alternanthera philoxeroides', 'Cerastium glomeratum', 'Cardamine hirsuta',
               'Amaranthus retroflexus', 'Pilea peperomioides', 'background']
    # classes = ['Galinsoga', 'Alternanthera', 'Cerastium']
    precentage_show = False
    # precentage_show = True

    # 优化前
    # confusion_matrix = np.array([
    #     [4512, 256, 126, 221, 123, 125, 12],
    #     [208, 4535, 252, 93, 246, 144, 15],
    #     [101, 271, 4879, 256, 153, 223, 16],
    #     [134, 205, 404, 4235, 74, 161, 8],
    #     [112, 83, 103, 189, 4610, 62, 14],
    #     [233, 182, 156, 352, 133, 4378, 6],
    #     [12, 3, 4, 5, 3 ,2, 0],
    # ], dtype=np.int32)  # 输入特征矩阵

    # 优化后
    confusion_matrix = np.array([
        [4932, 124, 63, 432, 78, 95, 5],
        [108, 4612, 152, 123, 216, 124, 9],
        [102, 251, 4979, 206, 143, 203, 2],
        [214, 155, 204, 4555, 54, 101, 5],
        [112, 34, 213, 145, 5546, 42, 9],
        [123, 142, 226, 234, 123, 6654, 4],
        [7, 1, 2, 5, 4, 2, 0],
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
    # iters = np.reshape([[i, j] for i in range(len(classes)) for j in range(len(classes))], (confusion_matrix.size, 2))
    iters = [(i, j) for i, j in np.ndindex((len(classes), len(classes)))]

    for i, j in iters:
        if i == j:
            plt.text(j, i - 0.12, format(confusion_matrix[i, j]), va='center', ha='center', fontsize=10, color='white',
                     weight=5)  # 显示对应的数字
            if precentage_show:
                plt.text(j, i + 0.12, pshow[i, j], va='center', ha='center', fontsize=10, color='white')
        else:
            plt.text(j, i - 0.12, format(confusion_matrix[i, j]), va='center', ha='center', fontsize=10)  # 显示对应的数字
            if precentage_show:
                plt.text(j, i + 0.12, pshow[i, j], va='center', ha='center', fontsize=10)

    plt.ylabel('True', fontsize=16)
    plt.xlabel('Predict', fontsize=16)
    plt.tight_layout()
    plt.savefig('results/Confusion Matrix.png')
    plt.show()
