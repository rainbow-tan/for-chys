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


def main():
    pass
    all_dirs, _ = traverse_folder(".", True)
    find_path_str = "site"
    site_paths = []
    for site_path in all_dirs:
        if find_path_str in site_path:
            site_paths.append(site_path)
    print(f"找到的{find_path_str}文件夹如下:")
    for index, site_path in enumerate(site_paths):
        print(f"第{index + 1}个 --> {os.path.basename(site_path)}, 绝对路径:{site_path}")
    print("=" * 20)
    index = 1
    names = []
    for site_path in site_paths:
        _, all_files = traverse_folder(site_path, False)
        flow = ""
        for file in all_files:
            if file.lower().endswith('.flow'):
                flow = os.path.basename(file)
                print(
                    f"{os.path.basename(site_path)}找到flow文件:{flow}, {find_path_str}绝对路径:{site_path}, flow的绝对路径:{file}")
                break
        if not flow:
            print(f"{os.path.basename(site_path)}未找到flow文件")
        n = 100
        m = 100
        a = index
        index += 1
        b = "ABC"
        c = os.path.basename(site_path)
        d = "XYZ"
        e = flow.replace(".flow", "")[:n]
        f = flow.replace(".flow", "")[-m:]

        father_start = 3  # 父亲文件夹基本名称从前截取father_start个
        father_end = 4  # 父亲文件夹基本名称从后截取father_end个
        father_basename = os.path.basename(os.path.dirname(site_path))  # 父亲文件夹基础名称
        g = father_basename[:father_start]  # 父亲文件夹基本名称从前截取father_start个
        h = father_basename[-father_end:]  # 父亲文件夹基本名称从后截取father_end个
        name = f"{a}-{b}-{c}-{d}-{e}-{f}-{g}-{h}"
        print(f"{os.path.basename(site_path)} 新的名称为 '{name}'")
        names.append(name)
    for i, site_path in enumerate(site_paths):
        new_name = site_path.replace(os.path.basename(site_path), names[i])
        os.rename(site_path, new_name)


if __name__ == '__main__':
    main()
