import os
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


def copy_file(src, dst):
    # 目标文件存在,直接覆盖
    # 目标是文件夹,则在文件夹中生成同名文件
    create_folder(os.path.dirname(dst))
    try:
        shutil.copy2(src, dst)
        msg = 'Success copy file:{} to :{}'.format(os.path.abspath(src), os.path.abspath(dst))
        print(msg)
    except Exception as e:
        msg = 'Fail copy file:{} to :{}, exception:{}'.format(os.path.abspath(src), os.path.abspath(dst), e)
        print(msg)


DATA = []


def traverse_by_number(path, index, n):
    global DATA
    if index > n:
        return
    info = os.listdir(path)
    for i in info:
        d = os.path.abspath(os.path.join(path, i))
        if os.path.isdir(d):
            traverse_by_number(d, index + 1, n)
        else:
            ccc = d
            DATA.append((index, ccc))


def do(dirname):
    files = filter(lambda x: x[0] != 1, DATA)
    files = map(lambda x: x[1], files)
    for file in files:
        if not os.path.splitext(file)[1] in XXX:
            continue
        f = file.replace(dirname, "")
        c = f.split(os.sep)
        d = "--".join(c)
        new_name = os.path.join(dirname, d)
        if len(c) > 1:
            pass
            copy_file(file, new_name)


XXX = ['.flow', '.dat', '.txt']


def main3(number):
    current_path = os.path.abspath(os.path.dirname(__file__))
    traverse_by_number(current_path, 1, int(number))
    DATA.sort(key=lambda x: x[0])
    for i in DATA:
        print(i)
    do(current_path + os.sep)


def main2():
    dirname = os.path.abspath(os.path.dirname(__file__))
    dirname += os.sep
    print(f"dirname:{dirname}")
    all_dirs, all_files = traverse_folder(".")
    files = []
    for file in all_files:
        if ".idea" not in file and file != os.path.abspath(__file__):
            if os.path.splitext(file)[1] in XXX:
                files.append(file)
    for file in files:
        f = file.replace(dirname, "")
        print(f"f:{f}")
        c = f.split(os.sep)
        print(f"c:{c}")
        d = "--".join(c)
        print(f"d:{d}")
        new_name = os.path.join(dirname, d)
        print(f'new name:{new_name}')
        if len(c) > 1:
            print(f"需要移动:{file}")
            pass
            # copy_file(file, new_name)


if __name__ == '__main__':
    main2()
#     show = """input 0 ---> all
# input other ---> number of plies
# """
#     input_str = input(show)
#     if input_str == "0":
#         main2()
#     else:
#         main3(input_str)
