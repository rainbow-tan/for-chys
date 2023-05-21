import os.path
import shutil
from threading import Thread


def traverse_folder(path: str, n: int = 999):
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


def create_folder(folder):
    folder = os.path.abspath(folder)
    if not os.path.exists(folder):
        try:
            os.makedirs(folder)
        except FileExistsError as e:
            pass
        except Exception as e:
            msg = 'Failed create folder:{}, exception:{}'.format(folder, e)
            print(msg)


def copy_file(src, dst):
    # 目标文件存在,直接覆盖
    # 目标是文件夹,则在文件夹中生成同名文件
    create_folder(os.path.dirname(dst))
    try:
        shutil.copy2(src, dst)
        # msg = 'Success copy file:{} to :{}'.format(os.path.abspath(src), os.path.abspath(dst))
        # print(msg)
    except Exception as e:
        msg = 'Fail copy file:{} to :{}, exception:{}'.format(os.path.abspath(src), os.path.abspath(dst), e)
        print(msg)


def read_txt():
    filename = "CopyList.txt"
    with open(filename) as f:
        lines = f.readlines()
    lines = list(filter(lambda x: x.strip(), lines))
    lines = list(map(lambda x: x.strip(), lines))
    # print(f"lines:{lines}")
    data = dict()
    for i in range(0, len(lines), 2):
        if i % 2 == 0:
            data[os.path.abspath(lines[i])] = os.path.abspath(lines[i + 1])
    # print(f"data:{data}")
    return data


def copy_my_file(src, dest):
    src = os.path.abspath(src)
    dest = os.path.abspath(dest)
    _, files = traverse_folder(src)
    need_copy_files = []
    for file in files:
        if file.lower().endswith('.csv'):
            continue
        if 'profile' in file:
            continue
        need_copy_files.append(file)
    for f in need_copy_files:
        new_name = f.replace(src, dest)
        copy_file(f, new_name)
    print(f"{os.path.basename(src)}完成拷贝{len(need_copy_files)}个文件")


def main():
    data = read_txt()
    for k, v in data.items():
        t = Thread(target=copy_my_file, args=(k, v))
        t.start()
        t.join()
    print(f"end deal {len(data)} 个文件夹")


if __name__ == '__main__':
    main()
