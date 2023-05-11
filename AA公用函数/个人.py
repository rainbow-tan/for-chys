import os


def traverse_folder(folder, only_first=False):
    folder = os.path.abspath(folder)
    all_files = []
    all_dirs = []
    if os.path.isdir(folder):
        for root, dirs, files in os.walk(folder):
            for one_file in files:
                all_files.append(os.path.join(root, one_file))  # 所有文件
            for one_dir in dirs:
                all_dirs.append(os.path.join(root, one_dir))  # 所有文件夹
            if only_first:
                break
    else:
        msg = 'Can not find folder:{} for traverse'.format(folder)
        print(msg)
    return all_dirs, all_files


def traverse_folder2(folder: str, n: int = 99):
    assert n > 0
    folder = os.path.abspath(folder)
    assert os.path.isdir(folder)
    all_files = []
    all_dirs = []
    for root, dirs, files in os.walk(folder):
        for one_file in files:
            all_files.append(os.path.join(root, one_file))  # 所有文件
        for one_dir in dirs:
            all_dirs.append(os.path.join(root, one_dir))  # 所有文件夹

    length = len(folder.split(os.sep))
    need_dir = []
    for dir_path in all_dirs:
        dir_path_split = dir_path.split(os.sep)
        dir_path_need = dir_path_split[length:]
        if len(dir_path_need) <= n:
            need_dir.append(dir_path)
    need_file = []
    for dir_file in all_files:
        dir_file_split = dir_file.split(os.sep)
        dir_file_need = dir_file_split[length:]
        if len(dir_file_need) <= n:
            need_file.append(dir_file)
    return need_dir, need_file


def traverse_by_number(path: str, n: int = 99, index: int = 1, data=None):
    if data is None:
        data = []
    if index > n:
        return
    info = os.listdir(path)
    for i in info:
        d = os.path.abspath(os.path.join(path, i))
        if os.path.isdir(d):
            traverse_by_number(d, n, index + 1, data)
        else:
            ccc = d
            data.append((index, ccc))
    data.sort(key=lambda x: x[0])
    """
    [(1, 'D:\\GitCode\\for-chys\\1\\新建文本文档 - 副本 (2).txt'),
     (1, 'D:\\GitCode\\for-chys\\1\\新建文本文档 - 副本.txt'),
     (1, 'D:\\GitCode\\for-chys\\1\\新建文本文档.txt'),
     (2, 'D:\\GitCode\\for-chys\\1\\2 - 副本 (2)\\新建文本文档 - 副本.txt'),
     (2, 'D:\\GitCode\\for-chys\\1\\2 - 副本 (2)\\新建文本文档.txt'),
     (2, 'D:\\GitCode\\for-chys\\1\\2 - 副本 (4)\\新建文本文档.txt'),
     (2, 'D:\\GitCode\\for-chys\\1\\2 - 副本 (5)\\新建文本文档.txt'),
     (3, 'D:\\GitCode\\for-chys\\1\\2 - 副本\\3\\新建文本文档.txt'),
     (3, 'D:\\GitCode\\for-chys\\1\\2 - 副本 (2)\\3\\新建文本文档.txt'),
     (4, 'D:\\GitCode\\for-chys\\1\\2 - 副本\\3\\4\\新建文本文档.txt')]
    """
    data = list(map(lambda x: x[1], data))
    """
    ['D:\\GitCode\\for-chys\\1\\新建文本文档 - 副本 (2).txt',
     'D:\\GitCode\\for-chys\\1\\新建文本文档 - 副本.txt',
     'D:\\GitCode\\for-chys\\1\\新建文本文档.txt',
     'D:\\GitCode\\for-chys\\1\\2 - 副本 (2)\\新建文本文档 - 副本.txt',
     'D:\\GitCode\\for-chys\\1\\2 - 副本 (2)\\新建文本文档.txt',
     'D:\\GitCode\\for-chys\\1\\2 - 副本 (4)\\新建文本文档.txt',
     'D:\\GitCode\\for-chys\\1\\2 - 副本 (5)\\新建文本文档.txt',
     'D:\\GitCode\\for-chys\\1\\2 - 副本\\3\\新建文本文档.txt',
     'D:\\GitCode\\for-chys\\1\\2 - 副本 (2)\\3\\新建文本文档.txt',
     'D:\\GitCode\\for-chys\\1\\2 - 副本\\3\\4\\新建文本文档.txt']
    """
    return data


if __name__ == '__main__':
    # c = traverse_by_number(r"D:\GitCode\for-chys\1", 1)
    # pprint.pprint(c)
    #
    # _, files = traverse_folder(r"D:\GitCode\for-chys\1", True)
    # pprint.pprint(files)

    a, b = traverse_folder2(r"D:\GitCode\for-chys\AA公用函数", 1)
    for i in b:
        print(i)
        # os.remove(i)
    # for i in range(1,5):
    #     with open(f'1-{i}.txt','w') as f:
    #         pass
