import datetime
import os.path
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


def do(obj):
    print(f"start-->{obj}")
    download_dir = os.path.abspath(".")
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument('window-size=200,200')
    options.add_argument('window-position=0,1000')
    prefs = {'profile.default_content_settings.popups': 0,
             'download.default_directory': download_dir}
    options.add_experimental_option('prefs', prefs)
    #options.add_argument('--headless')  # headless browser. Note: if browser is hidden, no download action.
    web = webdriver.Chrome(options=options)
    web.minimize_window()
    url = f'https://siwcharwizprod1.sing.micron.com/#/ViewSummaryTable?char_summary_id={obj}'
    # url = f'https://www.1ppt.com/moban/shangwu/ppt_shangwu_{obj}.html'
    # print(url)
    web.get(url)
    time.sleep(30)  # wait for screen to refresh finish
    try:
        element = web.find_element(By.XPATH, '//*[@id="page-wrap"]/div/div/div[1]/div[3]/div/div[4]/div/button')
        element.click()
    except:
        print("cannot find element, weblink changed? or time not enough?")
    #time.sleep(30) #30sec
    path = r"."  # download path
    path = os.path.abspath(path)
    now = datetime.datetime.now()
    sleep = datetime.timedelta(hours=0, minutes=30) # max wait time for 1 file download
    time.sleep(10)  # wait for a temp file to disappear
    while True:
        # print('into check')
        _, files = traverse_folder(path, True)
        exist = False
        for file in files:
            if ".csv.crdownload" in os.path.basename(file):
                print(f"not completed find in-completed download files'{file}'")
                exist = True
                break

        if exist:
            print('sleep in')
            time.sleep(10)  # check crdownload file every 10 secs if download complete.
            print('sleep end')
            ret = datetime.datetime.now() - now
            if ret > sleep:
                break
        else:
            # print('completed!!!')
            break
    web.quit()
    print(f"END-->{obj}")


def read_txt():
    with open('AddressList_NewNameList.txt') as f:
        lines = f.readlines()
    lines = list(filter(lambda x: str(x).strip(), lines))
    lines = list(map(lambda x: str(x).strip(), lines))
    return lines


def main():
    lines = read_txt()
    for i, line in enumerate(lines):
        # do(i+1)
        do(line)
    print(f"END, We need to have:{len(lines)} files downloaded, verify please.")
    # do()


if __name__ == '__main__':
    main()
