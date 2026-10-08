import os

import matplotlib.pylab as plt
import pandas as pd
import numpy as np


# 读取 results.csv 文件的函数
def load_results_csv(name):
    csv_file = f'runs/{name}/results.csv'
    data = pd.read_csv(csv_file)
    data.columns = data.columns.str.strip()
    return data

# 绘制精度曲线
def plot_precision(plt, names):
    plt.subplot(1, 3, 1)
    for i in names:
        data = load_results_csv(i)
        plt.plot(data['metrics/precision(B)'], label=i)
    plt.xlabel('epoch')
    plt.title('precision')
    plt.legend()

# 绘制召回率曲线
def plot_recall(plt, names):
    plt.subplot(1, 3, 2)
    for i in names:
        data = load_results_csv(i)
        plt.plot(data['metrics/recall(B)'], label=i)
    plt.xlabel('epoch')
    plt.title('recall')
    plt.legend()

# 绘制 mAP50 曲线
def plot_mAP50(plt, names):
    plt.subplot(1, 3, 3)
    for i in names:
        data = load_results_csv(i)
        plt.plot(data['metrics/mAP50(B)'], label=i)
    plt.xlabel('epoch')
    plt.title('mAP@50')
    plt.legend()

# 绘制训练分割损失曲线
def plot_train_seg_loss(plt, names):
    plt.subplot(1, 3, 1)
    for i in names:
        data = load_results_csv(i)
        plt.plot(data['train/seg_loss'], label=i)
    plt.xlabel('epoch')
    plt.title('seg_loss')
    plt.legend()

# 绘制训练分类损失曲线
def plot_train_cls_loss(plt, names):
    plt.subplot(1, 3, 2)
    for i in names:
        data = load_results_csv(i)
        plt.plot(data['train/cls_loss'], label=i)
    plt.xlabel('epoch')
    plt.title('cls_loss')
    plt.legend()

# 绘制训练 DFL 损失曲线
def plot_train_dfl_loss(plt, names):
    plt.subplot(1, 3, 3)
    for i in names:
        data = load_results_csv(i)
        plt.plot(data['train/dfl_loss'], label=i)
    plt.xlabel('epoch')
    plt.title('dfl_loss')
    plt.legend()

# 绘制并保存曲线的通用函数
def plot_and_save_curve(plt, pwd, path, save=False):
    plt.tight_layout()
    if not os.path.exists('results'):
        os.mkdir('results')
    if save:
        plt.savefig(path)
        print(f'{os.path.basename(path)} save in {pwd}/{path}')
    plt.show()

# 保存指标曲线
def save_metrics_curve(plt, names, pwd, metrics_path, save=False):
    plt.figure(figsize=(15, 5))
    plot_precision(plt, names)
    plot_recall(plt, names)
    plot_mAP50(plt, names)
    plot_and_save_curve(plt, pwd, metrics_path, save=save)

# 保存损失曲线
def save_loss_curve(plt, names, pwd, loss_path, save=False):
    plt.figure(figsize=(15, 5))
    plot_train_seg_loss(plt, names)
    plot_train_cls_loss(plt, names)
    plot_train_dfl_loss(plt, names)
    plot_and_save_curve(plt, pwd, loss_path, save=save)

# 保存所有曲线
def save_all_curve(plt, names, pwd, hub_path, save=False):
    plt.figure(figsize=(15, 10))
    plot_precision(plt, names)
    plot_recall(plt, names)
    plot_mAP50(plt, names)
    plot_train_seg_loss(plt, names)
    plot_train_cls_loss(plt, names)
    plot_train_dfl_loss(plt, names)
    # 修正调用
    plot_and_save_curve(plt, pwd, hub_path, save=save)

if __name__ == '__main__':
    pwd = os.getcwd()
    metrics_path = 'results/metrics_curve.png'
    loss_path = 'results/loss_curve.png'
    hub_path='results/all_curve.png'
    names = os.listdir('runs')

    # 画 metrics_curve
    save_metrics_curve(plt, names, pwd, metrics_path, save=True)

    # 画 loss_curve
    # save_loss_curve(plt, names, pwd, loss_path, save=True)

    # save_all_curve(plt, names, pwd, metrics_path, save=True)
    
    
