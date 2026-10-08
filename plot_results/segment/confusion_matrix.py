# confusion_matrix
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams


def draw_matrix(confusion_matrix, name):
    proportion = []
    length = len(confusion_matrix)
    print(length)
    for i in confusion_matrix:
        for j in i:
            temp = j / (np.sum(i))
            proportion.append(temp)
    # print(np.sum(confusion_matrix[0]))
    # print(proportion)
    pshow = []
    for i in proportion:
        pt = "{:.2}".format(i)
        pshow.append(pt)
    proportion = np.array(proportion).reshape(length, length)  # reshape(列的长度，行的长度)
    pshow = np.array(pshow).reshape(length, length)
    # print(pshow)
    config = {
        "font.family": 'Times New Roman',  # 设置字体类型
    }
    rcParams.update(config)
    plt.imshow(proportion, interpolation='nearest', cmap=plt.cm.Blues)  # 按照像素显示出矩阵
    # (改变颜色：'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds','YlOrBr', 'YlOrRd',
    # 'OrRd', 'PuRd', 'RdPu', 'BuPu','GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn')
    # plt.title('confusion_matrix')
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, fontsize=12, rotation=90)
    plt.yticks(tick_marks, classes, fontsize=12)

    thresh = confusion_matrix.max() / 2.
    # iters = [[i,j] for i in range(len(classes)) for j in range((classes))]

    iters = np.reshape([[[i, j] for j in range(length)] for i in range(length)], (confusion_matrix.size, 2))
    fontsize = 8
    for i, j in iters:
        if i == j:
            plt.text(j, i - 0.12, format(confusion_matrix[i, j]), va='center', ha='center', fontsize=fontsize,
                     color='white',
                     weight=5)  # 显示对应的数字
            plt.text(j, i + 0.12, pshow[i, j], va='center', ha='center', fontsize=fontsize, color='white')
        else:
            plt.text(j, i - 0.12, format(confusion_matrix[i, j]), va='center', ha='center',
                     fontsize=fontsize)  # 显示对应的数字
            plt.text(j, i + 0.12, pshow[i, j], va='center', ha='center', fontsize=fontsize)

    plt.ylabel('True', fontsize=16)
    plt.xlabel('Predict', fontsize=16)
    plt.title('Confusion Matrix')
    plt.tight_layout()
    plt.savefig(f'results/{name}.png')
    plt.show()


if __name__ == '__main__':
    classes = ['Galinsoga', 'Alternanthera', 'Cerastium', 'Cardamine', 'Amaranthus', 'Pilea', 'background']
    # 优化前
    pre_model = np.array(
        object=[[4512, 256, 126, 221, 123, 123, 12],
                [208, 4535, 252, 93, 246, 144, 15],
                [101, 271, 4879, 256, 153, 223, 6],
                [134, 205, 404, 4235, 74, 161, 8],
                [112, 83, 103, 189, 4610, 62, 14],
                [233, 182, 156, 352, 133, 4378, 6],
                [12, 3, 3, 5, 2, 2, 0],
                ], dtype=np.int32)  # 输入特征矩阵
    # 优化后
    better_model = np.array(
        object=[[4932, 124, 63, 432, 78, 95, 5],
                [108, 4612, 152, 123, 216, 124, 9],
                [102, 251, 4979, 206, 143, 203, 0],
                [214, 155, 204, 4555, 54, 101, 5],
                [112, 34, 213, 145, 4878, 42, 8],
                [123, 142, 226, 234, 123, 4758, 4],
                [7, 1, 2, 5, 4, 2, 0],
                ], dtype=np.int32)  # 输入特征矩阵
    draw_matrix(confusion_matrix=pre_model, name='baseline_CM')
    draw_matrix(confusion_matrix=better_model, name='ours_CM')
