# coding=utf-8
import serial
import time
import math
import numpy as np
import tkinter
from itertools import chain
from tkinter import scrolledtext
from tkinter import ttk
import matplotlib as mpl
import matplotlib.pyplot as plt
import threading

class GUI:
    def __init__(self):
        window = tkinter.Tk()
        window.title("GUI UART Tx/Rx Demo")
        self.uartState = False  # is uart open or not

        # a frame contains COM's information, and start/stop button
        frame_COMinf = tkinter.Frame(window)
        frame_COMinf.grid(row=1, column=1)

        labelCOM = tkinter.Label(frame_COMinf, text="COMx: ")
        self.COM = tkinter.StringVar(value="COM6")
        ertryCOM = tkinter.Entry(frame_COMinf, textvariable=self.COM)
        labelCOM.grid(row=1, column=1, padx=5, pady=3)
        ertryCOM.grid(row=1, column=2, padx=5, pady=3)

        labelBaudrate = tkinter.Label(frame_COMinf, text="Baudrate: ")
        self.Baudrate = tkinter.IntVar(value=9600)
        ertryBaudrate = tkinter.Entry(frame_COMinf, textvariable=self.Baudrate)
        labelBaudrate.grid(row=1, column=3, padx=5, pady=3)
        ertryBaudrate.grid(row=1, column=4, padx=5, pady=3)

        labelParity = tkinter.Label(frame_COMinf, text="Parity: ")
        self.Parity = tkinter.StringVar(value="NONE")
        comboParity = ttk.Combobox(frame_COMinf, width=17, textvariable=self.Parity)
        comboParity["values"] = ("NONE", "ODD", "EVEN", "MARK", "SPACE")
        comboParity["state"] = "readonly"
        labelParity.grid(row=2, column=1, padx=5, pady=3)
        comboParity.grid(row=2, column=2, padx=5, pady=3)

        labelStopbits = tkinter.Label(frame_COMinf, text="Stopbits: ")
        self.Stopbits = tkinter.StringVar(value="1")
        comboStopbits = ttk.Combobox(frame_COMinf, width=17, textvariable=self.Stopbits)
        comboStopbits["values"] = ("1", "1.5", "2")
        comboStopbits["state"] = "readonly"
        labelStopbits.grid(row=2, column=3, padx=5, pady=3)
        comboStopbits.grid(row=2, column=4, padx=5, pady=3)

        self.buttonSS = tkinter.Button(frame_COMinf, text="Start", command=self.processButtonSS)
        self.buttonSS.grid(row=3, column=4, padx=5, pady=3, sticky=tkinter.E)

        # serial object
        self.ser = serial.Serial()
        # serial read threading
        self.ReadUARTThread = threading.Thread(target=self.ReadUART)
        self.ReadUARTThread.start()

        frameTest = tkinter.Frame(window)
        frameTest.grid(row=2, column=1)
        labelOutTest = tkinter.Label(frameTest, text="Test Data:")
        labelOutTest.grid(row=1, column=1, padx=3, pady=2, sticky=tkinter.W)
        frameTestSon = tkinter.Frame(frameTest)
        frameTestSon.grid(row=2, column=1)
        scrollbarTest = tkinter.Scrollbar(frameTestSon)
        scrollbarTest.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.OutputTest = tkinter.Text(frameTestSon, wrap=tkinter.WORD, width=60, height=20, yscrollcommand=scrollbarTest.set)
        self.OutputTest.pack()

        frameTrans = tkinter.Frame(window)
        frameTrans.grid(row=3, column=1)
        labelInText = tkinter.Label(frameTrans, text="To Transmit Data:")
        labelInText.grid(row=1, column=1, padx=3, pady=2, sticky=tkinter.W)
        frameTransSon = tkinter.Frame(frameTrans)
        frameTransSon.grid(row=2, column=1)
        scrollbarTrans = tkinter.Scrollbar(frameTransSon)
        scrollbarTrans.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.InputText = tkinter.Text(frameTransSon, wrap=tkinter.WORD, width=60, height=5, yscrollcommand=scrollbarTrans.set)
        self.InputText.pack()
        self.buttonSend = tkinter.Button(frameTrans, text="Send", command=self.processButtonSend)
        self.buttonSend.grid(row=3, column=1, padx=5, pady=3, sticky=tkinter.E)

        frameRecv = tkinter.Frame(window)
        frameRecv.grid(row=1, column=2, rowspan=3)
        labelOutText = tkinter.Label(frameRecv, text="Received Data:")
        labelOutText.grid(row=1, column=1, padx=3, pady=2, sticky=tkinter.W)
        frameRecvSon = tkinter.Frame(frameRecv)
        frameRecvSon.grid(row=2, column=1)
        scrollbarRecv = tkinter.Scrollbar(frameRecvSon)
        scrollbarRecv.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.OutputText = tkinter.Text(frameRecvSon, wrap=tkinter.WORD, width=80, height=40, yscrollcommand=scrollbarRecv.set)
        self.OutputText.pack()

        window.mainloop()

    def processButtonSS(self):
        # print(self.Parity.get())
        if self.uartState:
            self.ser.close()
            self.buttonSS["text"] = "Start"
            self.uartState = False
        else:
            # restart serial port
            self.ser.port = self.COM.get()
            self.ser.baudrate = self.Baudrate.get()

            strParity = self.Parity.get()
            if strParity == "NONE":
                self.ser.parity = serial.PARITY_NONE
            elif strParity == "ODD":
                self.ser.parity = serial.PARITY_ODD
            elif strParity == "EVEN":
                self.ser.parity = serial.PARITY_EVEN
            elif strParity == "MARK":
                self.ser.parity = serial.PARITY_MARK
            elif strParity == "SPACE":
                self.ser.parity = serial.PARITY_SPACE

            strStopbits = self.Stopbits.get()
            if strStopbits == "1":
                self.ser.stopbits = serial.STOPBITS_ONE
            elif strStopbits == "1.5":
                self.ser.stopbits = serial.STOPBITS_ONE_POINT_FIVE
            elif strStopbits == "2":
                self.ser.stopbits = serial.STOPBITS_TWO

            self.ser.open()
            if self.ser.isOpen():  # open success
                self.buttonSS["text"] = "Stop"
                self.uartState = True

    def processButtonSend(self):
        if self.uartState:
            strToSend = self.InputText.get(1.0, tkinter.END)
            bytesToSend = strToSend[0:-1].encode(encoding='ascii')
            self.ser.write(bytesToSend)
            print(bytesToSend)
        else:
            print("Not In Connect!")

    def ReadUART(self):
        # print("Threading...")
        while True:
            if self.uartState:
                line = self.ser.readline().decode(encoding='ascii')
                self.OutputText.insert(tkinter.END, line)
                if line:
                    if line.split(',')[0] == '$ACKOK':
                        self.OutputTest.insert(tkinter.END, "系统已经重启完毕，开始计时……" + '\n')
                        data_test = []
                        utc_time = False
                        location = False
                        time_start = time.time()
                        continue
                    elif line.split(',')[0] == '$GNRMC':
                        if not utc_time and line.split(',')[1] != '' and (line.split(',')[3]) == '':
                            self.OutputTest.insert(tkinter.END, "系统已经成功获得UTC时间，还没开始定位……" + '\n')
                            utc_time = True
                            continue
                        elif utc_time and line.split(',')[3] != '':
                            if not location:
                                time_delta = time.time() - time_start
                                time_delta = str(time_delta)
                                self.OutputTest.insert(tkinter.END, "系统开始定位,首次捕获时间为：" + time_delta + '\n')  # 计算捕获时间
                                location = True
                            data_test.append(line.split(',')[3])  # 提取纬度信息
                            data_test.append(line.split(',')[5])  # 提取精度信息
                            data_test.append(line.split(',')[7])  # 提取速度信息
                    elif line.split(',')[0] == '$GNGGA':
                        if line.split(',')[3] != '':
                            data_test.append(line.split(',')[9])  # 提取高度信息
                            if len(data_test) == 40:
                                data_test = np.array(list(map(float, data_test))).reshape(10, 4)  # 转换成矩阵
                                data_test_detail = data_test.sum(axis=0) / 10  # 矩阵每列求和
                                lat_default = 32
                                lng_default = 120
                                data_test_detail[0] = math.floor(data_test_detail[0] / 100) + (data_test_detail[0] / 100 - math.floor(data_test_detail[0] / 100)) / 0.6
                                data_test_detail[1] = math.floor(data_test_detail[1] / 100) + (data_test_detail[1] / 100 - math.floor(data_test_detail[1] / 100)) / 0.6
                                high_distance = data_test_detail[3]
                                geo_distance = self.geo_distance_two(data_test_detail[0], data_test_detail[1], lat_default, lng_default)
                                if geo_distance > 100 or high_distance > 100:
                                    data_test = list(chain(*data_test))
                                    del data_test[0:4]
                                    geo_distance = str(geo_distance)
                                    high_distance = str(high_distance)
                                    self.OutputTest.insert(tkinter.END, "定位无效，水平误差为：" + geo_distance + '米' + '\n'
                                                           + '定位无效，垂直误差为：' + high_distance + '米' + '\n')
                                    continue
                                elif geo_distance < 100 and high_distance < 100:
                                    geo_distance = str(geo_distance)
                                    high_distance = str(high_distance)
                                    self.OutputTest.insert(tkinter.END, '定位有效，水平误差为：' + geo_distance + '米' + '\n'
                                                           + '定位无效，垂直误差为：' + high_distance + '米' + '\n')
                                    break

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

