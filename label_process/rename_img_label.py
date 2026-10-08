import os
import random
import string


# 生成9位不重复的随机数字的函数
def generate_unique_random_numbers(count):
    used_numbers = set()
    random_numbers = []
    while len(random_numbers) < count:
        num = ''.join(random.choice(string.digits) for _ in range(9))
        if num not in used_numbers:
            used_numbers.add(num)
            random_numbers.append(num)
    return random_numbers


def random_rename_img_label(img_folder, label_folder):
    # 获取图片文件列表（支持常见的几种图片格式，可按需扩展）
    image_files = [f for f in os.listdir(img_folder) if f.endswith(('.jpg', '.png', '.jpeg'))]
    # 获取txt文件列表，确保和图片文件一一对应，数量相等
    txt_files = [f for f in os.listdir(label_folder) if f.endswith('.txt')]
    if len(image_files) != len(txt_files):
        print("图片文件和txt文件数量不一致，请检查文件夹内容！")
        exit(1)

    # 生成和文件数量相等的不重复的随机数字
    random_numbers = generate_unique_random_numbers(len(image_files))

    # 重命名图片文件
    for index, image_file in enumerate(image_files):
        old_image_path = os.path.join(img_folder, image_file)
        new_image_name = random_numbers[index] + os.path.splitext(image_file)[1]
        new_image_path = os.path.join(img_folder, new_image_name)
        os.rename(old_image_path, new_image_path)

    # 重命名txt文件
    for index, txt_file in enumerate(txt_files):
        old_txt_path = os.path.join(label_folder, txt_file)
        new_txt_name = random_numbers[index] + os.path.splitext(txt_file)[1]
        new_txt_path = os.path.join(label_folder, new_txt_name)
        os.rename(old_txt_path, new_txt_path)


def rename_img_label(img_folder, label_folder, category):
    # A文件夹路径，存放图片
    folder_a = img_folder
    # B文件夹路径，存放对应的txt文件
    folder_b = label_folder

    # 用于记录重命名的序号，从1开始
    count = 1

    # 获取A文件夹下所有图片文件的文件名列表
    image_files = [f for f in os.listdir(folder_a) if f.endswith(('.jpg', '.png', '.jpeg'))]

    for image_file in image_files:
        # 新的图片文件名格式
        new_image_name = f"{category}_{count}.jpg"
        old_image_path = os.path.join(folder_a, image_file)
        new_image_path = os.path.join(folder_a, new_image_name)
        os.rename(old_image_path, new_image_path)

        # 对应txt文件的旧文件名和新文件名（假设txt文件和图片文件只是扩展名不同，名称主体一致）
        txt_file_name = os.path.splitext(image_file)[0] + ".txt"
        new_txt_name = f"{category}_{count}.txt"
        old_txt_path = os.path.join(folder_b, txt_file_name)
        new_txt_path = os.path.join(folder_b, new_txt_name)
        if os.path.exists(old_txt_path):
            os.rename(old_txt_path, new_txt_path)

        count += 1


def run(work_folder, category):
    img_folder = fr'{work_folder}\{category}\images'
    label_folder = fr'{work_folder}\{category}\labels'
    random_rename_img_label(img_folder, label_folder)
    rename_img_label(img_folder, label_folder, category)


if __name__ == '__main__':
    work_folder = fr'G:\datasets\SoybeanWeed\segment'
    categorys = ['Galinsoga', 'Alternanthera', 'Amaranthus', 'Cardamine', 'Cerastium', 'Pilea']
    for category in categorys:
        run(work_folder, category)
