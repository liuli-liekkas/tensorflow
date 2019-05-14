import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import time
import math
import serial
import tkinter
import threading


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.set_xlabel('经度')
ax.set_ylabel('纬度')
ax.set_title('运动轨迹')
line = ax.plot([0, 0], [10000, 10000], '-g', marker='.')[0]
plt.grid(True)
plt.ion()

matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['axes.unicode_minus'] = False

data_lng_theory_value = []
data_lat_theory_value = []
# data_lng_actual_value = []
# data_lat_actual_value = []
ser_theory_value = serial.Serial('COM7', 9600, timeout=0.5)
# ser_actual_value = serial.Serial('COM4', 115200, timeout=0.5)
while True:
    try:
        data_theory_value = ser_theory_value.readline().decode(encoding='gb18030')
        # data_actual_value = ser_actual_value.readline().decode(encoding='gb18030')
        if data_theory_value.split(',')[0] == "$GNRMC":
            data_lng_theory_value.append(float(data_theory_value.split(',')[3]))
            data_lat_theory_value.append(float(data_theory_value.split(',')[5]))
        # if data_actual_value.split(',')[0] == "$GNRMC":
        #     data_lng_actual_value.append(data_actual_value.split(',')[3])
        #     data_lat_actual_value.append(data_actual_value.split(',')[5])
        # plt.plot(data_lng_theory_value, data_lat_theory_value, 'r', data_lng_actual_value, data_lat_actual_value, 'b')
        # plt.plot(data_lng_theory_value, data_lat_theory_value, 'r')
        line.set_xdata(data_lng_theory_value)
        line.set_ydata(data_lat_theory_value)
        ax.set_xlim([3115, 3118])
        ax.set_ylim([12110, 12113])
        plt.pause(0.5)
    except:
        continue
