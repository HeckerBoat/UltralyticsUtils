import os
import glob


def remove_lines_starting_with_zero(directory):
    """
    遍历指定目录下所有的 .txt 文件，删除以 0 开头的行并覆盖保存。

    :param directory: 要处理的文件夹路径
    """
    # 使用glob匹配所有.txt文件
    txt_files = glob.glob(os.path.join(directory, "*.txt"))

    for file_path in txt_files:
        with open(file_path, 'r', encoding='utf-8') as file:
            # 读取所有行，过滤掉以0开头的行
            lines = [line for line in file if not line.startswith('11')]

        # 将处理后的行重新写入文件，覆盖原有内容
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(lines)


if __name__ == '__main__':
    # 指定要处理的文件夹路径
    folder_path = 'labels'  # 请替换为实际的文件夹路径
    remove_lines_starting_with_zero(folder_path)
