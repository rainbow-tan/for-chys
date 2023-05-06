import os
from concurrent.futures import ThreadPoolExecutor


def traverse_folder(path, only_first=False):
    path = os.path.abspath(path)
    all_files = []
    all_dirs = []
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for one_file in files:
                all_files.append(os.path.join(root, one_file))  # 所有文件
            for one_dir in dirs:
                all_dirs.append(os.path.join(root, one_dir))  # 所有文件夹
            if only_first:
                break
    else:
        msg = f'{path} is not dir'
        print(msg)
    return all_dirs, all_files


def deal_one_file(filename):
    info = []
    with open(filename) as f:
        lines = f.readlines()
    for line in lines:
        for string in SEARCH_STRING:
            if string in line:
                info.append(dict(filename=filename, key=string, content=line.strip()))
    return info


def show_result(result):
    for one in result:
        print("{:<20}{}".format('file', one['filename']))
        print("{:<20}{}".format('content', one['content']))
        print("\n")


def count_info(result):
    info = dict()
    for key in SEARCH_STRING:
        count = len(list(filter(lambda x: x['key'] == key, result)))
        info[key] = count
    print("===============出现的关键字次数===============")
    print("{:<20}{}".format('KEY', 'COUNT'))
    for k, v in info.items():
        print("{:<20}{}".format(k, v))
    return info


def gen_filename(info: dict):
    filename = "output_"
    for k, v in info.items():
        k = k.replace(":", "").replace("/", "")  # TODO 替换冒号和斜杆的地方
        k = k.strip()
        name = f"{k}{v}"
        filename += name + "_"
    if filename.endswith("_"):
        filename = filename[:-1]
    filename += '.txt'
    filename = os.path.abspath(filename)
    return filename


def write_file(info: dict, result):
    if not info:
        print("not find any keyword")
        return

    filename = gen_filename(info)
    with open(filename, 'w') as f:
        for ret in result:
            f.write(ret['filename'] + "\n")
            f.write(ret['content'] + "\n\n")
    print(f"save to {filename}")


SEARCH_STRING = ['ENDFLOW', ': Fail']


def main():
    _, all_files = traverse_folder('.')
    txt_files = list(filter(lambda x: str(x).lower().endswith('.txt'), all_files))

    default_count = 10
    max_workers = len(txt_files) if len(txt_files) < default_count else default_count

    result = []
    executor = ThreadPoolExecutor(max_workers)
    for ret in executor.map(deal_one_file, txt_files):
        result += ret

    show_result(result)
    info = count_info(result)
    write_file(info, result)


if __name__ == '__main__':
    main()
