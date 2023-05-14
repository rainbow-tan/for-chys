from pynput.keyboard import Controller

print(ord('A'))
data=[]
for i in range(65,65+26):
    print(i-65,chr(i))
    data.append(chr(i))
print(data)

keyboard = Controller()
keyboard.type('aaaa')