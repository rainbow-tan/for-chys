import datetime
import json
import os.path

import requests


def is_update(old: list, save_name: str, size: int):
    for one in old:
        if one['size'] == size:
            print("not update")
            return
    print(f"updated!!!, newest {save_name}")


def compare(now: str, save_name: str, size: int):
    filename = "ExistingVersion.txt"
    info = {'time': now, 'filename': save_name, 'size': size}
    if not os.path.isfile(filename):
        with open(filename, 'w') as f:
            json.dump([info], f, indent=4)
        print(f'first save info to {filename}')
    else:
        print(f'open exist file:{filename}')
        with open(filename, 'r') as f:
            old: list = json.load(f)
            print(f"old info:{old}")
        is_update(old, save_name, size)
        new = old.copy()
        new.append(info)
        with open(filename, 'w') as f:
            json.dump(new, f, indent=4)


def download():
    # url 替换为你的链接 TODO
    url = "https://tse2-mm.cn.bing.net/th/id/OIP-C.taD0yuVYGePBADOU5r_P7gHaMl?w=115&h=196&c=7&r=0&o=5&pid=1.7"
    response = requests.get(url)
    text = response.content
    basename = url.split("/")[-1]
    # basename = "123.png"  # TODO 后续需要注释掉
    basename = os.path.basename(basename)
    name, suffix = os.path.splitext(basename)
    now = datetime.datetime.now().strftime("%Y_%m_%d")
    save_name = name + '_' + now + suffix
    with open(save_name, 'wb') as f:
        f.write(text)
    size = os.path.getsize(save_name)
    print(f"{now.replace('_', '/')} download pdf size:{size}")
    return now, save_name, size


def main():
    now, save_name, size = download()
    compare(now, save_name, size)


if __name__ == '__main__':
    main()
