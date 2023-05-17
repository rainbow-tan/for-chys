# ----------------------------配置区----------------------------
import datetime
import os.path
import shutil
from typing import List

BAT_NAME = r"a.bat"
INDEX = 3  # 第几个元素表示名称
TXT_NAME = r"AddressList_NewNameList.txt"
M = 6  # 后面取几位


# --------------------------------------------------------------
def read_txt():
    with open(TXT_NAME) as f:
        # info = f.read()
        lines = f.readlines()
    # content=info.split("\n")
    lines = list(filter(lambda x: x.strip(), lines))
    names = []
    for line in lines:
        names.append(line.strip().split()[-1])
    print(f"names:{names}")
    return names


def read_bat():
    with open(BAT_NAME) as f:
        content = f.read()
        ret = content.split()
    print(f'ret:{ret}')
    return ret


def write(bat_info: List[str]):
    with open(TXT_NAME) as f:
        # info = f.read()
        lines = f.readlines()
    ret = list(map(lambda x: f"{x}\n", bat_info))
    with open(TXT_NAME, 'w') as f:
        f.writelines(lines + ["\n\n"] + ret)
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
def rename(names: list):
    t = datetime.datetime.now().strftime(f"%d%b_%H%M%p")
    print(t)
    name = f"{t}_{os.path.splitext(TXT_NAME)[0]}_{names[0].split('.')[0]}"
    print(f"name:{name}")
    s = ""
    for i in range(1, len(names)):
        n = names[i].split('.')[0]
        print(f"n:{n}")
        m = n[-M:]
        s += m + "_"
    s = s[:-1]
    print(f"s:{s}")
    name = f"{name}_{s}.csv"
    print(f"name:{name}")
    move_file(TXT_NAME,name)


def main():
    bat_info = read_bat()
    names = read_txt()
    write(bat_info)
    rename(names)


if __name__ == '__main__':
    main()
