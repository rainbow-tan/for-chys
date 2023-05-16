import datetime
import os.path
import shutil
import time

from selenium import webdriver
from selenium.webdriver.common.by import By


def traverse_folder(folder, only_first=False):
    folder = os.path.abspath(folder)
    all_files = []
    all_dirs = []
    if os.path.isdir(folder):
        for root, dirs, files in os.walk(folder):
            for one_file in files:
                all_files.append(os.path.join(root, one_file))  # 
            for one_dir in dirs:
                all_dirs.append(os.path.join(root, one_dir))  # 
            if only_first:
                break
    else:
        msg = 'Can not find folder:{} for traverse'.format(folder)
        print(msg)
    return all_dirs, all_files


def do(line):
    print(f"start-->{line}")
    download_dir = os.path.abspath(".")
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument('window-size=200,200')
    options.add_argument('window-position=0,1000')
    prefs = {'profile.default_content_settings.popups': 0,
             'download.default_directory': download_dir}
    options.add_experimental_option('prefs', prefs)
    # options.add_argument('--headless')  # headless browser. Note: if browser is hidden, no download action.
    web = webdriver.Chrome(options=options)
    web.minimize_window()
    url = f'https://siwcharwizprod1.sing.micron.com/#/ViewSummaryTable?char_summary_id={line}'
    print(f'url:{url}')
    web.get(url)
    sleep_time = 30
    print(f"wait {sleep_time} second for screen to refresh finish")
    time.sleep(sleep_time)  # wait for screen to refresh finish
    try:
        element = web.find_element(By.XPATH, '//*[@id="page-wrap"]/div/div/div[1]/div[3]/div/div[4]/div/button')
        element.click()
        print("click button end")
    except:
        print("cannot find element, weblink changed? or time not enough?")
    # time.sleep(30) #30sec
    download_dir = os.path.abspath(download_dir)
    now = datetime.datetime.now()
    sleep = datetime.timedelta(hours=0, minutes=30)  # 最多等多长时间, 还未出现csv则认为失败
    time.sleep(10)  # wait for a temp file to disappear
    while True:
        print("检查是否还存在.csv.crdownload文件")
        _, files = traverse_folder(download_dir, True)
        exist = False
        for file in files:
            if ".csv.crdownload" in os.path.basename(file):
                print(f"not completed find in-completed download files'{file}'")
                print("依旧存在.csv.crdownload文件")
                exist = True
                break

        if exist:
            t = 10
            print(f"继续等待{t}秒")
            time.sleep(t)  # check crdownload file every 10 secs if download complete.

            ret = datetime.datetime.now() - now
            if ret > sleep:
                raise Exception(f"系统出现问题, 等了{sleep}也没出现下载成功的csv文件")
        else:
            # print('completed!!!')
            print("未存在.csv.crdownload文件, 认为下载完成")
            break
    web.quit()
    print(f"END-->{line}")


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


def copy_file(src, dst):
    # 目标文件存在,直接覆盖
    # 目标是文件夹,则在文件夹中生成同名文件
    # create_folder(os.path.dirname(dst))
    try:
        shutil.copy2(src, dst)
        # msg = 'Success copy file:{} to :{}'.format(os.path.abspath(src), os.path.abspath(dst))
        # print(msg)
    except Exception as e:
        msg = 'Fail copy file:{} to :{}, exception:{}'.format(os.path.abspath(src), os.path.abspath(dst), e)
        print(msg)


def rename_file(lines):
    info = []
    print("rename file begin")
    download_dir = os.path.abspath(".")
    for i in range(len(lines)):

        if i == 0:
            name = 'spreadsheet.csv'
        else:
            name = f'spreadsheet ({i}).csv'

        print(f"src:{name}")
        src_sbs = os.path.join(download_dir, name)
        if os.path.isfile(src_sbs):
            a, b = os.path.splitext(name)
            new_name = "{}{}{}{}".format(a, "-", lines[i][0], b)
            info.append(new_name)
            copy_file(src_sbs, new_name)

        else:
            raise Exception(f"不存在文件, 可能没下载下来:{src_sbs}")

    with open("SpreadsheetList.txt", "w") as f:
        f.writelines(info)

    print("rename file end")


def main():
    lines = load_config("AddressList_NewNameList.txt")
    for line, _ in lines:
        # do(i+1)
        do(line)
    print(f"END, We need to have:{len(lines)} files downloaded, verify please.")
    rename_file(lines)


if __name__ == '__main__':
    main()
