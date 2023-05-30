# coding=utf-8
# python24执行
import os


def deal_output1():
    filename = 'output1.txt'
    find_str = 'HSRT'
    f = open(filename, 'r')
    # with open(filename) as f:
    lines = f.readlines()
    print(lines)
    for line in lines:
        content = line.strip()
        if find_str in content:
            print(content)
            data = content.split()
            print(data)
            need = data[0]
            return need
    f.close()
    raise Exception("未找到字符串:{}".format(find_str))


def main():
    cmd = 'fid 2418591:19:P06:45:1:12:10-substep-time> output1.txt'
    # cmd = 'dir'
    ret = os.popen(cmd)
    output = ret.read()
    print(output)

    need = deal_output1()
    print(need)

    cmd2 = "frpt %s +charonly -samechar='/1CC1 wx6 8k/' -fgrp=/2418591:19:P06:45:1:12:10/ > output2.txt" % need
    # cmd2 = "dir"
    ret2 = os.popen(cmd2)
    output2 = ret2.read()
    print(output2)
    print("end!!!")


if __name__ == '__main__':
    main()
