import os.path
import re
from concurrent.futures import ThreadPoolExecutor

from typing import List

STR = "PATTEN.*"  # TODO 修改这些地方


def split_content(filename: str):
    filename = os.path.abspath(filename)
    with open(filename, 'r') as f:
        lines = f.readlines()

    all_index = []
    for index, line in enumerate(lines):
        # if STR in line:
        if re.search(STR,line):
            all_index.append(index)
    # print(f"all index:{all_index}")
    split_lines = []
    for i in range(len(all_index) - 1):
        start = all_index[i]
        end = all_index[i + 1]
        # print(f'(start,end):{(start, end)}')
        split_lines.append(lines[start:end])

    start = all_index[-1]
    end = len(lines)
    # print(f'(start,end):{(start, end)}')
    split_lines.append(lines[start:end])
    # print(f"split lines:{split_lines}")
    # for i in split_lines:
    #     print(i)
    return split_lines


def gen_filename(filename: str, split_line: str):
    basename = os.path.basename(os.path.abspath(filename))
    basename_without_suffix = os.path.splitext(basename)[0]
    left = 3  # TODO 修改这些地方
    left_name = basename_without_suffix[:left]
    # print(f"left name:{left_name}")

    right = 3  # TODO 修改这些地方
    right_name = basename_without_suffix[-right:]
    # print(f"right name:{right_name}")

    constant = "AAA"  # TODO 修改这些地方

    print(f"before split line:{split_line}")
    strings = [";", ",", "\t", "!", " ", "-"]  # TODO 修改这些地方
    for s in strings:
        split_line = split_line.replace(s, "").strip()
    print(f"after split line:{split_line}")

    new_name = "{}{}{}{}".format(left_name, right_name, constant, split_line)  # TODO 修改这些地方
    # print(f'new_name:{new_name}')
    new_name = os.path.join(os.path.dirname(os.path.abspath(filename)), f"{new_name}{os.path.splitext(basename)[-1]}")
    print(f'new_name:{new_name}')
    return new_name


def write_file(filename: str, split_lines: List[list]):
    # print("----------")
    for lines in split_lines:
        # print(f"lines:{lines}")
        new_name = gen_filename(filename, lines[0])
        with open(new_name, 'w') as f:
            f.writelines(lines)


def traverse_folder(path: str, n: int = 9999):
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


def do(filename: str):
    # filename = "abcdef.txt"
    split_lines = split_content(filename)
    write_file(filename, split_lines)


def main():
    _, files = traverse_folder(".", 1)
    suffix = ".txt"  # TODO 修改这些地方
    need_files = list(filter(lambda x: str(x).lower().endswith(suffix), files))

    max_workers = len(need_files) if len(need_files) <= 20 else 20
    executor = ThreadPoolExecutor(max_workers)
    results = []
    for result in executor.map(do, need_files):
        results.append(result)
    print("=" * 50)
    print(f"处理的文件个数是:{len(need_files)}个")


if __name__ == '__main__':
    main()
