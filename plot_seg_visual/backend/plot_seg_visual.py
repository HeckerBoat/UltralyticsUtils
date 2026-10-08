import argparse
import os
import sys

import cv2
import numpy as np
from PIL import Image
from tqdm import tqdm


def get_background(bg_choice, img_path):
    if bg_choice == 'black':
        # 使用PIL读取图片信息，支持中文路径
        try:
            image = Image.open(img_path)
            img_array = np.array(image)
            if img_array is None:
                print(f"警告：无法读取图片文件 {img_path}")
                return None
            img_x = img_array.shape[0]
            img_y = img_array.shape[1]
            return np.zeros((img_x, img_y, 3))  # 三通道黑色背景，支持彩色绘制
        except Exception as e:
            print(f"警告：无法读取图片文件 {img_path}: {e}")
            return None
    elif bg_choice == 'img':
        try:
            image = Image.open(img_path)
            img_array = np.array(image)
            # 确保返回三通道图像
            if len(img_array.shape) == 2:
                # 灰度图像转换为三通道
                img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2BGR)
            elif img_array.shape[2] == 1:
                # 单通道图像转换为三通道
                img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2BGR)
            return img_array
        except Exception as e:
            print(f"警告：无法读取图片文件 {img_path}: {e}")
            return None


# 解析坐标
def parse_data(img_x, img_y, line):
    # 处理每一行的内容
    data = line.split('\n')[0]
    d = data.split(' ', -1)
    data = []

    # 从索引1开始，每次步长为2，遍历所有坐标对
    for i in range(1, len(d), 2):
        if i + 1 < len(d):
            try:
                data.append([img_y * float(d[i]), img_x * float(d[i + 1])])
            except ValueError:
                continue

    data = np.array(data, dtype=np.int32)
    return data


def draw_masks(img_path, txt_path, colors, save_dir, name, bg_choice):
    # 使用PIL读取图片信息，支持中文路径
    try:
        image = Image.open(img_path)
        img_array = np.array(image)
        if img_array is None:
            print(f"警告：无法读取图片文件 {img_path}")
            return
        img_x = img_array.shape[0]
        img_y = img_array.shape[1]
    except Exception as e:
        print(f"警告：无法读取图片文件 {img_path}: {e}")
        return
    
    img_save = get_background(bg_choice, img_path)
    if img_save is None:
        print(f"警告：无法创建背景 {img_path}")
        return
    
    if os.path.exists(txt_path):
        # 打开文件
        with open(txt_path, "r", encoding='utf-8') as f:
            # 逐行读取文件内容
            for line in f:
                # 确保行不为空
                line = line.strip()
                if not line:
                    continue
                try:
                    # 获取类别索引
                    class_idx = int(line[0])
                    if class_idx >= len(colors):
                        print(f"警告：类别索引 {class_idx} 超出范围，使用默认颜色")
                        color = (255, 255, 255)
                    else:
                        color = colors[class_idx]
                    
                    data = parse_data(img_x, img_y, line)
                    if len(data) > 0:
                        # 只绘制当前多边形，不累积
                        cv2.fillPoly(img_save, [data], color=color)
                except (ValueError, IndexError) as e:
                    print(f"警告：处理标签文件时出错 {txt_path}: {e}")
                    continue
        
        # 确保保存目录存在
        os.makedirs(save_dir, exist_ok=True)
        
        # 保存结果
        save_path = os.path.join(save_dir, f"{name}.png")
        try:
            # 使用cv2.imencode支持中文路径
            success, encoded_image = cv2.imencode('.png', img_save)
            if success:
                with open(save_path, 'wb') as f:
                    f.write(encoded_image)
                print(f'saved to ==> {save_path}')
            else:
                print(f"警告：无法编码图片 {save_path}")
        except Exception as e:
            print(f"警告：无法保存图片 {save_path}: {e}")


