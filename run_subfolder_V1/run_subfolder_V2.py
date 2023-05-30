import os
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from typing import List

MAP = {
    ".ps1": r'powershell',
    ".py": "python",
    ".exe": "",
}


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


def copy_file(src: str, target: str):
    # 如果target是一个已存在的文件, 则覆盖文件内容
    # 如果target是一个已存在的文件夹, 则拷贝src到文件夹中, target文件夹中多一个src文件 如果target中存在同名src文件 则覆盖
    src = os.path.abspath(src)
    target = os.path.abspath(target)
    if os.path.isfile(src):
        try:
            shutil.copy2(src, target)
            # print(f"拷贝文件成功, src:{src}, target:{target}")
        except Exception as e:
            print(f"拷贝文件失败, src:{src}, target:{target}, e:{e}")


def rm_file(filename: str):
    filename = os.path.abspath(filename)
    if os.path.isfile(filename):
        try:
            os.remove(filename)
            # print(f"删除文件成功, filename:{filename}")
        except FileNotFoundError:
            print(f"无需删除不存在的文件, filename:{filename}")
        except Exception as e:
            print(f"删除文件失败, filename:{filename}, e:{e}")


def copy_file_to_sub_folder_run(files: List[str], sub_folder: str):
    sub_folder = os.path.abspath(sub_folder)
    # print(f"sub folder:{sub_folder}")
    new_files = []
    for file in files:
        file = os.path.abspath(file)
        # print(f'file:{file}')
        new_file = os.path.join(sub_folder, os.path.basename(file))
        new_files.append(new_file)
        # print(f"new file:{new_file}")
        assert os.path.isfile(file)
        copy_file(file, new_file)

    run_bat = os.path.join(sub_folder, 'run.bat')
    popen = subprocess.Popen(run_bat, shell=True, cwd=sub_folder, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = popen.stdout.read()
    # print(f"out:{out}")
    err = popen.stderr.read()
    # print(f'err:{err}')

    for filename in new_files:
        rm_file(filename)

    return out, err


def main():
    need_copy_files = ['a.txt', 'b.txt', 'run.bat']
    src_path = os.path.abspath(os.getcwd())
    # print(f"当前的运行路径是:{src_path}")
    dirs, _ = traverse_folder(src_path)
    # print(dirs)
    # copy_file_to_sub_folder(need_copy_dfiles, dirs[0])

    max_workers = 10 if 10 <= len(dirs) else len(dirs)
    executor = ThreadPoolExecutor(max_workers)
    rets = []
    for result in executor.map(copy_file_to_sub_folder_run, [need_copy_files] * len(dirs), dirs):
        rets.append(result)
    print("执行情况如下".center(50, '='))
    for index, dir_name in enumerate(dirs):
        print(f"子目录:{dir_name}")
        print(f"子目录的输出:{rets[index]}")
        print("\n")
    print(f"共处理了{len(dirs)}个子目录".center(50, '-'))


if __name__ == '__main__':
    main()
