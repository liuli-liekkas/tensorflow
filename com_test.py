# coding=utf-8
import serial
import time
import math
import numpy as np
import tkinter
from tkinter import scrolledtext
from tkinter import ttk
import matplotlib as mpl
import matplotlib.pyplot as plt
from threading import Thread
import _tkinter


class Application:
    def __init__(self):
        # self.serial = serial.Serial('COM5', 115200, timeout=0.1)
        self.window = tkinter.Tk()
        self.set_window(self.window)
        self.reset_port()
        self.scrolled_window()
        self.test_window()
        # self.test_main()

        self.window.mainloop()

    @staticmethod
    def set_window(window):
        window.title("导航测试系统")
        window.geometry('1200x800')

    def reset_port(self):
        global e1
        global e2
        global b1
        global b2
        monty = ttk.LabelFrame(self.window, text=" 指令窗口 ")
        monty.grid(column=0, row=0, padx=10, pady=10, sticky='W')
        s1 = tkinter.Label(monty, text='指令1：')
        s1.grid(row=0, column=0, sticky='W')
        e1 = tkinter.Entry(monty, show=None)
        e1.grid(row=0, column=1, sticky='E')
        b1 = tkinter.Button(monty, text='发送', command=self.send_port1)
        b1.grid(row=0, column=2, sticky='E')
        s2 = tkinter.Label(monty, text='指令2:')
        s2.grid(row=1, column=0, sticky='W')
        e2 = tkinter.Entry(monty, show=None)
        e2.grid(row=1, column=1, sticky='E')
        b2 = tkinter.Button(monty, text='发送', command=self.send_port2)
        b2.grid(row=1, column=2, sticky='E')

        # hot_set = '$reset,1,2'
        # col_set = '$reset,1,0'
    def send_port1(self):
        message1 = e1.get()
        self.serial.write(message1.encode('utf-8') + '\n')

    def send_port2(self):
        message2 = e2.get()
        self.serial.write(message2.encode('utf-8') + '\n')

    def scrolled_window(self):
        global scr_show
        scrolled_W = 80
        scrolled_H = 20
        monty = ttk.LabelFrame(self.window, text=" 报文数据 ")
        monty.grid(row=1, column=0, padx=10, pady=10)
        scr_show = tkinter.scrolledtext.ScrolledText(monty, width=scrolled_W, height=scrolled_H, wrap=tkinter.WORD)
        scr_show.grid(column=0, columnspan=3)

    def test_window(self):
        global scr_test
        scrolled_W = 80
        scrolled_H = 10
        monty = ttk.LabelFrame(self.window, text=" 测试结果 ")
        monty.grid(row=2, column=0, padx=10, pady=10)
        scr_test = tkinter.scrolledtext.ScrolledText(monty, width=scrolled_W, height=scrolled_H, wrap=tkinter.WORD)
        scr_test.grid(column=0, columnspan=3)

    def get_data(self):
        line = self.serial.readline()
        line = line.decode('utf-8')
        scr_show.insert('end', line)
        scr_show.update()
        scr_show.see('end')
        return line

    def paint(self, x_data, y_data, x_label, y_label, title, name):
        plt.figure()
        plt.xlabel(x_label, size=14)
        plt.ylabel(y_label, size=14)
        plt.title(title, size=14)
        plt.plot(x_data, y_data, linewidth=2, c='b')
        plt.grid(True)
        plt.axis('tight')
        plt.show()
        plt.savefig(name + '.jpg')

    # 三点计算公式
    def geo_distance_three(self, lng_test, lat_test, h_test, lng_default, lat_default, h_default):
        lng_test, lat_test, lng_default, lat_default = map(math.radians, [lng_test, lat_test, lng_default, lat_default])
        delta_x = h_test * math.cos(lat_test) * math.cos(lng_test) - h_test * math.cos(lat_default) * math.cos(
            lng_default)
        delta_y = h_test * math.cos(lat_test) * math.sin(lng_test) - h_test * math.cos(lat_default) * math.sin(
            lng_default)
        delta_z = h_test - h_default
        dis = math.sqrt(delta_x + delta_y + delta_z)
        return dis

    # 经典两点计算公式
    def geo_distance_two(self, lat_test, lng_test, lat_default, lng_default):
        lat1, lng1, lat2, lng2 = map(math.radians, [lat_test, lng_test, lat_default, lng_default])  # 角度转弧度
        d_lat = lat2 - lat1
        d_lng = lng2 - lng1
        a = math.sin(d_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lng / 2) ** 2
        dis = 2 * math.asin(math.sqrt(a)) * 6371 * 1000
        return dis

    def test_main(self):
        utc_time = False
        location = False
        data_test = []
        time_start = 0
        while True:
            time.sleep(0.01)
            line = self.get_data()
            if line:
                if line.split(',')[0] == e1.get():
                    scr_test.insert('end', '已发送指令1:' + e1.get())
                    scr_test.update()
                    scr_test.see('end')
                    continue
                elif line.split(',')[0] == e2.get():
                    scr_test.insert('end', '已发送指令2:' + e2.get())
                    scr_test.update()
                    scr_test.see('end')
                    continue
                elif line.split(',')[0] == '$ACKOK':
                    scr_test.insert('end', "系统已经重启完毕，开始计时……")
                    scr_test.update()
                    scr_test.see('end')
                    time_start = time.time()
                    continue
                elif line.split(',')[0] == '$GNRMC':
                    if not utc_time and line.split(',')[1] and not(line.split(',')[3]):
                        scr_test.insert('end', "系统已经成功获得UTC时间，还没开始定位……")
                        scr_test.update()
                        scr_test.see('end')
                        utc_time = True
                    if line.split(',')[3]:
                        if not location:
                            time_delta = time.time() - time_start
                            time_delta = str(time_delta)
                            scr_test.insert('end, '"系统开始定位,首次捕获时间为：" + time_delta)  # 计算捕获时间
                            scr_test.update()
                            scr_test.see('end')
                            location = True
                        data_test.append(self.get_data().split(',')[3])  # 提取纬度信息
                        data_test.append(self.get_data().split(',')[5])  # 提取精度信息
                        data_test.append(self.get_data().split(',')[7])  # 提取速度信息
                elif line.split(',')[0] == '$GNGGA':
                    if line.split(',')[3]:
                        data_test.append(line.split(',')[9])  # 提取高度信息
                        if len(data_test) == 40:
                            data_test = np.array(list(map(float, data_test))).reshape(10, 4)  # 转换成矩阵
                            data_test = data_test.sum(axis=0) / 10  # 矩阵每列求和
                            scr_test.insert('end', data_test)
                            scr_test.update()
                            scr_test.see('end')
                            lat_default = 30
                            lng_default = 100
                            geo_distance = self.geo_distance_two(data_test[0], data_test[1], lat_default, lng_default)
                            if geo_distance > 100 or data_test[3] > 100:
                                np.delete(data_test, 0, axis=1)
                                geo_distance = str(geo_distance)
                                scr_test.insert('end', "定位无效，水平误差为：" + geo_distance + '米'
                                                + '\n' + '定位无效，垂直误差为：' + geo_distance + '米')
                                scr_test.update()
                                scr_test.see('end')
                            elif geo_distance < 100 and data_test[3] < 100:
                                geo_distance = str(geo_distance)
                                scr_test.insert('end', '定位有效，水平误差为：' + geo_distance + '米'
                                                + '\n' + '定位无效，垂直误差为：' + geo_distance + '米')
                                scr_test.update()
                                scr_test.see('end')
                                break


