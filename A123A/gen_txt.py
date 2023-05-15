import os.path
from typing import List

# ----------------------------配置区----------------------------
BAT_NAME = r"a.bat"
INDEX = 3  # 第几个元素表示名称
TXT_NAME = r"AddressList_NewNameList.txt"


# --------------------------------------------------------------
def get_names():
    with open(BAT_NAME) as f:
        content = f.read()
    info = content.split("&&")
    ret = []

    for one in info:
        if 'python' not in one:
            continue
        if os.path.basename(__file__) in one:
            continue
        data = one.split()
        print(f'data:{data}')
        assert len(data) > INDEX
        ret.append(data[INDEX].strip())
    print(f'ret:{ret}')
    return ret


def write(names: List[str]):
    txt_name = os.path.abspath(TXT_NAME)
    if not os.path.isdir(os.path.dirname(txt_name)):
        os.makedirs(os.path.dirname(txt_name))
    info = list(map(lambda x: f'xxxx\t{x}\n', names))
    with open(txt_name, 'w') as f:
        f.writelines(info)
    print(f"save to {txt_name}")


def main():
    names = get_names()
    write(names)
    print(f"write line count:{len(names)}")


if __name__ == '__main__':
    main()
