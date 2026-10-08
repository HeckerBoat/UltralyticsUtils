import os
import re
import shutil

png_dir = fr'G:\论文\图片\汇总'
save_dir = fr"G:\论文\图片\汇总\temp"
if not os.path.exists(save_dir):
    os.mkdir(save_dir)
N = 1

# 获取当前目录下的所有文件
files = os.listdir(png_dir)

# 遍历文件列表
for file in files:
    # 检查文件名是否以"Fig"开头
    if file.startswith("Fig"):
        # 使用正则表达式提取数字
        match = re.search(r'\d+', file)
        if match:
            # 提取数字
            number = int(match.group())
            # 数字加1
            new_number = number + N
            # 构建新的文件名
            new_filename = f"Fig{new_number}.png"
            old_path = fr"{png_dir}/{file}"
            new_path = fr"{save_dir}/{new_filename}"
            # 重命名文件
            shutil.copy(old_path, new_path)
