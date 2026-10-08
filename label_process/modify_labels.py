import os
from concurrent.futures import ThreadPoolExecutor


def replace_file_start(file_path):
    old = '10'
    new = '5'
    with open(file_path, 'r') as file:
        lines = file.readlines()
        # 将以10开头的行替换为以9开头的行
    lines = [line.replace(old, new, 1) if line.strip().startswith(old) else line for line in lines]
    # lines = [line.replace('11', '10', 1) if line.strip().startswith('11') else line for line in lines]
    with open(file_path, 'w') as file:
        file.writelines(lines)


# 检查标签
def verify(file_path):
    find = '6'
    with open(file_path, 'r') as file:
        lines = file.readlines()
    [print(line, end='') if line.strip().startswith(find) else line for line in lines]


# 移动
def remove_target_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    # 删除指定行
    lines = [line for line in lines if not line.strip().startswith('11')]
    # lines = [print(line) for line in lines if line.strip().startswith('3')]
    with open(file_path, 'w') as file:
        file.writelines(lines)


# 将任务分配给每个线程
def process_folder(folder_path):
    with ThreadPoolExecutor(max_workers=10) as executor:
        files = os.listdir(folder_path)
        for file_name in files:
            if file_name.endswith('.txt'):
                file_path = os.path.join(folder_path, file_name)
                # print(file_path)
                # 在这里修改执行函数
                # 先删，再挪，最后检查
                # executor.submit(remove_target_lines, file_path)
                # executor.submit(replace_file_start, file_path)
                executor.submit(verify, file_path)


if __name__ == "__main__":
    source_path = r"labels"
    process_folder(source_path)
    # print(source_path)
