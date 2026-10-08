import os

import matplotlib.pylab as plt
import pandas as pd
import numpy as np


def plot_precision(plt, names):
    plt.subplot(2, 2, 1)
    for i in names:
        csv_file = f'runs/{i}/results.csv'
        data = pd.read_csv(csv_file)
        data.columns = data.columns.str.strip()
        plt.plot(data['metrics/precision(B)'], label=i)
    plt.xlabel('epoch')
    plt.title('precision')
    plt.legend()


def plot_recall(plt, names):
    plt.subplot(2, 2, 2)
    for i in names:
        csv_file = f'runs/{i}/results.csv'
        data = pd.read_csv(csv_file)
        data.columns = data.columns.str.strip()
        plt.plot(data['metrics/recall(B)'], label=i)
    plt.xlabel('epoch')
    plt.title('recall')
    plt.legend()


def plot_mAP50(plt, names):
    plt.subplot(2, 2, 3)
    for i in names:
        csv_file = f'runs/{i}/results.csv'
        data = pd.read_csv(csv_file)
        data.columns = data.columns.str.strip()
        plt.plot(data['metrics/mAP50(B)'], label=i)
    plt.xlabel('epoch')
    plt.title('mAP50')
    plt.legend()


def plot_mAP50_95(plt, names):
    plt.subplot(2, 2, 4)
    for i in names:
        csv_file = f'runs/{i}/results.csv'
        data = pd.read_csv(csv_file)
        data.columns = data.columns.str.strip()
        plt.plot(data['metrics/mAP50-95(B)'], label=i)
    plt.xlabel('epoch')
    plt.title('mAP50:95')
    plt.legend()


def plot_params(plt, x_values, y_values):
    plt.subplot(2, 2, 4)
    plt.bar(x=x_values, height=y_values, width=0.5, align='center')
    plt.xlabel('model')
    plt.title('parameters(M)')
    plt.legend()

def plot_f1_score(plt, names):
    plt.subplot(1,1,1)
    for i in names:
        csv_file = f'runs/{i}/results.csv'
        data = pd.read_csv(csv_file)
        data.columns = data.columns.str.strip()
        precision = data['metrics/precision(B)']
        recall = data['metrics/recall(B)']
        f1_score = 2 * (precision * recall) / (precision + recall)
        plt.plot(f1_score, label=i)
    plt.xlabel('epoch')
    plt.title('F1-Score')
    plt.legend()

def save_metrics(plt, pwd, metrics_path, save=False):
    plt.tight_layout()
    if not os.path.exists('results'):
        os.mkdir('results')
    if save:
        plt.savefig(metrics_path)
        print(f'metrics_curve.png save in {pwd}/{metrics_path}')
    plt.show()


def plot_box_loss(plt, names):
    plt.subplot(2, 3, 1)
    for i in names:
        data = pd.read_csv(f'runs/{i}/results.csv')
        data.columns = data.columns.str.strip()
        plt.plot(data['/box_loss'], label=i)
    plt.xlabel('epoch')
    plt.title('/box_loss')
    plt.legend()


def plot_dfl_loss(plt, names):
    plt.subplot(2, 3, 2)
    for i in names:
        csv_file = f'runs/{i}/results.csv'
        data = pd.read_csv(csv_file)
        data.columns = data.columns.str.strip()
        plt.plot(data['/dfl_loss'], label=i)
    plt.xlabel('epoch')
    plt.title('/dfl_loss')
    plt.legend()


def plot_cls_loss(plt, names):
    plt.subplot(2, 3, 3)
    for i in names:
        csv_file = f'runs/{i}/results.csv'
        data = pd.read_csv(csv_file)
        data.columns = data.columns.str.strip()
        plt.plot(data['/cls_loss'], label=i)
    plt.xlabel('epoch')
    plt.title('/cls_loss')
    plt.legend()


def plot_val_box_loss(plt, names):
    plt.subplot(2, 3, 4)
    for i in names:
        csv_file = f'runs/{i}/results.csv'
        data = pd.read_csv(csv_file)
        data.columns = data.columns.str.strip()
        plt.plot(data['val/box_loss'], label=i)
    plt.xlabel('epoch')
    plt.title('val/box_loss')
    plt.legend()


def plot_val_dfl_loss(plt, names):
    plt.subplot(2, 3, 5)
    for i in names:
        csv_file = f'runs/{i}/results.csv'
        data = pd.read_csv(csv_file)
        data.columns = data.columns.str.strip()
        plt.plot(data['val/dfl_loss'], label=i)
    plt.xlabel('epoch')
    plt.title('val/dfl_loss')
    plt.legend()


def plot_val_cls_loss(plt, names):
    plt.subplot(2, 3, 6)
    for name in names:
        csv_file = f'runs/{name}/results.csv'
        data = pd.read_csv(csv_file)
        data.columns = data.columns.str.strip()
        plt.plot(data['val/cls_loss'], label=name)
    plt.xlabel('epoch')
    plt.title('val/cls_loss')
    plt.legend()


def plot_loss_curve(plt, pwd, loss_path, save=True):
    plt.tight_layout()
    if save:
        plt.savefig(loss_path)
        print(f'loss_curve.png save in {pwd}/{loss_path}')
    plt.show()


def metrics_curve(plt, names, pwd, metrics_path, save=False):
    # 画metrics_curve
    plt.figure(figsize=(10, 10))
    # plot_precision(plt, names)
    # plot_recall(plt, names)
    plot_f1_score(plt, names)
    # plot_mAP50(plt, names)
    # plot_mAP50_95(plt, names)
    # plot_params(plt, names, [6.2, 9.4])
    save_metrics(plt, pwd, metrics_path, save=save)


def loss_curve(plt, names, pwd, loss_path, save=False):
    # 画loss_curve
    plt.figure(figsize=(15, 10))
    plot_box_loss(plt, names)
    plot_dfl_loss(plt, names)
    plot_cls_loss(plt, names)
    # plot_val_box_loss(plt, names)
    # plot_val_dfl_loss(plt, names)
    # plot_val_cls_loss(plt, names)
    plot_loss_curve(plt, pwd, loss_path, save=save)


if __name__ == '__main__':
    pwd = os.getcwd()
    metrics_path = 'results/metrice_curve.png'
    loss_path = 'results/loss_curve.png'
    names = os.listdir('./runs')
    # 画F1-Score
    metrics_curve(plt, names, pwd, metrics_path, save=True)

    # 画metrics_curve
    # metrics_curve(plt, names, pwd, metrics_path, save=False)

    # 画loss_curve
    # loss_curve(plt, names, pwd, loss_path, save=True)