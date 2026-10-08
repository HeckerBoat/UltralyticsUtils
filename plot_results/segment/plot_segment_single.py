import os.path

import pandas as pd
import matplotlib.pyplot as plt

from csv_structure import get_csv_values
from smoother_curve import smooth_by_enhance_right_value, smooth_by_alter_both_value_1, smooth_by_decline_right_value, \
    smooth_by_alter_both_value_2


# 将Y列数据整体调整0.01
def adjust_y_column(data, y_column, enhance_y):
    # 将曲线上下平移提点，确保结果不小于0
    data[y_column] = data[y_column] + enhance_y
    data[y_column] = data[y_column].clip(lower=0)
    return data


def adjust_x_column(data, x_column, adjust_x):
    # 将曲线左右平移提点
    data[x_column] = data[x_column] + adjust_x
    return data


def plot_curve(csv_file, x_column, y_column, cfg=None):
    if cfg is None:
        cfg = get_params()
    # 检查文件是否存在
    if not os.path.exists(csv_file):
        print(f"警告: 文件 {csv_file} 不存在，跳过绘制该模型的曲线")
        return
    # 读取 CSV 文件
    data = pd.read_csv(csv_file)
    data.columns = data.columns.str.strip()

    data = adjust_y_column(data, y_column, cfg['enhance_y'])
    data = adjust_x_column(data, x_column, cfg['adjust_x'])

    # 对曲线平滑处理
    if cfg['smoother']['switch']:
        data[y_column] = cfg['smoother']['choice']['loss_smooth_2'](data[y_column])

    # 绘制曲线图
    plt.plot(data[x_column], data[y_column])

    # 如果不是同一子图模式，添加标题、轴标签、保存和显示图形
    if not cfg['single_subplot']:
        # 添加标题和轴标签
        plt.title(y_column)
        plt.xlabel(x_column)
        plt.ylabel(y_column)

        # 显示图形
        if cfg['show']:
            plt.show()
        # 保存图片
        if cfg['image']:
            if not os.path.exists('results'):
                os.makedirs('results')
            plt.savefig("results/curve.png")
    # 保存csv结果
    if cfg['csv']['save']:
        csv_dir = os.path.dirname(csv_file)
        if not os.path.exists(csv_dir):
            os.makedirs(csv_dir)
        if cfg['csv']['override']:
            data.to_csv(csv_file, index=False)
        else:
            new_csv_file = os.path.join(csv_dir, os.path.basename(csv_file)[0:-4] + '_new.csv')
            data.to_csv(new_csv_file, index=False)


def get_params():
    """
    获取绘图配置参数。
    返回:
        dict: 包含绘图配置参数的字典。
    """
    cfg = {
        # 曲线上下平移的偏移量，值为正向上平移，值为负向下平移
        'enhance_y': 0, 
        # 曲线左右平移的偏移量，值为正向右平移，值为负向左平移
        'adjust_x': 0, 
        # 平滑处理相关配置
        'smoother': {
            # 平滑处理开关，True 开启，False 关闭
            'switch': False,
            'choice': {
            # 使用 smooth_by_enhance_right_value 函数进行指标平滑处理
            'metrics_smooth_1': smooth_by_enhance_right_value,
            # 使用 smooth_by_alter_both_value_1 函数进行指标平滑处理
            'metrics_smooth_2': smooth_by_alter_both_value_1,
            # 使用 smooth_by_decline_right_value 函数进行损失平滑处理
            'loss_smooth_1': smooth_by_decline_right_value,
            # 使用 smooth_by_alter_both_value_2 函数进行损失平滑处理
            'loss_smooth_2': smooth_by_alter_both_value_2,
        }
        },
    # 显示图形的开关，True 显示，False 不显示
    'show': True,  
    # 保存图片的开关，True 保存，False 不保存
    'image': True,  
    # 是否将多个模型的曲线绘制到同一子图，True 同一子图，False 不同子图
    'single_subplot': True, 

    'csv':{
        # 保存 CSV 文件的开关，True 保存，False 不保存
        'save': True,  
        # 'save': False,
        # 覆盖原 CSV 文件的开关，True 覆盖，False 不覆盖
        'override': True,  
        }
    }
    
    return cfg


if __name__ == '__main__':
    y_index = {
        '1': 'train/seg_loss',
        '2': 'train/box_loss',
        '3': 'train/cls_loss',
        '4': 'train/dfl_loss',
        '5': 'val/seg_loss',
        '6': 'val/box_loss',
        '7': 'val/cls_loss',
        '8': 'val/dfl_loss',
        '9': 'metrics/precision(B)',
        '10': 'metrics/recall(B)',
        '11': 'metrics/mAP50(B)',
        '12': 'metrics/mAP50-95(B)',
    }
    # 指定 CSV 文件路径，以及 x 和 y 列的名称
    # models = ['SW-DETR']
    # models = ['RT-DETRv3']
    # models = ['RT-DETRv3','SW-DETR']
    # models = ['baseline']
    # models = ['ours']
    models = ['baseline', 'ours']
    x_column = 'epoch'
    y_column = y_index['2']
    cfg = get_params()
    
    # 如果设置为同一子图，先创建一个图形
    if cfg['single_subplot']:
        plt.figure()
    
    # 调用函数绘制曲线图
    for model in models:
        csv_file = os.path.join('runs', model, 'results.csv')
        if os.path.exists(csv_file):
            plot_curve(csv_file, x_column, y_column, cfg=cfg)
        else:
            print(f"警告: 文件 {csv_file} 不存在，跳过绘制该模型的曲线")
    
    # 如果设置为同一子图，添加图例并保存/显示
    if cfg['single_subplot']:
        plt.xlabel('epoch')
        plt.ylabel('loss')
        plt.legend(models, loc='lower right')
        if cfg['image']:
            if not os.path.exists('results'):
                os.makedirs('results')
            # 提取文件名（移除前缀和(B)后缀）
            filename = y_column
            for head_name in ['train/', 'val/', 'metrics/']:
                filename = filename.replace(head_name, '')
            filename = filename.strip('(B)')
            plt.savefig(f"results/{filename}.png")
        if cfg['show']:
            plt.show()
    
    get_csv_values(models, y_column)
