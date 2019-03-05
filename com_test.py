# coding=utf-8
from serial import serialwin32
import time
import math
import numpy as np
import tkinter
from tkinter import scrolledtext
from tkinter import ttk



class Application:
    def __init__(self):
        self.serial = serialwin32.Serial('COM5', 115200, timeout=0.1)
        self.window = tkinter.Tk()
        self.set_window(self.window)
        self.reset_port()
        self.scrolled_window()
        self.test_window()
        self.test_main()

        self.window.mainloop()

    def set_window(self, window):
        window.title("导航测试系统")
        window.geometry('1200x800')

    def reset_port(self):
        global e1
        global e2
        global b1
        global b2
        s1 = tkinter.Label(self.window, text='指令1：')
        s1.grid(row=0, column=0, sticky='W')
        e1 = tkinter.Entry(self.window, show=None)
        e1.grid(row=0, column=1, sticky='E')
        b1 = tkinter.Button(self.window, text='发送', command=self.send_port1)
        b1.grid(row=0, column=2, sticky='E')
        s2 = tkinter.Label(self.window, text='指令2:')
        s2.grid(row=1, column=0, sticky='W')
        e2 = tkinter.Entry(self.window,show=None)
        e2.grid(row=1, column=1, sticky='E')
        b2 = tkinter.Button(self.window, text='发送', command=self.send_port2)
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
        scrolled_H = 40
        scr_show = tkinter.scrolledtext.ScrolledText(self.window, width=scrolled_W, height=scrolled_H, wrap=tkinter.WORD)
        scr_show.grid(column=0, columnspan=100)

    def test_window(self):
        global scr_test
        scrolled_W = 80
        scrolled_H = 10
        scr_test = tkinter.scrolledtext.ScrolledText(self.window, width=scrolled_W, height=scrolled_H, wrap=tkinter.WORD)
        scr_test.grid(column=0, columnspan=500)

    def get_data(self):
        line = self.serial.readline()
        line = line.decode('utf-8')
        scr_show.insert('end', line)
        scr_show.update()
        scr_show.see('end')
        return line

    def test_main(self):
        utc_time = False
        location = False
        data_test = []
        while True:
            time.sleep(0.01)
            if self.get_data():
                if self.get_data().split(',')[0] == e1.get():
                    scr_test.insert('end', '已发送指令1:' + e1.get())
                    scr_test.update()
                    scr_show.see('end')
                    continue
                elif self.get_data().split(',')[0] == e2.get():
                    scr_test.insert('end', '已发送指令2:' + e2.get())
                    scr_test.update()
                    scr_show.see('end')
                    continue
                elif self.get_data().split(',')[0] == '$ACKOK':
                    print("系统已经重启完毕，开始计时……")
                    time_start = time.time()
                    continue
                if self.get_data().split(',')[0] == '$GNRMC':
                    if not utc_time and self.get_data().split(',')[1] and not(self.get_data().split(',')[3]):
                        print("系统已经成功获得UTC时间，还没开始定位……")
                        utc_time = True
                    if self.get_data().split(',')[3]:
                        if not location:
                            time_delta = time.time() - time_start
                            print("系统开始定位,首次捕获时间为：", time_delta)  # 计算捕获时间
                            location = True
                        data_test.append(self.get_data().split(',')[3])  # 提取纬度信息
                        data_test.append(self.get_data().split(',')[5])  # 提取精度信息
                        data_test.append(self.get_data().split(',')[7])  # 提取速度信息
                if self.get_data().split(',')[0] == '$GNGGA':
                    if self.get_data().split(',')[3]:
                        data_test.append(self.get_data().split(',')[9])  # 提取高度信息
                        if len(data_test) == 40:
                            data_test = np.array(list(map(float, data_test))).reshape(10, 4)  # 转换成矩阵
                            print(data_test.sum(axis=0) / 10)  # 矩阵每列求和
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









