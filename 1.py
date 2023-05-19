import csv
import os

import openpyxl


def change_str_to_number(s: str):
    try:
        e = eval(s)
        if type(e) == int:
            return int(s)
        if type(e) == float:
            return float(s)
    except Exception as e:
        return s
    return s


def main():
    csvs = list(filter(lambda x: os.path.isfile(x) and str(x).lower().endswith('.csv'), os.listdir('.')))
    print(f'csv:{csvs}')

    all_data = []
    for file in csvs:
        all_data.append([file])  # MergeCsVFilesV1B 功能 注释则无文件名
        with open(file) as f:
            data = list(csv.reader(f))
            for one in data:
                all_data.append(one)
    # print(all_data)

    new_data = []
    for row in all_data:
        new_row = list(map(lambda x: change_str_to_number(x), row))
        new_data.append(new_row)

    new_data.insert(0, new_data[1])  # todo 是否拷贝row3到row1

    book = openpyxl.Workbook()  # 创建空白工作薄
    sheet = book.active  # 获取当前默认工作表
    sheet.name = '工作表'  # 修改工作表名称
    # sheet.cell(1, 1, '数据')  # 几行几列写入数据

    for row in new_data:
        # print(f"row:{row}")
        sheet.append(row)
    book.save("Merge.xlsx ")


if __name__ == '__main__':
    main()
