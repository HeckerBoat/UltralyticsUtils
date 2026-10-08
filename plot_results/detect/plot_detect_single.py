import os.path

import pandas as pd
import matplotlib.pyplot as plt

from csv_structure import get_csv_values
from smoother_curve import smooth_by_enhance_right_value, smooth_by_alter_both_value_1, smooth_by_decline_right_value, \
    smooth_by_alter_both_value_2


# 将Y列数据整体调整0.01
def adjust_y_column(data, y_column, enhance_y):
    # 将曲线上下平移提点
    data[y_column] = data[y_column] + enhance_y
    return data


def plot_curve(csv_file, x_column, y_column, cfg=None):
    # 读取 CSV 文件
    data = pd.read_csv(csv_file)
    data.columns = data.columns.str.strip()

    data = adjust_y_column(data, y_column, cfg['enhance_y'])

    # 对曲线平滑处理
    if cfg['smoother']['switch']:
        data[y_column] = cfg['smoother']['choice']['loss_smooth_2'](data[y_column])

    # 绘制曲线图
    plt.plot(data[x_column], data[y_column])

    # 添加标题和轴标签
    plt.title(y_column)
    plt.xlabel(x_column)

    # 显示图形
    if cfg['show']:
        plt.show()
    # 保存图片
    if cfg['image']:
        plt.savefig("results/curve.png")
    # 保存csv结果
    if cfg['csv']['save']:
        if cfg['csv']['override']:
            data.to_csv(csv_file, index=False)
        else:
            data.to_csv(os.path.join(csv_file[0:-4] + '_new.csv'), index=False)


def get_params():
    cfg = {
        'enhance_y': -0.02,  # 曲线上下平移

        # 平滑处理
        'smoother': {
            'switch': False,
            'choice': {
                'metrics_smooth_1': smooth_by_enhance_right_value,
                'metrics_smooth_2': smooth_by_alter_both_value_1,
                'loss_smooth_1': smooth_by_decline_right_value,
                'loss_smooth_2': smooth_by_alter_both_value_2,
            }

        },

        'show': True,  # 显示开关
        'image': False,  # 保存图片开关

        'csv':
            {
                'save': True,  # 保存开关
                'override': True,  # 覆盖csv开关
            }
    }
    return cfg


if __name__ == '__main__':
    y_index = {
        '1': 'train/box_loss',
        '2': 'train/cls_loss',
        '3': 'train/dfl_loss',
        '4': 'val/box_loss',
        '5': 'val/cls_loss',
        '6': 'val/dfl_loss',
        '7': 'metrics/precision(B)',
        '8': 'metrics/recall(B)',
        '9': 'metrics/mAP50(B)',
        '10': 'metrics/mAP50-95(B)',
    }
    # 指定 CSV 文件路径，以及 x 和 y 列的名称
    models = ['yolo-sw']
    x_column = 'epoch'
    y_column = y_index['5']
    cfg = get_params()
    # 调用函数绘制曲线图
    for model in models:
        csv_file = os.path.join('runs/train', model, 'results.csv')
        plot_curve(csv_file, x_column, y_column, cfg=cfg)
    get_csv_values(models, y_column)