# 获取颜色
def get_colors(num):
    colors = []
    if num == 0:
        return colors
    
    # 预定义一些鲜艳的颜色，确保不同类别有明显区别
    predefined_colors = [
        (0, 0, 255),   # 红色
        (0, 255, 0),   # 绿色
        (255, 0, 0),   # 蓝色
        (0, 255, 255), # 黄色
        (255, 0, 255), # 洋红色
        (255, 255, 0), # 青色
        (128, 0, 0),   # 深红色
        (128, 128, 0), # 橄榄色
        (0, 128, 0),   # 深绿色
        (128, 0, 128), # 紫色
        (0, 128, 128), # 蓝绿色
        (0, 0, 128),   # 深蓝色
        (255, 165, 0), # 橙色
        (192, 192, 192),# 银色
        (128, 128, 128),# 灰色
        (255, 255, 255),# 白色
        (139, 0, 0),   # 深红色
        (0, 100, 0),   # 深绿色
        (0, 0, 139),   # 深蓝色
        (139, 139, 0)  # 暗黄色
    ]
    
    # 如果类别数量小于预定义颜色数量，直接使用预定义颜色
    if num <= len(predefined_colors):
        return predefined_colors[:num]
    
    # 如果类别数量超过预定义颜色数量，生成更多颜色
    # 使用预定义颜色作为基础
    colors = predefined_colors.copy()
    # 使用集合来跟踪已使用的颜色，确保唯一性
    used_colors = set(predefined_colors)
    
    # 生成剩余的颜色
    for i in range(len(predefined_colors), num):
        # 计算色相值，均匀分布在0-360之间
        hue = i * 137.5  # 使用黄金角度，生成更均匀的颜色分布
        hue %= 360
        
        # 转换为RGB颜色
        # 参考：https://stackoverflow.com/questions/24852345/hsv-to-rgb-color-conversion
        c = 255  # 饱和度
        x = c * (1 - abs((hue / 60) % 2 - 1))
        m = 0  # 亮度偏移
        
        if 0 <= hue < 60:
            r, g, b = c, x, 0
        elif 60 <= hue < 120:
            r, g, b = x, c, 0
        elif 120 <= hue < 180:
            r, g, b = 0, c, x
        elif 180 <= hue < 240:
            r, g, b = 0, x, c
        elif 240 <= hue < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        
        r, g, b = int(r + m), int(g + m), int(b + m)
        # OpenCV使用BGR格式
        color = (b, g, r)
        
        # 确保颜色唯一，如果重复则重新生成
        while color in used_colors:
            # 稍微调整色相值，生成新的颜色
            hue = (hue + 10) % 360
            x = c * (1 - abs((hue / 60) % 2 - 1))
            if 0 <= hue < 60:
                r, g, b = c, x, 0
            elif 60 <= hue < 120:
                r, g, b = x, c, 0
            elif 120 <= hue < 180:
                r, g, b = 0, c, x
            elif 180 <= hue < 240:
                r, g, b = 0, x, c
            elif 240 <= hue < 300:
                r, g, b = x, 0, c
            else:
                r, g, b = c, 0, x
            r, g, b = int(r + m), int(g + m), int(b + m)
            color = (b, g, r)
        
        # 添加新颜色并更新已使用颜色集合
        colors.append(color)
        used_colors.add(color)
    
    return colors


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--img_path', type=str, default=os.getcwd())
    parser.add_argument('--cls_path', type=str, default=fr'./classes.txt')
    parser.add_argument('--bg_ground', type=str, default=fr'black', choices=['black', 'img'])
    parser.add_argument('--class_color', type=str, default='auto', choices=['auto', 'white'])
    return parser.parse_args()


def get_cls(cls_path):
    with open(cls_path, 'r', encoding='utf-8') as f:
        classes = f.read().split('\n')
    return classes


def run():
    # txt文件夹操作
    args = get_args()
    dataset_dir = args.img_path
    img_dir = os.path.join(dataset_dir, 'images')
    txt_dir = os.path.join(dataset_dir, 'labels')
    save_dir = os.path.join(dataset_dir, 'masks')
    
    # 创建保存目录
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    files = os.listdir(img_dir)
    classes = get_cls(args.cls_path)
    class_color = args.class_color
    if class_color == 'white':
        # 统一使用白色
        colors = [(255, 255, 255)] * len(classes)
    else:
        # 不同类别使用不同颜色
        colors = get_colors(len(classes))
    bg_choice = args.bg_ground


    # 过滤出图片文件（支持jpg和png）
    image_files = []
    for file in files:
        if file.endswith('.png') or file.endswith('.jpg'):
            image_files.append(file)
    
    for file in tqdm(image_files, total=len(image_files)):
        # 获取文件名（不包含扩展名）
        name = os.path.splitext(file)[0]
        # 根据原始文件扩展名构建图片路径
        img_path = fr"{img_dir}/{file}"
        txt_path = fr"{txt_dir}/{name}.txt"

        draw_masks(img_path, txt_path, colors, save_dir, name, bg_choice)  # 将每张图中的mask画出来


if __name__ == '__main__':
    run()
