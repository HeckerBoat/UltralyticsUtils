# 分割掩码可视化工具

## 功能介绍

本工具用于将YOLO格式的分割标签可视化，生成掩码图像。支持两种背景模式：黑色背景和原图背景。

## 目录结构

```
plot_seg_visual/
├── backend/              # 后端功能代码
│   └── plot_seg_visual.py  # 核心可视化功能
├── Frontend/             # 前端界面代码（已弃用）
│   └── main_window.py      # 前端界面实现
├── app.py                # 前端启动入口（已弃用）
├── run_visualization.py  # 命令行脚本入口
└── README.md             # 使用说明
```

## 环境要求

- Python 3.8+
- opencv-python
- numpy
- Pillow
- tqdm

## 安装依赖

```bash
# 使用uv安装依赖
uv pip install opencv-python numpy Pillow tqdm

# 清除缓存（可选）
uv cache clean --force
```

## 使用方法

### 命令行脚本

```bash
# 基本用法
python run_visualization.py --img_path <数据集路径> --cls_path <类别文件路径> [--bg_ground <背景类型>]

# 参数说明
# --img_path: 数据集路径，包含images和labels文件夹
# --cls_path: 类别文件路径，如classes.txt
# --bg_ground: 背景类型，可选值：black（黑色背景）或img（原图背景），默认为black

# 示例
python run_visualization.py --img_path ./dataset --cls_path ./classes.txt --bg_ground black
```

### 前端界面（已弃用）

前端界面已不再推荐使用，建议使用命令行脚本进行操作。

## 输入格式

### 数据集结构

```
dataset/
├── images/      # 存放原图
│   ├── image1.png
│   ├── image2.png
│   └── ...
└── labels/      # 存放YOLO格式的分割标签
    ├── image1.txt
    ├── image2.txt
    └── ...
```

### 标签格式

YOLO格式的分割标签，每行格式如下：

```
<class_id> <x1> <y1> <x2> <y2> ... <xn> <yn>
```

其中：
- `<class_id>`: 类别ID
- `<x1> <y1> ... <xn> <yn>`: 分割多边形的归一化坐标（范围0-1）

### 类别文件

classes.txt文件，每行一个类别名称：

```
person
car
tree
...
```

## 输出结果

生成的掩码图像将保存在数据集路径下的`masks`文件夹中，文件名与原图相同。

## 示例

### 命令示例

```bash
# 使用黑色背景
python run_visualization.py --img_path ./dataset --cls_path ./classes.txt --bg_ground black

# 使用原图背景
python run_visualization.py --img_path ./dataset --cls_path ./classes.txt --bg_ground img
```

### 输出示例

```
开始运行分割掩码可视化...
数据集路径: ./dataset
类别文件: ./classes.txt
背景类型: black
执行命令: python backend/plot_seg_visual.py --img_path ./dataset --cls_path ./classes.txt --bg_ground black
============================================================
saved to ==> ./dataset/masks/image1.png
saved to ==> ./dataset/masks/image2.png

100%|██████████| 2/2 [00:00<00:00, 10.00it/s]

============================================================
分割掩码可视化完成！
结果保存到: ./dataset/masks
```

## 注意事项

1. 确保数据集路径下存在`images`和`labels`文件夹
2. 确保图像文件为PNG格式
3. 确保标签文件与图像文件同名（仅扩展名不同）
4. 类别文件中的类别顺序应与标签中的类别ID对应
