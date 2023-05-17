import datetime
import time


def main():
    pass


if __name__ == '__main__':
    for i in range(5):
        filename = f'filename{i}.txt'
        print(filename)
        with open(filename,'w')as f:
            pass
