# coding=utf-8
import csv
import os


def change_str_to_number(s):
    try:
        e = eval(s)
        if type(e) == int:
            return int(s)
        if type(e) == float:
            return float(s)
    except Exception as e:
        return s
    return s


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


def delete_all_csv(csvs):
    for c in csvs:
        delete_file(c)


def main():
    csvs = list(filter(lambda x: os.path.isfile(x) and str(x).lower().endswith('.csv'), os.listdir('.')))
    print(csv)

    all_data = []
    for index1, file in enumerate(csvs):
        with open(file) as f:
            data = list(csv.reader(f))
            for index2, one in enumerate(data):
                if index1 != 0 and index2 == 0:
                    continue
                all_data.append(one)

    new_data = []
    for row in all_data:
        new_row = list(map(lambda x: change_str_to_number(x), row))
        new_data.append(new_row)

    filename = "aggregated_csv_files_no_bad_data.csv"
    with open(filename, 'w') as f:
        w = csv.writer(f)
        w.writerows(new_data)

    delete_all_csv(csvs)  # 是否删除所有csv

    print("共处理了%d个CSV文件"%len(csvs))


if __name__ == '__main__':
    main()
