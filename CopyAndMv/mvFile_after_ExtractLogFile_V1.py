import os
import re
import shutil


def traverse_folder(folder, only_first=False):
    folder = os.path.abspath(folder)
    all_files = []
    all_dirs = []
    if os.path.isdir(folder):
        for root, dirs, files in os.walk(folder):
            for one_file in files:
                all_files.append(os.path.join(root, one_file))  # 所有文件
            for one_dir in dirs:
                all_dirs.append(os.path.join(root, one_dir))  # 所有文件夹
            if only_first:
                break
    else:
        msg = 'Can not find folder:{} for traverse'.format(folder)
        print(msg)
    return all_dirs, all_files


def create_folder(folder):
    folder = os.path.abspath(folder)
    if not os.path.exists(folder):
        try:
            os.makedirs(folder)
            msg = 'Success create folder:{}'.format(folder)
            print(msg)
        except Exception as e:
            msg = 'Failed create folder:{}, exception:{}'.format(folder, e)
            print(msg)


def move_file(src, desc):
    # move_file("1.txt", "1.txt")  # 不报错
    # move_file("1.txt", "2.txt")  # OK
    # move_file("1.txt", "aa/2.txt")  # 需要先创建不存在的目录
    # move_file("1.txt", "aa/2.txt")  # 目标文件存在则覆盖
    src = os.path.abspath(src)
    desc = os.path.abspath(desc)
    try:
        create_folder(os.path.dirname(desc))
        shutil.move(src, desc)
    except Exception as e:
        print(f"移动文件报错, src:{src}, desc:{desc}, {e}")


def main():
    suffix = ['.csv', '.flow']
    suffix_files = []
    name = 'temp'
    _, all_files = traverse_folder('.', True)
    for file in all_files:
        s = str(os.path.splitext(file)[-1]).lower()
        if s in suffix:
            suffix_files.append(file)
    for suffix_file in suffix_files:
        ok = re.search(r"abcd.*1234", os.path.basename(suffix_file))
        if ok:
            desc = os.path.join(os.path.split(suffix_file)[0], name, os.path.split(suffix_file)[1])
            move_file(suffix_file, desc)
            print(f"move -->  {os.path.basename(suffix_file)}")


if __name__ == '__main__':
    main()
