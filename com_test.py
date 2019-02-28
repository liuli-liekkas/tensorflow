import serial
import time
import math
import numpy as np


def geodistance(lng_test, lat_test, h_test, lng_default, lat_default, h_default):
    lng_test, lat_test, lng_default, lat_default = map(math.radians, [lng_test, lat_test, lng_default, lat_default])
    delta_x = h_test * math.cos(lat_test) * math.cos(lng_test) - h_test * math.cos(lat_default) * math.cos(lng_default)
    delta_y = h_test * math.cos(lat_test) * math.sin(lng_test) - h_test * math.cos(lat_default) * math.sin(lng_default)
    delta_z = h_test - h_default
    dis = math.sqrt(delta_x + delta_y + delta_z)
    return dis


serial = serial.Serial('COM4', 115200, timeout=0.1)
hot_str = '$reset,1,2'
col_set = '$reset,1,0'
utc_time = False
location = False
data_test = []
if serial.isOpen():
    print("串口打开成功，开始接收数据……")
    serial.write((hot_str+'\n').encode())
    while True:
        line = serial.readline()
        line = line.decode('utf-8')
        if line:
            if line.split(',')[0] == '$reset':
                print('已发送指令：', hot_str)
                continue
            if line.split(',')[0] == '$ACKOK':
                print("系统已经重启完毕，开始计时……")
                time_start = time.time()
                continue
            if line.split(',')[0] == '$GNRMC':
                if not utc_time and line.split(',')[1] and not(line.split(',')[3]):
                    print("系统已经成功获得UTC时间，还没开始定位……")
                    utc_time = True
                if line.split(',')[3]:
                    if not location:
                        print("系统开始定位……")
                        location = True
                    data_test.append(line.split(',')[3])  # 提取纬度信息
                    data_test.append(line.split(',')[5])  # 提取精度信息
                    data_test.append(line.split(',')[7])  # 提取速度信息
            if line.split(',')[0] == '$GNGGA':
                if line.split(',')[3]:
                    data_test.append(line.split(',')[9])  # 提取高度信息
                    if len(data_test) == 40:
                        data_test = np.array(list(map(float, data_test))).reshape(10, 4)  # 转换成矩阵
                        print(data_test.sum(axis=0) / 10)  # 矩阵每列求和
                        break
else:
    print("串口打开失败")
