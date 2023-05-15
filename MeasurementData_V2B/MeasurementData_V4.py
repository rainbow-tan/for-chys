import csv
import time
from typing import List

import openpyxl
from openpyxl.cell import Cell
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from pynput.keyboard import Controller, Key

# ----------------------------配置区----------------------------
START = 'E'  # 插入的首行
END = 'G'  # 插入的尾行
SLEEP_TIME = 5  # 等待多少秒后开始插入
INTERVAL = 0.5  # 模拟按下键盘后,每种操作之间的间隔 即按下右键后输入内容 按下左键与下一个按下左键 太快了系统反应不过来
# --------------------------------------------------------------
alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z']


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


# def get_insert_string() -> List[list]:
#     insert_string = []
#     with open('MeasurementData.csv') as f:
#         reader = csv.reader(f)
#         start = START
#         end = END
#         for data in reader:
#             row = []
#             for j in range(alphabet.index(start), alphabet.index(end) + 1):
#                 row.append(data[j])
#             print(f'row:{row}')
#             insert_string.append(row)
#     print(f'insert_string:{insert_string}')
#     return insert_string


def get_insert_string() -> List[list]:
    data1 = read_xlsm('MeasurementData.xlsx')
    print(f'data:{data1}')
    insert_string = []
    start = START
    end = END
    for data in data1:
        row = []
        for j in range(alphabet.index(start), alphabet.index(end) + 1):
            if data[j]:
                row.append(data[j])
            else:
                row.append('')
        print(f'row:{row}')
        insert_string.append(row)
    print(f'insert_string:{insert_string}')
    return insert_string


def insert(insert_string: List[list]):
    keyboard = Controller()
    for row in insert_string:
        print(f'row:{row}')
        length = sum(list(map(lambda x: len(str(x)), row))) + 1
        for index, data in enumerate(row):
            print(f"data:{data}")
            value = str(data)
            keyboard.type(value)
            if index != len(row) - 1:
                time.sleep(INTERVAL)
                keyboard.tap(Key.right)  # 点击右箭头
                time.sleep(INTERVAL)
        print(f'length:{length}')
        # keyboard.type(value)
        for i in range(length):
            keyboard.tap(Key.left)
            # time.sleep(INTERVAL)

        keyboard.tap(Key.down)
        time.sleep(INTERVAL)


def main():
    insert_string=get_insert_string()
    # insert_string = get_insert_string()
    print(f"等待{SLEEP_TIME}秒后开始插入")
    time.sleep(SLEEP_TIME)
    insert(insert_string)
    print("结束了!!!")


if __name__ == '__main__':
    main()
