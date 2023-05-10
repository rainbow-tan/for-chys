# -*- encoding=utf-8 -*-
import os

def load_config(filename: str):
    filename = os.path.abspath(filename)
    if os.path.isfile(filename):
        with open(filename) as f:
            lines = f.readlines()
    data = []
    for line in lines:
        line_strip = line.strip()
        if not line_strip:
            continue
        split = line_strip.split()
        assert len(split) == 2
        src = split[0].strip()
        desc = split[1].strip()
        data.append((src, desc))
    print(f"split info:{data}")
    return data
def main():
    load_config()

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
