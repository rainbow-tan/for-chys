import os
import re
import shutil


def traverse_folder(path: str, n: int = 99):
    path = os.path.abspath(path)
    assert os.path.isdir(path)
    assert n > 0
    all_files = []
    all_dirs = []
    for root, dirs, files in os.walk(path):
        for one_file in files:
            all_files.append(os.path.join(root, one_file))  # 所有文件
        for one_dir in dirs:
            all_dirs.append(os.path.join(root, one_dir))  # 所有文件夹

    path_split = path.split(os.sep)
    len_path_split = len(path_split)

    need_dir = []
    for d_name in all_dirs:
        dir_split = d_name.split(os.sep)
        dir_split_ = dir_split[len_path_split:]
        if len(dir_split_) <= n:
            need_dir.append(d_name)

    need_files = []
    for f_name in all_files:
        f_name_split = f_name.split(os.sep)
        f_name_split_ = f_name_split[len_path_split:]
        if len(f_name_split_) <= n:
            need_files.append(f_name)

    return need_dir, need_files


def input_n():
    print("直接回车表示遍历所有文件夹")
    print("输入整数N表示遍历前N层文件夹")
    n = input("请输入:")
    if not n.strip():
        n = 99
        print("将会遍历所有文件夹")
    else:
        n = int(n)
        print(f"将会遍历前{n}层文件夹")
    return n


def _choose_by_re(path: str):
    patterns = ['.*AA', '.*C', '.*BB']
    basename = os.path.basename(path)
    for pattern in patterns:
        ret = re.search(pattern, basename)
        if ret:
            return True


def choose_by_re(paths):
    need_paths = []
    for path in paths:
        if _choose_by_re(path):
            need_paths.append(path)
    print("=========符合条件的文件夹如下=========")
    for path in need_paths:
        print(path)
    return need_paths


def create_folder(folder):
    folder = os.path.abspath(folder)
    if not os.path.exists(folder):
        try:
            os.makedirs(folder)
        except Exception as e:
            msg = 'Failed create folder:{}, exception:{}'.format(folder, e)
            print(msg)


def delete_folder(folder):
    folder = os.path.abspath(folder)
    if os.path.isdir(folder):
        try:
            shutil.rmtree(folder)
        except Exception as e:
            msg = 'Failed delete folder:{}, exception:{}'.format(folder, e)
            print(msg)


def copy_folder(src, dst, delete=True):
    """
    :param src:
    :param dst:
    :param delete: 目标文件夹存在时,是否删除
    :return:
    """
    src = os.path.abspath(src)
    dst = os.path.abspath(dst)
    if delete:
        delete_folder(dst)
    try:
        shutil.copytree(src, dst)
    except Exception as e:
        msg = 'Fail copy folder:{} to path:{}, exception:{}'.format(src, dst, e)
        print(msg)


def deal_folder(path: str):
    current_path = os.path.abspath(".")
    path1 = current_path.split(os.sep)
    path2 = path.split(os.sep)
    path3 = path2[len(path1):]
    if len(path3) > 1:
        name = "--".join(path3)
        new_name = os.path.join(current_path, name)
        copy_folder(path, new_name, True)


def main():
    n = input_n()
    folders, _ = traverse_folder(".", n)
    need_paths = choose_by_re(folders)

    for need_path in need_paths:
        deal_folder(need_path)

    for need_path in need_paths:
        delete_folder(need_path)  # 是否删除源文件夹
        pass


if __name__ == '__main__':
    main()
