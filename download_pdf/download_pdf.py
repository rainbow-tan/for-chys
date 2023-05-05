import datetime
import json
import os.path
import shutil
import time

from selenium import webdriver


def download_pdf():
    path = r"D:\下载"
    url = 'http://edc.micron.com/mti/SEG001/APPENG/B58R_NAND_Design_Datasheet.pdf'
    url = 'https://onepetro.org/books/book/chapter-pdf/2796210/dedication.pdf'
    #############################################################
    path = os.path.abspath(path)
    if not os.path.isdir(path):
        os.makedirs(path)
        # print(f"create dir:{path}")

    name = url.split("/")[-1]
    filename = os.path.join(path, name)
    if os.path.isfile(filename):
        os.remove(filename)
        # print(f"delete file:{filename}")

    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_experimental_option('prefs', {
        "download.default_directory": path,  # Change default directory for downloads
        "download.prompt_for_download": False,  # To auto download the file
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True  # It will not show PDF directly in chrome
    })
    web = webdriver.Chrome(options=options)
    web.get(url)
    time.sleep(5)  # TODO 等待下载的时间

    # print(f"save to:{filename}")
    return filename


def is_update(old: list, save_name: str, size: int):
    now = datetime.datetime.now().strftime("%Y_%m_%d")
    print(f"today is {now}")
    for one in old:
        if one['size'] == size:
            print("not update~~~~")
            return
    print(f"updated!!!, newest {save_name}")


def create_folder(folder):
    folder = os.path.abspath(folder)
    if not os.path.exists(folder):
        try:
            os.makedirs(folder)
            msg = 'Success create folder:{}'.format(folder)
            # print(msg)
        except Exception as e:
            msg = 'Failed create folder:{}, exception:{}'.format(folder, e)
            print(msg)


def copy_file(src, dst):
    # 目标文件存在,直接覆盖
    # 目标是文件夹,则在文件夹中生成同名文件
    create_folder(os.path.dirname(dst))
    try:
        shutil.copy2(src, dst)
        msg = 'Success copy file:{} to :{}'.format(os.path.abspath(src), os.path.abspath(dst))
        # print(msg)
    except Exception as e:
        msg = 'Fail copy file:{} to :{}, exception:{}'.format(os.path.abspath(src), os.path.abspath(dst), e)
        print(msg)


def delete_file(file):
    file = os.path.abspath(file)
    if os.path.isfile(file):
        try:
            os.remove(file)
            msg = 'Success delete file:{}'.format(file)
            # print(msg)
        except Exception as e:
            msg = 'Failed delete file:{}, exception:{}'.format(file, e)
            print(msg)


def compare(filename: str):
    now = datetime.datetime.now().strftime("%Y_%m_%d")
    version_file = "ExistingVersion.txt"
    info = {'time': now, 'filename': filename, 'size': os.path.getsize(filename)}
    if not os.path.isfile(version_file):
        with open(version_file, 'w') as f:
            json.dump([info], f, indent=4)
        # print(f'first save info to {version_file}')
    else:
        # print(f'open exist file:{version_file}')
        with open(version_file, 'r') as f:
            old: list = json.load(f)
            # print(f"old info:{old}")
        is_update(old, filename, os.path.getsize(filename))
        new = old.copy()
        new.append(info)
        with open(version_file, 'w') as f:
            json.dump(new, f, indent=4)
    # dir_name = os.path.dirname(filename)
    name, suffix = os.path.splitext(filename)
    new_name = name + '_' + now + suffix
    # print(f"new name:{new_name}")
    copy_file(filename, new_name)
    delete_file(filename)


def main():
    filename = download_pdf()
    compare(filename)


if __name__ == '__main__':
    main()
