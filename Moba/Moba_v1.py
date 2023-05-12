import os


def deal_output1():
    filename = 'output1.txt'
    find_str = 'HSRT'
    with open(filename) as f:
        lines = f.readlines()
    print(f'lines:{lines}')
    for line in lines:
        content = line.strip()
        if find_str in content:
            print(f'find in line:{content}')
            data = content.split()
            print(f'data:{data}')
            need = data[0]
            return need
    raise Exception(f"未找到字符串:{find_str}")


def main():
    cmd = 'fid 2418591:19:P06:45:1:12:10-substep-time> output1.txt'
    cmd = 'dir'
    ret = os.popen(cmd)
    output = ret.read()
    print(f'output:{output}')

    need = deal_output1()
    print(f'need:{need}')

    cmd2 = f"frpt {need} +charonly -samechar='/1CC1 wx6 8k/' -fgrp=/2418591:19:P06:45:1:12:10/ > output2.txt"
    ret2 = os.popen(cmd2)
    output2 = ret2.read()
    print(f'output:{output2}')
    print("end!!!")


if __name__ == '__main__':
    main()
