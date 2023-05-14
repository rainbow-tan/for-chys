import os.path
import shutil

import pandas as pd
from pandas import DataFrame


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


def traverse_folders_by_layer(folder, layer=999, index=1, data=None):
    """
    提示: 当前目录是第一层 次级目录是第二次 依次类推
    :param folder: 要遍历的路径
    :param layer: 要遍历多少层
    :param index: 当前是第几层,默认第一层,使用时不需要传递该参数
    :param data: 存放遍历的结果
    :return:
    e.g:
    data = traverse_folders_by_layer(".", 1) 遍历至第1层
    data = traverse_folders_by_layer(".", 2) 遍历至第2层
    data = traverse_folders_by_layer(".", 3) 遍历至第3层
    data = traverse_folders_by_layer(".") 遍历至第999层,也可以理解为遍历当前目录所有子目录
    """
    if data is None:
        data = []
    folder = os.path.abspath(folder)
    if index > layer:
        return data
    info = os.listdir(folder)
    for name in info:
        path = os.path.abspath(os.path.join(folder, name))
        if os.path.isfile(path):
            data.append((index, path))
        else:
            data = traverse_folders_by_layer(path, layer, index + 1, data)
    return data


def find_all_csv():
    csv = []
    data = traverse_folders_by_layer(".", 1)
    for one in data:
        file = one[1]
        basename = os.path.basename(file)
        if basename.lower().endswith(".csv"):
            csv.append(file)
    return csv


################################################################################
def get_delete():
    data: DataFrame = pd.read_excel('RmColDataSort_V1.xlsm')
    delete = []
    for key in data.keys():
        values = data[key]
        val = values[0]
        if val == 'Del':
            delete.append(key)
    print(f'delete:{delete}')
    return delete


def deal_one_file(file, delete):
    file = os.path.abspath(file)
    data: DataFrame = pd.read_csv(file)
    for name in delete:
        del data[name]
    name = file + '.1.csv'
    data.to_csv(name, index=False)
    print(f"file save to {name}")


def main():
    result = find_all_csv()
    for csv in result:
        deal_one_file(csv, delete=get_delete())



if __name__ == '__main__':
    main()
