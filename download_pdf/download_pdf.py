import datetime
import json
import os.path


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
    import requests

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    # response = requests.get('', headers=headers)

    # url 替换为你的链接 TODO
    url = "http://edc.micron.com/mti/SEG001/APPENG/B58R_NAND_Design_Datasheet.pdf"
    response = requests.get(url, headers=headers)
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
