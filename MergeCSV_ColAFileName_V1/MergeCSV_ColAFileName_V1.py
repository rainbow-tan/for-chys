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
    except:
        return s
    return s


def main():
    csvs = list(filter(lambda x: os.path.isfile(x) and str(x).lower().endswith('.csv'), os.listdir('.')))

    all_data = []
    for file in csvs:
        print(file)
        filename_row = ['', file]
        all_data.append(filename_row)
        with open(file) as f:
            data = list(csv.reader(f))
            for one in data:
                # print(one)
                new_one = [file.split('.')[0]] + one
                # print(new_one)
                all_data.append(new_one)

    new_data = []
    for row in all_data:
        new_row = list(map(lambda x: change_str_to_number(x), row))
        new_data.append(new_row)

    new_data.insert(0, new_data[1])  # todo 是否拷贝row3到row1
    # print(new_data)

    book = openpyxl.Workbook()  # 创建空白工作薄
    sheet = book.active  # 获取当前默认工作表
    sheet.name = '工作表'  # 修改工作表名称

    for row in new_data:
        sheet.append(row)
    book.save("Merge.xlsx")


if __name__ == '__main__':
    main()
    print("结束")
