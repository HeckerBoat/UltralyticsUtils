import os


def check_txt_delete_jpg(folder_a, folder_b):
    # 获取A文件夹下所有的jpg文件
    jpg_files = [f for f in os.listdir(folder_a) if f.endswith('.jpg')]
    for jpg_file in jpg_files:
        base_name = os.path.splitext(jpg_file)[0]
        txt_file_name = base_name + ".txt"
        txt_file_path = os.path.join(folder_b, txt_file_name)
        if not os.path.exists(txt_file_path):
            jpg_file_path = os.path.join(folder_a, jpg_file)
            os.remove(jpg_file_path)
            print(fr'{jpg_file_path} removed')


def check_jpg_delete_txt(folder_a, folder_b):
    # 获取A文件夹下所有txt文件的文件名（不含路径，仅文件名）
    txt_files_in_b = [file for file in os.listdir(folder_b) if file.endswith('.txt')]

    for txt_file in txt_files_in_b:
        # 去除扩展名，获取文件名主体部分（用于对比同名情况）
        file_name_without_ext = os.path.splitext(txt_file)[0]
        # 构造对应的jpg文件名
        jpg_file_name = file_name_without_ext + ".jpg"
        jpg_file_path = os.path.join(folder_a, jpg_file_name)
        if not os.path.exists(jpg_file_path):
            txt_file_path = os.path.join(folder_b, txt_file)
            os.remove(txt_file_path)
            print(fr'{txt_file_path} removed')


if __name__ == "__main__":
    folder_a = fr"G:\datasets\SoybeanWeed\test\images"  # 存放jpg图片的文件夹路径，可根据实际情况修改
    folder_b = fr"G:\datasets\SoybeanWeed\test\labels"  # 存放txt文件的文件夹路径，可根据实际情况修改
    # check_txt_delete_jpg(folder_a, folder_b)  # 根据标签删除图片
    check_jpg_delete_txt(folder_a, folder_b)  # 根据图片删除标签
