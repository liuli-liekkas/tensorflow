import serial
from time import sleep

serial = serial.Serial('COM6', 115200, timeout=0.1)
if serial.isOpen():
    print("open success")
else:
    print("open failed")
n = 0
time = 0
while True:
    line = serial.readline()
    # if line != b'':
    time = time + 0.5
    n = n+1
    print("receive : ", n, time, line)