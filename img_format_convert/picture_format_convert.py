import os
from concurrent.futures import ThreadPoolExecutor

from PIL import Image
from convert import *


def converting(file, input_path, output_path, origin_mode, new_mode):
    file_path = os.path.join(input_path, file)
    # 检查文件是否为 JPG 格式
    if file.lower().endswith(f'.{origin_mode}'):
        try:
            # 打开图像文件
            img = Image.open(file_path)

            # 构造新文件路径和文件名
            new_file_path = os.path.splitext(os.path.join(output_path, file))[0] + f'.{new_mode}'

            # 转换并保存图像为 PNG 格式
            img.save(new_file_path, f'{new_mode.upper()}')

            print(f"转换 '{file}' 完成。")

        except Exception as e:
            print(f"转换 '{file}' 失败: {e}")
    else:
        print(f"文件 '{file}' 不是 {origin_mode} 格式，跳过转换。")


def jpg_to_png(input_path, output_path, origin_mode, new_mode):
    # 检查文件夹是否存在
    if not os.path.exists(input_path):
        print(f"文件夹 '{input_path}' 不存在。")
        return

    # 获取文件夹中所有文件的列表
    files = os.listdir(input_path)

    # 遍历文件夹中的每个文件
    with ThreadPoolExecutor(max_workers=16) as executor:
        for file in files:
            executor.submit(converting, file, input_path, output_path, origin_mode, new_mode)


if __name__ == "__main__":
    input_path = r'G:\论文\图片\汇总'
    output_path = 'D:/输出'
    origin_mode = 'png'
    new_mode = 'jpg'
    png_to_jpg(input_path, output_path)
    # jpg_to_png(input_path, output_path, origin_mode, new_mode)
