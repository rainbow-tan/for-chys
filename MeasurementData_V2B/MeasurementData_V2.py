import csv
import time

from pynput.keyboard import Key, Controller

need = []
with open('MeasurementData.csv') as f:
    reader = csv.reader(f)
    for i in reader:
        need.append(i[4])  # E
        need.append(i[5])  # F
print(need)

keyboard = Controller()
start_time = 5
print(f"after {start_time} second begin")
time.sleep(start_time)

line = 0
while line < len(need):
    keyboard.type(str(need[line]))  # 输入
    line += 1

    time.sleep(1)  # 等待几秒再操作
    right = Key.right  # 向右
    keyboard.press(right)
    keyboard.release(right)

    time.sleep(1)  # 等待几秒再操作
    keyboard.type(str(need[line]))  # 输入
    length = len(str(need[line]))
    n = 2  # 多移动几位
    length += n
    print(f"左移{length}位")
    line += 1

    time.sleep(1)  # 等待几秒再操作

    for i in range(length):
        left = Key.left  # 向左
        keyboard.press(left)
        keyboard.release(left)

    time.sleep(1)  # 等待几秒再操作
    down = Key.down  # 向下
    keyboard.press(down)
    keyboard.release(down)

    time.sleep(1)  # 等待几秒再操作

print("exit...")
