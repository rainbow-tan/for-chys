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
    _, files = traverse_folder(".", True)
    for f in files:
        if f.endswith('.1.csv'):
            src = f.replace('.1.csv', "")
            delete_file(src)
            shutil.move(f, src)


if __name__ == '__main__':
    main()
