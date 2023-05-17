import os
import shutil

MAP = {
    ".ps1": r'powershell',
    ".py": "python",
    ".exe": "",
}


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


def do(run_filename, dir_name, src_path):
    copy_file(run_filename, dir_name)

    os.chdir(dir_name)
    run_filename = os.path.abspath(run_filename)
    dir_name = os.path.abspath(dir_name)
    if str(os.path.splitext(run_filename)[-1]) not in MAP:
        raise Exception(f"不存在对应文件的运行配置MAP, file:{run_filename}, MAP:{MAP}")
    cmd = f"{MAP[str(os.path.splitext(run_filename)[-1])]} {run_filename}".strip()
    ret = os.popen(cmd)
    info = ret.read()
    msg = f"folder:{os.path.basename(dir_name)} cmd:'{cmd}' return info:{info}"
    print(msg)
    f = os.path.join(dir_name, os.path.basename(run_filename))
    delete_file(f)
    os.chdir(src_path)


def main():
    src_path = os.getcwd()
    run_filename = "a.ps1"  # 要拷贝运行的文件, 目前支持这三种
    run_filename = "a.exe"  # 要拷贝运行的文件, 目前支持这三种
    run_filename = "a.py"  # 要拷贝运行的文件, 目前支持这三种
    if not os.path.isfile(run_filename):
        raise Exception(f"{run_filename}不存在")
    all_dirs, _ = traverse_folder('.', True)
    for dir_name in all_dirs:
        do(run_filename, dir_name, src_path)


if __name__ == '__main__':
    main()
    # args = [r"C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe", "-ExecutionPolicy", "Unrestricted", r"D:\Project\PythonProject\沧海一粟\run_subfolder_V1\a.ps1"]
    # p = subprocess.Popen(args, stdout=subprocess.PIPE)
    # dt = p.stdout.read().decode('gbk')
    # print(dt)
