import datetime
import json
import logging
import os.path
import shutil
import time
import logging.handlers
from selenium import webdriver
def create_folder(folder):
    folder = os.path.abspath(folder)
    if not os.path.exists(folder):
        try:
            os.makedirs(folder)
            msg = 'Success create folder:{}'.format(folder)
            print(msg)
        except Exception as e:
            msg = 'Failed create folder:{}, exception:{}'.format(folder, e)
            print(msg)

def init_logger(log_name='logs/log.log',
                logger_string='ROOT',
                max_bytes=1024 * 1024 * 1,
                backup_count=10,
                mode='a',
                fmt_string='[%(asctime)s][%(name)s][%(levelname)s]%(message)s',
                record_level=logging.INFO,
                console_level=logging.INFO,
                file_level=logging.INFO):
    """
    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10
    NOTSET = 0
    :param fmt_string:
    :param logger_string:
    :param mode:
    :param log_name:
    :param max_bytes:
    :param backup_count:
    :param record_level:
    :param console_level:
    :param file_level:
    :return:
    """
    create_folder(os.path.dirname(log_name))
    fmt = logging.Formatter(fmt_string)  # 设置日志格式
    logger = logging.getLogger(logger_string)
    logger.setLevel(record_level)

    stream_handler = logging.StreamHandler()  # 控制台日志句柄,设置则可以打印到控制台
    stream_handler.setLevel(console_level)  # 设置打印到控制台日志等级
    stream_handler.setFormatter(fmt)
    if stream_handler not in logger.handlers:
        logger.addHandler(stream_handler)  # 添加控制台句柄
    # 设置回滚日志句柄
    rollback_handler = logging.handlers.RotatingFileHandler(log_name, mode, max_bytes, backup_count)

    rollback_handler.setLevel(file_level)  # 设置回滚日志记录INFO以及以上信息
    rollback_handler.setFormatter(fmt)
    if rollback_handler not in logger.handlers:
        logger.addHandler(rollback_handler)  # 添加回滚日志句柄
    return logger  # 返回句柄，以便于使用

today = datetime.datetime.now().strftime("%Y-%m-%d")
print(f"today is {today}")
log_name = f"{today}.log"
if os.path.isfile(log_name):
    os.remove(log_name)
    print(f"删除已经存在的日志:{log_name}")
log = init_logger(log_name)
def download_pdf():
    path = r"D:\下载"
    url = 'http://edc.micron.com/mti/SEG001/APPENG/B58R_NAND_Design_Datasheet.pdf'
    url = 'https://onepetro.org/books/book/chapter-pdf/2796210/dedication.pdf'
    #############################################################
    path = os.path.abspath(path)
    if not os.path.isdir(path):
        os.makedirs(path)
        # log.info(f"create dir:{path}")

    name = url.split("/")[-1]
    filename = os.path.join(path, name)
    if os.path.isfile(filename):
        os.remove(filename)
        # log.info(f"delete file:{filename}")

    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument('window-size=200,200')
    options.add_argument('window-position=0,1000')
    options.add_experimental_option('prefs', {
        "download.default_directory": path,  # Change default directory for downloads
        "download.prompt_for_download": False,  # To auto download the file
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True  # It will not show PDF directly in chrome
    })
    web = webdriver.Chrome(options=options)
    web.get(url)
    time.sleep(5)  # TODO 等待下载的时间

    log.info(f"save to:{filename}")
    return filename


def is_update(old: list, save_name: str, size: int):
    now = datetime.datetime.now().strftime("%Y_%m_%d")
    log.info(f"today is {now}")
    for one in old:
        if one['size'] == size:
            log.info("not update~~~~")
            return
    log.info(f"updated!!!, newest {save_name}")


def create_folder(folder):
    folder = os.path.abspath(folder)
    if not os.path.exists(folder):
        try:
            os.makedirs(folder)
            msg = 'Success create folder:{}'.format(folder)
            # log.info(msg)
        except Exception as e:
            msg = 'Failed create folder:{}, exception:{}'.format(folder, e)
            log.info(msg)


def copy_file(src, dst):
    # 目标文件存在,直接覆盖
    # 目标是文件夹,则在文件夹中生成同名文件
    create_folder(os.path.dirname(dst))
    try:
        shutil.copy2(src, dst)
        msg = 'Success copy file:{} to :{}'.format(os.path.abspath(src), os.path.abspath(dst))
        # log.info(msg)
    except Exception as e:
        msg = 'Fail copy file:{} to :{}, exception:{}'.format(os.path.abspath(src), os.path.abspath(dst), e)
        log.info(msg)


def delete_file(file):
    file = os.path.abspath(file)
    if os.path.isfile(file):
        try:
            os.remove(file)
            msg = 'Success delete file:{}'.format(file)
            # log.info(msg)
        except Exception as e:
            msg = 'Failed delete file:{}, exception:{}'.format(file, e)
            log.info(msg)


def compare(filename: str):
    now = datetime.datetime.now().strftime("%Y_%m_%d")
    version_file = "ExistingVersion.txt"
    info = {'time': now, 'filename': filename, 'size': os.path.getsize(filename)}
    log.info(f"info:{info}")
    if not os.path.isfile(version_file):
        with open(version_file, 'w') as f:
            json.dump([info], f, indent=4)
        log.info(f'first save info to {version_file}')
    else:
        log.info(f'open exist file:{version_file}')
        with open(version_file, 'r') as f:
            old: list = json.load(f)
            # log.info(f"old info:{old}")
        is_update(old, filename, os.path.getsize(filename))
        new = old.copy()
        new.append(info)
        with open(version_file, 'w') as f:
            json.dump(new, f, indent=4)
    # dir_name = os.path.dirname(filename)
    name, suffix = os.path.splitext(filename)
    new_name = name + '_' + now + suffix
    # log.info(f"new name:{new_name}")
    copy_file(filename, new_name)
    delete_file(filename)


def main():
    filename = download_pdf()
    compare(filename)


if __name__ == '__main__':
    main()
