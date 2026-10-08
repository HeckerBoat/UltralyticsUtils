import matplotlib.pyplot as plt
import random


def random_color(classes_num):
    colors = set()
    """
    生成随机颜色代码
    """
    while len(colors) != classes_num:
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        color = f'#{r:02x}{g:02x}{b:02x}'  # 将RGB值格式化为十六进制颜色代码
        if color not in colors:
            colors.add(color)
    return colors


def plot_bar_chart(data):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    x_values = list(data.keys())
    y_values = list(data.values())

    plt.bar(x_values, y_values, color=random_color(classes_num=len(x_values)))
    plt.xlabel('Labels')
    # plt.ylabel('number')
    plt.title('Number of total labels')
    plt.xticks(rotation=90)  # 设置 x 轴标签竖着写
    plt.tight_layout()
    plt.savefig('results/labels.png')
    plt.show()


if __name__ == '__main__':
    # 数量放大倍数
    N = 1
    # 示例字典
    data = {
        'Galinsoga': 4896 * N,
        'Alternanthera': 6245 * N,
        'Cerastium': 5128 * N,
        'Oxalis': 5456 * N,
        'Cardamine': 4625 * N,
        'Amaranthus': 5576 * N,
        'Hemistepta': 4324 * N,
        'Eleusine': 5435 * N,
    }
    # 调用函数绘制条形图
    plot_bar_chart(data)
