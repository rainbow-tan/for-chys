import os.path
import time

from selenium import webdriver
from selenium.webdriver.common.by import By


def read_txt():
    address_list = "AddressList.txt"
    with open(address_list) as f:
        lines = f.readlines()
    lines = list(filter(lambda x: x.strip(), lines))
    lines = list(map(lambda x: x.strip(), lines))
    print(f"lines:{lines}")
    return lines


def main():
    lines = read_txt()
    for line in lines:
        do(line)
    print(f"结束, 访问的网址数量是:{len(lines)}")


def do(index):
    print(f"开始执行-->{index}")
    download_dir = os.path.abspath(".")
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument('window-size=500,500')
    options.add_argument('window-position=500,500')
    prefs = {'profile.default_content_settings.popups': 0,
             'download.default_directory': download_dir}
    options.add_experimental_option('prefs', prefs)
    web = webdriver.Chrome(options=options)
    url = f'https://siwcharwizprodl.sing.micron.com/#/ViewSummaryTable?char_summary_id={index}'
    web.get(url)
    time.sleep(45)
    try:
        element = web.find_element(By.XPATH, '//*[@id="page-wrap"]/div/div/div[1]/div[3]/div/div[4]/div/button')
        element.click()
    except Exception as e:
        print("未找到元素, 是网页变了 还是 时间不够")
    time.sleep(60)

    web.quit()
    print(f"结束执行-->{index}")


if __name__ == '__main__':
    main()
