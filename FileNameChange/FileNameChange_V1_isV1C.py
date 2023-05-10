# -*- encoding=utf-8 -*-
import os


def main():
    with open("file_name_change.txt", 'r') as f:
        content = f.readlines()
    new_content = []
    for i in content:
        new_content.append(i.strip())
    for i in new_content:
        d = i.split('\t')
        try:
            os.rename(src=d[0], dst=d[1])
            print(f'success {d[0]} --> {d[1]}')
        except Exception as e:
            print(f"fail, e:{e}")


if __name__ == '__main__':
    main()
