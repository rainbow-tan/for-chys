import os
import shutil

# ----------------------------
TEMP_FOLDER_NAME = 'temp'


# ----------------------------
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


def read_txt(filename: str):
    with open(filename) as f:
        lines = f.readlines()
    lines = list(filter(lambda x: x.strip(), lines))
    lines = list(map(lambda x: x.strip(), lines))
    return lines


def main():
    lines = read_txt("List.txt")
    for line in lines:
        print(f"line:{line}")

        copy_file(line, os.path.join(TEMP_FOLDER_NAME, line))  # 拷贝
        delete_file(line)  # 删除源文件
        # move_file(line,os.path.join(TEMP_FOLDER_NAME,line))#移动


if __name__ == '__main__':
    main()
