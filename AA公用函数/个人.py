import os
import pprint


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
    c = traverse_by_number(r"D:\GitCode\for-chys\1", 1)
    pprint.pprint(c)

    _, files = traverse_folder(r"D:\GitCode\for-chys\1", True)
    pprint.pprint(files)
