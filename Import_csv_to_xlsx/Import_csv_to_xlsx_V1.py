import openpyxl
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

XLSX_NAME = "XLSX_File_Before_RunCode.xlsx"
def main():
    wb: Workbook = openpyxl.load_workbook(XLSX_NAME)
    print(type(wb))
    sheet_names = wb.sheetnames
    print(f"sheet names:{sheet_names}")
    sheet: Worksheet = wb["1-111"]
    print(type(sheet))
    sheet.cell(1, 1, "AAA")
    wb.save("tmp.xlsx")


if __name__ == '__main__':
    main()
