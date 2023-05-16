# -*- encoding=utf-8 -*-
import os
import shutil


def load_config(filename: str):
    filename = os.path.abspath(filename)
    if os.path.isfile(filename):
        with open(filename) as f:
            lines = f.readlines()
    data = []
    for line in lines:
        line_strip = line.strip()
        if not line_strip:
            continue
        split = line_strip.split()
        assert len(split) == 2
        src = split[0].strip()
        desc = split[1].strip()
        data.append((src, desc))
    print(f"split info:{data}")
    return data


def copy_file(src, dst):
    # 目标文件存在,直接覆盖
    # 目标是文件夹,则在文件夹中生成同名文件
    # create_folder(os.path.dirname(dst))
    try:
        shutil.copy2(src, dst)
        # msg = 'Success copy file:{} to :{}'.format(os.path.abspath(src), os.path.abspath(dst))
        # print(msg)
    except Exception as e:
        msg = 'Fail copy file:{} to :{}, exception:{}'.format(os.path.abspath(src), os.path.abspath(dst), e)
        print(msg)

def delete_file(file):
    file = os.path.abspath(file)
    if os.path.isfile(file):
        try:
            os.remove(file)
            msg = 'Success delete file:{}'.format(file)
            print(msg)
        except Exception as e:
            msg = 'Failed delete file:{}, exception:{}'.format(file, e)
            print(msg)
def main():
    lines = load_config("AddressList_NewNameList.txt")

    for i in range(len(lines)):

        if i == 0:
            name = f'spreadsheet-{lines[0][0]}.csv'
        else:
            name = f'spreadsheet ({i})-{lines[i][0]}.csv'
        print(f"name:{name}")

        src_sbs = os.path.abspath(name)
        if os.path.isfile(src_sbs):
            a, b = os.path.splitext(lines[i][1])
            new_name = "{}{}{}{}".format(a, "-", lines[i][0], b)
            copy_file(src_sbs, new_name)
            delete_file(src_sbs)  # 删除下载的文件

        else:
            raise Exception(f"不存在文件:{src_sbs}")


if __name__ == '__main__':
    main()
