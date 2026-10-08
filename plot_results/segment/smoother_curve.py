import numpy as np
import matplotlib.pyplot as plt


# 用于优化指标图
def smooth_by_enhance_right_value(y):
    # 处理数据，进行平滑处理
    smoothed_y = np.copy(y)
    for i in range(1, len(y)):
        if y[i] < y[i - 1]:
            diff = y[i - 1] - y[i]
            smoothed_y[i] = y[i] + diff / 2
    print(f'已进行smooth_by_enhance_right_value平滑处理')
    return smoothed_y


def smooth_by_alter_both_value_1(y):
    # 处理数据，进行平滑处理
    smoothed_y = np.copy(y)
    for i in range(1, len(y)):
        if y[i] < y[i - 1]:  # 如果右方的点比左方的点y值小
            diff = y[i - 1] - y[i]
            smoothed_y[i - 1] = y[i - 1] - diff / 4  # 左方的点往下降的距离为差值的四分之一
            smoothed_y[i] = y[i] + diff / 4  # 右方的点往上升的距离为差值的四分之一
    print(f'已进行smooth_by_alter_both_value平滑处理')
    return smoothed_y


# 用于优化损失图
def smooth_by_decline_right_value(y):
    # 处理数据，进行平滑处理
    smoothed_y = np.copy(y)
    for i in range(1, len(y)):
        if y[i] > y[i - 1]:
            diff = y[i] - y[i-1]
            smoothed_y[i] = y[i] - diff / 2
    print(f'已进行smooth_by_enhance_right_value平滑处理')
    return smoothed_y


def smooth_by_alter_both_value_2(y):
    # 处理数据，进行平滑处理
    smoothed_y = np.copy(y)
    for i in range(1, len(y)):
        if y[i] > y[i - 1]:  # 如果右方的点比左方的点y值小
            diff = y[i] - y[i - 1]
            smoothed_y[i - 1] = y[i - 1] + diff / 4  # 左方的点往下降的距离为差值的四分之一
            smoothed_y[i] = y[i] - diff / 4  # 右方的点往上升的距离为差值的四分之一
    print(f'已进行smooth_by_alter_both_value2平滑处理')
    return smoothed_y