GUI()

# class Application:
#     def __init__(self):
#         # self.serial = serial.Serial('COM5', 115200, timeout=0.1)
#         self.window = tkinter.Tk()
#         self.set_window(self.window)
#         self.reset_port()
#         self.scrolled_window()
#         self.test_window()
#         # self.test_main()
#
#         self.window.mainloop()
#
#     @staticmethod
#     def set_window(window):
#         window.title("导航测试系统")
#         window.geometry('1200x800')
#
#     def reset_port(self):
#         global e1
#         global e2
#         global b1
#         global b2
#         monty = ttk.LabelFrame(self.window, text=" 指令窗口 ")
#         monty.grid(column=0, row=0, padx=10, pady=10, sticky='W')
#         s1 = tkinter.Label(monty, text='指令1：')
#         s1.grid(row=0, column=0, sticky='W')
#         e1 = tkinter.Entry(monty, show=None)
#         e1.grid(row=0, column=1, sticky='E')
#         b1 = tkinter.Button(monty, text='发送', command=self.send_port1)
#         b1.grid(row=0, column=2, sticky='E')
#         s2 = tkinter.Label(monty, text='指令2:')
#         s2.grid(row=1, column=0, sticky='W')
#         e2 = tkinter.Entry(monty, show=None)
#         e2.grid(row=1, column=1, sticky='E')
#         b2 = tkinter.Button(monty, text='发送', command=self.send_port2)
#         b2.grid(row=1, column=2, sticky='E')
#
#         # hot_set = '$reset,1,2'
#         # col_set = '$reset,1,0'
#     def send_port1(self):
#         message1 = e1.get()
#         self.serial.write(message1.encode('utf-8') + '\n')
#
#     def send_port2(self):
#         message2 = e2.get()
#         self.serial.write(message2.encode('utf-8') + '\n')
#
#     def scrolled_window(self):
#         global scr_show
#         scrolled_W = 80
#         scrolled_H = 20
#         monty = ttk.LabelFrame(self.window, text=" 报文数据 ")
#         monty.grid(row=1, column=0, padx=10, pady=10)
#         scr_show = tkinter.scrolledtext.ScrolledText(monty, width=scrolled_W, height=scrolled_H, wrap=tkinter.WORD)
#         scr_show.grid(column=0, columnspan=3)
#
#     def test_window(self):
#         global scr_test
#         scrolled_W = 80
#         scrolled_H = 10
#         monty = ttk.LabelFrame(self.window, text=" 测试结果 ")
#         monty.grid(row=2, column=0, padx=10, pady=10)
#         scr_test = tkinter.scrolledtext.ScrolledText(monty, width=scrolled_W, height=scrolled_H, wrap=tkinter.WORD)
#         scr_test.grid(column=0, columnspan=3)
#
#     def get_data(self):
#         line = self.serial.readline()
#         line = line.decode('utf-8')
#         scr_show.insert('end', line)
#         scr_show.update()
#         scr_show.see('end')
#         return line
#
#     def paint(self, x_data, y_data, x_label, y_label, title, name):
#         plt.figure()
#         plt.xlabel(x_label, size=14)
#         plt.ylabel(y_label, size=14)
#         plt.title(title, size=14)
#         plt.plot(x_data, y_data, linewidth=2, c='b')
#         plt.grid(True)
#         plt.axis('tight')
#         plt.show()
#         plt.savefig(name + '.jpg')
#
#     # 三点计算公式
#     def geo_distance_three(self, lng_test, lat_test, h_test, lng_default, lat_default, h_default):
#         lng_test, lat_test, lng_default, lat_default = map(math.radians, [lng_test, lat_test, lng_default, lat_default])
#         delta_x = h_test * math.cos(lat_test) * math.cos(lng_test) - h_test * math.cos(lat_default) * math.cos(
#             lng_default)
#         delta_y = h_test * math.cos(lat_test) * math.sin(lng_test) - h_test * math.cos(lat_default) * math.sin(
#             lng_default)
#         delta_z = h_test - h_default
#         dis = math.sqrt(delta_x + delta_y + delta_z)
#         return dis
#
#     # 经典两点计算公式
#     def geo_distance_two(self, lat_test, lng_test, lat_default, lng_default):
#         lat1, lng1, lat2, lng2 = map(math.radians, [lat_test, lng_test, lat_default, lng_default])  # 角度转弧度
#         d_lat = lat2 - lat1
#         d_lng = lng2 - lng1
#         a = math.sin(d_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lng / 2) ** 2
#         dis = 2 * math.asin(math.sqrt(a)) * 6371 * 1000
#         return dis
#
#     def test_main(self):
#         utc_time = False
#         location = False
#         data_test = []
#         time_start = 0
#         while True:
#             time.sleep(0.01)
#             line = self.get_data()
#             if line:
#                 if line.split(',')[0] == e1.get():
#                     scr_test.insert('end', '已发送指令1:' + e1.get())
#                     scr_test.update()
#                     scr_test.see('end')
#                     continue
#                 elif line.split(',')[0] == e2.get():
#                     scr_test.insert('end', '已发送指令2:' + e2.get())
#                     scr_test.update()
#                     scr_test.see('end')
#                     continue
#                 elif line.split(',')[0] == '$ACKOK':
#                     scr_test.insert('end', "系统已经重启完毕，开始计时……")
#                     scr_test.update()
#                     scr_test.see('end')
#                     time_start = time.time()
#                     continue
#                 elif line.split(',')[0] == '$GNRMC':
#                     if not utc_time and line.split(',')[1] and not(line.split(',')[3]):
#                         scr_test.insert('end', "系统已经成功获得UTC时间，还没开始定位……")
#                         scr_test.update()
#                         scr_test.see('end')
#                         utc_time = True
#                     if line.split(',')[3]:
#                         if not location:
#                             time_delta = time.time() - time_start
#                             time_delta = str(time_delta)
#                             scr_test.insert('end, '"系统开始定位,首次捕获时间为：" + time_delta)  # 计算捕获时间
#                             scr_test.update()
#                             scr_test.see('end')
#                             location = True
#                         data_test.append(self.get_data().split(',')[3])  # 提取纬度信息
#                         data_test.append(self.get_data().split(',')[5])  # 提取精度信息
#                         data_test.append(self.get_data().split(',')[7])  # 提取速度信息
#                 elif line.split(',')[0] == '$GNGGA':
#                     if line.split(',')[3]:
#                         data_test.append(line.split(',')[9])  # 提取高度信息
#                         if len(data_test) == 40:
#                             data_test = np.array(list(map(float, data_test))).reshape(10, 4)  # 转换成矩阵
#                             data_test = data_test.sum(axis=0) / 10  # 矩阵每列求和
#                             scr_test.insert('end', data_test)
#                             scr_test.update()
#                             scr_test.see('end')
#                             lat_default = 30
#                             lng_default = 100
#                             geo_distance = self.geo_distance_two(data_test[0], data_test[1], lat_default, lng_default)
#                             if geo_distance > 100 or data_test[3] > 100:
#                                 np.delete(data_test, 0, axis=1)
#                                 geo_distance = str(geo_distance)
#                                 scr_test.insert('end', "定位无效，水平误差为：" + geo_distance + '米'
#                                                 + '\n' + '定位无效，垂直误差为：' + geo_distance + '米')
#                                 scr_test.update()
#                                 scr_test.see('end')
#                             elif geo_distance < 100 and data_test[3] < 100:
#                                 geo_distance = str(geo_distance)
#                                 scr_test.insert('end', '定位有效，水平误差为：' + geo_distance + '米'
#                                                 + '\n' + '定位无效，垂直误差为：' + geo_distance + '米')
#                                 scr_test.update()
#                                 scr_test.see('end')
#                                 break
#

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


# if __name__ == '__main__':
#     app = Application()
