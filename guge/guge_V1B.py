import time

from selenium import webdriver
from selenium.webdriver.common.by import By


def do(obj):
    print(f"开始执行-->{obj}")
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument('--headless')  # 无头浏览器
    web = webdriver.Chrome(options=options)

    url = f'https://siwcharwizprodl.sing.micron.com/#/ViewSummaryTable?char_summary_id={obj}'
    # url = f'https://www.1ppt.com/moban/shangwu/ppt_shangwu_{obj}.html'
    web.get(url)
    time.sleep(1)
    try:
        element = web.find_element(By.XPATH, '//*[@id="page-wrap"]/div/div/div[1]/div[3]/div/div[4]/div/button')
        element.click()
    except:
        print("未找到元素, 是网页变了 还是 时间不够")
    time.sleep(1)

    web.quit()
    print(f"结束执行-->{obj}")


def read_txt():
    with open('requment.txt') as f:
        lines = f.readlines()
    lines = list(filter(lambda x: str(x).strip(), lines))
    lines = list(map(lambda x: str(x).strip(), lines))
    return lines


def main():
    lines = read_txt()
    for i, line in enumerate(lines):
        # do(i+1)
        do(line)
    print(f"结束, 应该有:{len(lines)}个文件被下载了, 请检查是否正确")
    # do()


if __name__ == '__main__':
    main()
