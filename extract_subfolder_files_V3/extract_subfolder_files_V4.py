import os
import re
import shutil


def traverse_by_number(path: str, n: int = 99, index: int = 1, data=None):
    if data is None:
        data = []
    if index > n:
        return
    info = os.listdir(path)
    for i in info:
        d = os.path.abspath(os.path.join(path, i))
        if os.path.isdir(d):
            traverse_by_number(d, n, index + 1, data)
        else:
            ccc = d
            data.append((index, ccc))
    data.sort(key=lambda x: x[0])
    data = list(map(lambda x: x[1], data))
    return data


def create_folder(folder):
    folder = os.path.abspath(folder)
    if not os.path.exists(folder):
        try:
            os.makedirs(folder)
        except Exception as e:
            msg = 'Failed create folder:{}, exception:{}'.format(folder, e)
            print(msg)


def copy_file(src, dst):
    # 目标文件存在,直接覆盖
    # 目标是文件夹,则在文件夹中生成同名文件
    create_folder(os.path.dirname(dst))
    try:
        shutil.copy2(src, dst)
    except Exception as e:
        msg = 'Fail copy file:{} to :{}, exception:{}'.format(os.path.abspath(src), os.path.abspath(dst), e)
        print(msg)


def _choose_by_re(file: str):
    patterns = ['.*.txt', '123.*.txt']
    for pattern in patterns:
        ret = re.search(pattern, file)
        if ret:
            return True


def choose_by_re(files):
    need_file = []
    for file in files:
        if _choose_by_re(file):
            need_file.append(file)
    print("=========符合条件的文件如下=========")
    for file in need_file:
        print(file)

    return need_file


def delete_file(file):
    file = os.path.abspath(file)
    if os.path.isfile(file):
        try:
            os.remove(file)
        except Exception as e:
            msg = 'Failed delete file:{}, exception:{}'.format(file, e)
            print(msg)


def op_files(files):
    dir_name = os.path.abspath(os.path.dirname(__file__))
    dir_name += os.sep
    for file in files:
        f = file.replace(dir_name, "")
        c = f.split(os.sep)
        d = "--".join(c)
        new_name = os.path.join(dir_name, d)
        if len(c) > 1:
            copy_file(file, new_name)
            # delete_file(file)  # todo 删除源文件


def main():
    show = """input 0 ---> all
input other ---> number of plies
please input:"""
    input_str = input(show)
    if input_str == "0":
        n = 99
    else:
        n = int(input_str)
    files = traverse_by_number(".", n)

    need_file = choose_by_re(files)
    op_files(need_file)
    print("结束！！！")


if __name__ == '__main__':
    main()
