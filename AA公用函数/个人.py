import datetime
import json
import logging
import logging.handlers
import os
import shutil

def traverse_folder(path: str, n: int = 9999):
    path = os.path.abspath(path)
    assert os.path.isdir(path)
    assert n > 0
    all_files = []
    all_dirs = []
    for root, dirs, files in os.walk(path):
        for one_file in files:
            all_files.append(os.path.join(root, one_file))  # 所有文件
        for one_dir in dirs:
            all_dirs.append(os.path.join(root, one_dir))  # 所有文件夹

    path_split = path.split(os.sep)
    len_path_split = len(path_split)

    need_dir = []
    for d_name in all_dirs:
        dir_split = d_name.split(os.sep)
        dir_split_ = dir_split[len_path_split:]
        if len(dir_split_) <= n:
            need_dir.append(d_name)

    need_files = []
    for f_name in all_files:
        f_name_split = f_name.split(os.sep)
        f_name_split_ = f_name_split[len_path_split:]
        if len(f_name_split_) <= n:
            need_files.append(f_name)

    return need_dir, need_files
# -*- encoding=utf-8 -*-



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


def delete_folder(folder):
    folder = os.path.abspath(folder)
    if os.path.isdir(folder):
        try:
            shutil.rmtree(folder)
            msg = 'Success delete folder:{}'.format(folder)
            print(msg)
        except Exception as e:
            msg = 'Failed delete folder:{}, exception:{}'.format(folder, e)
            print(msg)


def delete_file(file):
    file = os.path.abspath(file)
    if os.path.isfile(file):
        try:
            os.remove(file)
            msg = 'Success delete file:{}'.format(file)
            print(msg)
        except Exception as e:
            msg = 'Failed delete file:{}, exception:{}'.format(file, e)
            print(msg)


def copy_file(src, dst):
    # 目标文件存在,直接覆盖
    # 目标是文件夹,则在文件夹中生成同名文件
    create_folder(os.path.dirname(dst))
    try:
        shutil.copy2(src, dst)
        msg = 'Success copy file:{} to :{}'.format(os.path.abspath(src), os.path.abspath(dst))
        print(msg)
    except Exception as e:
        msg = 'Fail copy file:{} to :{}, exception:{}'.format(os.path.abspath(src), os.path.abspath(dst), e)
        print(msg)


def copy_folder(src, dst, delete=True):
    """
    :param src:
    :param dst:
    :param delete: 目标文件夹存在时,是否删除
    :return:
    """
    src = os.path.abspath(src)
    dst = os.path.abspath(dst)
    if delete:
        delete_folder(dst)
    try:
        shutil.copytree(src, dst)
        msg = 'Success copy folder:{} to path:{}'.format(src, dst)
        print(msg)
    except Exception as e:
        msg = 'Fail copy folder:{} to path:{}, exception:{}'.format(src, dst, e)
        print(msg)


def read_file(file, mode='r', line_type=False, encoding=None):
    file = os.path.abspath(file)
    if line_type:
        content = []
    else:
        content = ''
    if os.path.isfile(file):
        with open(file, mode, encoding=encoding) as f:
            if line_type:
                content = f.readlines()
            else:
                content = f.read()
    return content


def write_file(file, info, mode='w', encoding=None, indent=4):
    create_folder(os.path.dirname(file))
    with open(file, mode, encoding=encoding) as f:
        if isinstance(info, str):
            f.write(info)
        elif isinstance(info, list):
            info = map(lambda x: str(x), info)
            f.writelines(info)
        elif isinstance(info, dict):
            info = json.dumps(info, indent=indent, ensure_ascii=False)
            f.write(info)
        else:
            msg = 'The type I don\'t know'
            print(msg)


def load_json_by_file(file, default=None):
    if default is None:
        default = dict()
    data = default
    file = os.path.abspath(file)
    if os.path.isfile(file):
        with open(file, 'r') as f:
            try:
                data = json.load(f)
                msg = 'Success load json file:{}'.format(file)
                print(msg)
            except Exception as e:
                msg = 'Failed load json file:{}  exception:{}'.format(file, e)
                print(msg)
    else:
        msg = 'Can not find file:{} for load json'.format(file)
        print(msg)
    return data


def load_json_by_string(string, default=None):
    if default is None:
        default = dict()
    data = default
    try:
        data = json.loads(string)
        msg = 'Success load json string:{}'.format(string)
        print(msg)
    except Exception as e:
        msg = 'Failed load json string:{},  exception:{}'.format(string, e)
        print(msg)
    return data


def now(fmt='%Y%m%d%H%M%S'):
    string = datetime.datetime.now().strftime(fmt)
    return string


def string_to_date(string, fmt='%Y-%m-%d %H:%M:%S'):
    # 2021-01-28 10:51:26
    date = datetime.datetime.strptime(string, fmt)
    return date


def date_to_string(date, fmt='%Y-%m-%d %H:%M:%S'):
    # 2021-01-28 10:51:26
    string = date.strftime(fmt)
    return string





def init_logger(log_name='logs/log.log',
                logger_string='ROOT',
                max_bytes=1024 * 1024 * 1,
                backup_count=10,
                mode='a',
                fmt_string='[%(asctime)s][%(name)s][%(levelname)s]%(message)s',
                record_level=logging.INFO,
                console_level=logging.WARN,
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


log = init_logger()
if __name__ == '__main__':
    log.info('!!!!')
    log.info('!!!!1')
    log.info('!!!!2')
    log.info('!!!!3')