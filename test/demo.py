from pynput.keyboard import Controller

if __name__ == '__main__':
    # import linecache
    # filename = "文件名"
    # count = linecache.getline(filename, 50435)
    # print(count)
    #
    # count = linecache.getline(filename, 50436)
    # print(count)
    #
    # count = linecache.getline(filename, 50437)
    # print(count)

    keyboard = Controller()
    keyboard.type('a\na')
