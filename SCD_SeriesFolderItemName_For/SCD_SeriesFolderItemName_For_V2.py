import os.path
from typing import List

import xlrd
import xlwt
from xlrd import Book
from xlrd.sheet import Sheet
from xlutils.copy import copy


def read_xls(filename: str, sheet_name: str) -> List[list]:
    filename = os.path.abspath(filename)
    assert os.path.isfile(filename), f'{filename} is not file'
    wb: Book = xlrd.open_workbook(filename)
    sheet_names = wb.sheet_names()
    assert sheet_name in sheet_names, 'sheet name error'
    sheet: Sheet = wb.sheet_by_name(sheet_name)
    all_data = []
    for row_x in range(sheet.nrows):
        row = []
        for col_x in range(sheet.ncols):
            row.append(sheet.cell(row_x, col_x).value)
        all_data.append(row)
    print("all data".center(50, '*'))
    for one in all_data:
        print(one)
    return all_data


def deal_with_all_data(all_data: List[list]):
    prefix = None
    for row in all_data:
        a_value = row[0]
        if 'Folder' in a_value:
            e_value = row[4]
            prefix = e_value
        else:
            if prefix:
                e = row[4]
                e_after = f'{prefix}-{e}'
                row[4] = e_after
    print("after data".center(50, '*'))
    for one in all_data:
        print(one)
    return all_data


def write_xls(filename: str, sheet_name: str, data: List[list]):
    filename = os.path.abspath(filename)
    assert os.path.isfile(filename), f'{filename} is not file'
    wb: Book = xlrd.open_workbook(filename)
    sheet_names = wb.sheet_names()
    assert sheet_name in sheet_names, 'sheet name error'
    wb2: xlwt.Workbook = copy(wb)
    sheet: xlwt.Worksheet = wb2.get_sheet(sheet_name)
    for row_x, row in enumerate(data):
        for clo_x, clo in enumerate(row):
            sheet.write(row_x, clo_x, clo)
    wb2.save(filename)


def main():
    filename = "SCD_SeriesFolderItemName_ForV1_Before.xls"
    sheet_name = "Sheet1"
    all_data = read_xls(filename, sheet_name)
    all_data = deal_with_all_data(all_data)
    write_xls(filename, sheet_name, all_data)


if __name__ == '__main__':
    main()