# def get_data(self):
    #     utc_time = False
    #     location = False
    #     data_test = []
    #     while True:
    #         line = serial.readline()
    #         line = line.decode('utf-8')
    #         if line:
    #             if line.split(',')[0] == '$reset':
    #                 print('已发送指令：', self.hot_set)
    #                 continue
    #             if line.split(',')[0] == '$ACKOK':
    #                 print("系统已经重启完毕，开始计时……")
    #                 time_start = time.time()
    #                 continue
    #             if line.split(',')[0] == '$GNRMC':
    #                 if not utc_time and line.split(',')[1] and not(line.split(',')[3]):
    #                     print("系统已经成功获得UTC时间，还没开始定位……")
    #                     utc_time = True
    #                 if line.split(',')[3]:
    #                     if not location:
    #                         time_delta = time.time() - time_start
    #                         print("系统开始定位,首次捕获时间为：", time_delta)  # 计算捕获时间
    #                         location = True
    #                     data_test.append(line.split(',')[3])  # 提取纬度信息
    #                     data_test.append(line.split(',')[5])  # 提取精度信息
    #                     data_test.append(line.split(',')[7])  # 提取速度信息
    #             if line.split(',')[0] == '$GNGGA':
    #                 if line.split(',')[3]:
    #                     data_test.append(line.split(',')[9])  # 提取高度信息
    #                     if len(data_test) == 40:
    #                         data_test = np.array(list(map(float, data_test))).reshape(10, 4)  # 转换成矩阵
    #                         print(data_test.sum(axis=0) / 10)  # 矩阵每列求和
    #                         break

    # 三点计算公式
    # def geo_distance(self, lng_test, lat_test, h_test, lng_default, lat_default, h_default):
    #     lng_test, lat_test, lng_default, lat_default = map(math.radians, [lng_test, lat_test, lng_default, lat_default])
    #     delta_x = h_test * math.cos(lat_test) * math.cos(lng_test) - h_test * math.cos(lat_default) * math.cos(
    #         lng_default)
    #     delta_y = h_test * math.cos(lat_test) * math.sin(lng_test) - h_test * math.cos(lat_default) * math.sin(
    #         lng_default)
    #     delta_z = h_test - h_default
    #     dis = math.sqrt(delta_x + delta_y + delta_z)
    #     return dis

    # 经典两点计算公式
    # def geo_distance(lng_test, lat_test, lng_default, lat_default):
    #     lng1, lat1, lng2, lat2 = map(math.radians, [lng_test, lat_test, lng_default, lat_default])  # 角度转弧度
    #     d_lng = lng2 - lng1
    #     d_lat = lat2 - lat1
    #     a = math.sin(d_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lng / 2) ** 2
    #     dis = 2 * math.asin(math.sqrt(a)) * 6371 * 1000
    #     print(dis)

    # def insert_point(self):
    #     var = self.entry.get()
    #     self.text.insert('insert', var)
    #
    # def insert_end(self):
    #     var = self.entry.get()
    #     self.text.insert(2.2, var)
    #
    # def print_selection(self):
    #     value = self.lb.get(self.lb.curselection())
    #     print(value)
    #     serial.write((value + '\n').encode())
    #     self.var1.set(value)
    #     return value

        # if serial.isOpen():
        #     print("串口打开成功，开始接收数据……")
        #     # self.entry = tkinter.Entry(window, show=None)
        #     # self.entry.pack()
        #     var1 = tkinter.StringVar()
        #     l = tkinter.Label(self.window, width=30, textvariable=var1)
        #     l.pack()
        #     b1 = tkinter.Button(window,  text='发送指令', width=15, height=2, command=print_selection)
        #     b1.pack()
        #
        #     # self.text = tkinter.Text(window, height=10)
        #     # self.text.pack()
        #     # # button1 = tkinter.Button(window, text='insert point', width=15, height=2, command=self.insert_point)
        #     # button1.pack()
        #     # button2 = tkinter.Button(window, text='insert end', command=self.insert_end)
        #     # button2.pack()
        #     var2 = tkinter.StringVar()
        #     var2.set((self.hot_set, self.col_set))
        #     lb = tkinter.Listbox(window, listvariable=var2)
        #     lb.pack()
        # else:
        #     print("串口打开失败")


