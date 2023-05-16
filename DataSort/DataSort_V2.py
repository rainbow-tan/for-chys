import ast
import csv
import os.path
from concurrent.futures import ThreadPoolExecutor
from typing import List

import openpyxl
import pandas as pd
from openpyxl.cell import Cell
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from pandas import DataFrame


def traverse_folder(path: str, n: int = 99):
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


def read_xlsm(filename: str) -> List[list]:
    wb: Workbook = openpyxl.load_workbook(filename)
    ws: Worksheet = wb.active
    data = []
    for column in ws:
        row = []
        for cell in column:
            cell: Cell = cell
            row.append(cell.value)
        print(f"row:{row}")
        data.append(row)
    return data


def read_csv(filename: str) -> List[list]:
    data = []
    with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
    print(f'csv data:{data}')
    return data


def get_xlsm_data(xlsx_path: str) -> List[list]:
    return read_xlsm(xlsx_path)


def xlsm_data_to_dict(xlsm_data: List[list]) -> dict:
    print("=" * 50)
    row0 = xlsm_data[0]
    data = {}
    for i in range(0, len(row0)):
        data[row0[i]] = [xlsm_data[j][i] for j in range(1, len(xlsm_data))]

    for k, v in data.items():
        print(f"{k}  --->   {v}")

    for k, v in data.items():
        vv = set(v)
        vv.remove(None)
        data[k] = list(vv)

    new_request = dict()
    for k, v in data.items():
        if v:
            new_request[k] = v
    data = new_request
    print("=" * 50)
    for k, v in data.items():
        print(f"{k}  --->   {v}")
    return data


def save_src(value: str):
    try:
        ret = ast.literal_eval(value)
    except:
        return value
    if type(ret) == int:
        return int(value)
    elif type(ret) == float:
        return float(value)
    else:
        return value


def sava_src_int_float(data: List[list]):
    rows = []
    for row in data:
        row_new = list(map(lambda x: save_src(x), row))
        rows.append(row_new)
    print(f"rows:{rows}")
    return rows


def find_cut_index(xlsm_data_dict: dict, csv_data: List[list]):
    rows0 = csv_data[0]
    cut_index = []
    for k, v in xlsm_data_dict.items():
        assert k in rows0, f'未找到key:{k}, 请检查xlsm文件'
        find = rows0.index(k)
        print(f"find:{find} kry:{k}")
        for i, csv_value in enumerate(csv_data):
            if i == 0:
                continue
            # print(csv_value)
            # print(csv_value[find])
            find_csv = csv_value[find]
            if find_csv in v:
                print(f"第{i}行符合条件{v}, 需要切掉")
                cut_index.append(i)
    print(f'cut_index:{cut_index}')
    cut_index = list(set(cut_index))
    cut_index.sort()
    print(f'cut_index:{cut_index}')
    return cut_index


class INFO:
    def __init__(self, csv_filename: str, cut_count: int):
        self.csv_filename = csv_filename
        self.cut_count = cut_count

    def __str__(self):
        return f"{self.csv_filename}--->{self.cut_count}"

    def __repr__(self):
        return self.__str__()


def save_cut_line(cut_index: list, csv_data: List[list], csv_filename: str):
    cut_data = [csv_data[0]]
    for i in cut_index:
        cut_data.append(csv_data[i])
    print(f'cut data:{cut_data}')

    csv_filename = os.path.abspath(csv_filename)
    name, suffix = os.path.splitext(csv_filename)
    new_name = f'{name}-New{suffix}'
    with open(new_name, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerows(cut_data)

    info = INFO(csv_filename, len(cut_index))
    print(f'info:{info}')
    return info


def save_not_cut_line(cut_index: list, csv_data: List[list], csv_filename: str):
    rows = []
    for i, row in enumerate(csv_data):
        if i not in cut_index:
            rows.append(row)
    with open(csv_filename, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerows(rows)


def cut(cut_index: list, csv_data: List[list], csv_filename: str):
    info = save_cut_line(cut_index, csv_data, csv_filename)
    save_not_cut_line(cut_index, csv_data, csv_filename)
    return info


def aaa(a, k, xlsm_data_dict: dict):
    print(f'k:{k}')
    print(f'a:{a}')
    print(f'a:{type(a)}')
    v = xlsm_data_dict[k]
    print(f'v:{v}')
    print("----")
    for i in v:
        for j in a:
            print(f"j:{j}")

            if str(i) in str(j):
                print("aaaa!")
                # return True
        print(i in a)
    return False


def _deal_one_file(xlsm_data_dict: dict, csv_filename: str):
    # df:DataFrame=pd.read_csv(csv_filename,usecols=xlsm_data_dict.keys())
    df: DataFrame = pd.read_csv(csv_filename)
    print(f"df:{df}")
    # for k  in xlsm_data_dict:
    #     print("ss")
    #     c=df[ aaa( df[k],k,xlsm_data_dict),:]
    #     print(f'c:{c}')
    print("*" * 50)
    dfs = []
    for k in xlsm_data_dict:
        for v in xlsm_data_dict[k]:
            print(f"选{k}列包含字符串{v}的")
            df2 = df[df[k].str.contains(str(v))]
            print(f'df2:{df2}')
            print("*" * 10)
            dfs.append(df2)
    print(f'dfs:{dfs}')
    df3 = pd.concat(dfs)
    print(f'df3:{df3}')
    df4: DataFrame = df3.drop_duplicates()
    print(f'df4:{df4}')
    df4.to_csv("切下来的行.csv", index=False)


def deal_one_file(xlsm_data_dict: dict, csv_filename: str):
    try:
        info = _deal_one_file(xlsm_data_dict, csv_filename)
    except Exception as e:
        info = f"{csv_filename} 操作失败, e:{e}"
    return info


def find_all_csv():
    _, files = traverse_folder(".")
    csv_files = list(filter(lambda x: str(x).lower().endswith('.csv'), files))
    print(f'csv_files:{csv_files}')
    return csv_files


def deal_many_files(csv_files: List[str], xlsm_data_dict: dict):
    max_workers = len(csv_files) if len(csv_files) <= 20 else 20
    executor = ThreadPoolExecutor(max_workers)
    results = []
    for result in executor.map(deal_one_file, [xlsm_data_dict] * len(csv_files), csv_files):
        results.append(result)
    print("=" * 50)
    print("=" * 50)
    print("=" * 50)
    fail = list(filter(lambda x: type(x) == str, results))
    if fail:
        print(f"某些文件失败了, 详情:{fail}")
        raise Exception()
    print("{:<60}{}".format("filename", "cut count"))
    for info in results:
        print("{:<60}{}".format(info.csv_filename, info.cut_count))


def main():
    xlsm_data = get_xlsm_data("DataSort_V1.xlsm")
    xlsm_data_dict = xlsm_data_to_dict(xlsm_data)

    csv_files = find_all_csv()
    # deal_many_files(csv_files, xlsm_data_dict)

    deal_one_file(xlsm_data_dict, 'CSV.csv')


if __name__ == '__main__':
    main()