# serial = serial.Serial('COM5', 115200, timeout=0.1)
# hot_set = '$reset,1,2'
# col_set = '$reset,1,0'
# utc_time = False
# location = False
# data_test = []
# if serial.isOpen():
#     print("串口打开成功，开始接收数据……")
#     while True:
#         line = serial.readline()
#         line = line.decode('utf-8')
#         if line:
#             if line.split(',')[0] == '$reset':
#                 print('已发送指令：', hot_set)
#                 continue
#             if line.split(',')[0] == '$ACKOK':
#                 print("系统已经重启完毕，开始计时……")
#                 time_start = time.time()
#                 continue
#             if line.split(',')[0] == '$GNRMC':
#                 if not utc_time and line.split(',')[1] and not(line.split(',')[3]):
#                     print("系统已经成功获得UTC时间，还没开始定位……")
#                     utc_time = True
#                 if line.split(',')[3]:
#                     if not location:
#                         time_delta = time.time() - time_start
#                         print("系统开始定位,首次捕获时间为：", time_delta)  # 计算捕获时间
#                         location = True
#                     data_test.append(line.split(',')[3])  # 提取纬度信息
#                     data_test.append(line.split(',')[5])  # 提取精度信息
#                     data_test.append(line.split(',')[7])  # 提取速度信息
#             if line.split(',')[0] == '$GNGGA':
#                 if line.split(',')[3]:
#                     data_test.append(line.split(',')[9])  # 提取高度信息
#                     if len(data_test) == 40:
#                         data_test = np.array(list(map(float, data_test))).reshape(10, 4)  # 转换成矩阵
#                         print(data_test.sum(axis=0) / 10)  # 矩阵每列求和
#                         break
# else:
#     print("串口打开失败")


if __name__ == '__main__':
    app = Application()
