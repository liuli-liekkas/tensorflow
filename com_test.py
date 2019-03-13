# coding=utf-8
import serial
import time
import math
import numpy as np
import tkinter
from itertools import chain
from tkinter import scrolledtext
from tkinter import ttk
import matplotlib.font_manager
import matplotlib.pyplot as plt
import threading


class GUI:
    def __init__(self):
        window = tkinter.Tk()
        window.title("GUI UART Tx/Rx Demo")
        self.uartState = False  # is uart open or not
        self.ser = serial.Serial()
        self.data_test = []
        self.utc_time = False
        self.location = False
        self.get_target = False
        self.time_start = 0
        self.lock_target = False
        self.num = 0
        self.first_label = set()

        # a frame contains COM's information, and start/stop button
        frame_COMinf = tkinter.Frame(window)
        frame_COMinf.grid(row=1, column=1)

        self.ReadUARTThread = threading.Thread(target=self.ReadUART)
        self.ReadUARTThread.start()

        labelCOM = tkinter.Label(frame_COMinf, text="COMx: ")
        self.COM = tkinter.StringVar(value="COM7")
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

        framePaint = tkinter.Frame(window)
        framePaint.grid(row=1, column=3, rowspan=3)

        self.title = tkinter.Label(framePaint, text="图片标签: ")
        self.entry_title = tkinter.Entry(framePaint)
        self.title.grid(row=1, column=1, padx=5, pady=3)
        self.entry_title.grid(row=1, column=2, padx=5, pady=3)

        hor_axis = tkinter.Label(framePaint, text="横轴标签: ")
        self.entry_hor_axis = tkinter.Entry(framePaint)
        hor_axis.grid(row=2, column=1, padx=5, pady=3)
        self.entry_hor_axis.grid(row=2, column=2, padx=5, pady=3)

        ver_axis = tkinter.Label(framePaint, text="纵轴标签: ")
        self.entry_ver_axis = tkinter.Entry(framePaint)
        ver_axis.grid(row=3, column=1, padx=5, pady=3)
        self. entry_ver_axis.grid(row=3, column=2, padx=5, pady=3)

        self.num = 10

        test_value = tkinter.Label(framePaint, text="数据" + str(1) + ':')
        self.entry_test_value_1 = tkinter.Entry(framePaint)
        test_value.grid(row=4, column=1, padx=5, pady=3)
        self.entry_test_value_1.grid(row=4, column=2, padx=5, pady=3)

        test_value = tkinter.Label(framePaint, text="数据" + str(2) + ':')
        self.entry_test_value_2 = tkinter.Entry(framePaint)
        test_value.grid(row=5, column=1, padx=5, pady=3)
        self.entry_test_value_2.grid(row=5, column=2, padx=5, pady=3)

        test_value = tkinter.Label(framePaint, text="数据" + str(3) + ':')
        self.entry_test_value_3 = tkinter.Entry(framePaint)
        test_value.grid(row=6, column=1, padx=5, pady=3)
        self.entry_test_value_3.grid(row=6, column=2, padx=5, pady=3)

        test_value = tkinter.Label(framePaint, text="数据" + str(4) + ':')
        self.entry_test_value_4 = tkinter.Entry(framePaint)
        test_value.grid(row=7, column=1, padx=5, pady=3)
        self.entry_test_value_4.grid(row=7, column=2, padx=5, pady=3)

        test_value = tkinter.Label(framePaint, text="数据" + str(5) + ':')
        self. entry_test_value_5 = tkinter.Entry(framePaint)
        test_value.grid(row=8, column=1, padx=5, pady=3)
        self.entry_test_value_5.grid(row=8, column=2, padx=5, pady=3)

        test_value = tkinter.Label(framePaint, text="数据" + str(6) + ':')
        self.entry_test_value_6 = tkinter.Entry(framePaint)
        test_value.grid(row=9, column=1, padx=5, pady=3)
        self.entry_test_value_6.grid(row=9, column=2, padx=5, pady=3)

        test_value = tkinter.Label(framePaint, text="数据" + str(7) + ':')
        self.entry_test_value_7 = tkinter.Entry(framePaint)
        test_value.grid(row=10, column=1, padx=5, pady=3)
        self.entry_test_value_7.grid(row=10, column=2, padx=5, pady=3)

        test_value = tkinter.Label(framePaint, text="数据" + str(8) + ':')
        self. entry_test_value_8 = tkinter.Entry(framePaint)
        test_value.grid(row=11, column=1, padx=5, pady=3)
        self.entry_test_value_8.grid(row=11, column=2, padx=5, pady=3)

        test_value = tkinter.Label(framePaint, text="数据" + str(9) + ':')
        self.entry_test_value_9 = tkinter.Entry(framePaint)
        test_value.grid(row=12, column=1, padx=5, pady=3)
        self.entry_test_value_9.grid(row=12, column=2, padx=5, pady=3)

        test_value = tkinter.Label(framePaint, text="数据" + str(10) + ':')
        self.entry_test_value_10 = tkinter.Entry(framePaint)
        test_value.grid(row=13, column=1, padx=5, pady=3)
        self.entry_test_value_10.grid(row=13, column=2, padx=5, pady=3)

        self.button_paint = tkinter.Button(framePaint, text="画图", command=self.paint)
        self.button_paint.grid(row=14, column=2, padx=5, pady=3, sticky=tkinter.E)

        window.mainloop()

    def paint(self):
        matplotlib.use('qt4agg')
        matplotlib.rcParams['font.sans-serif'] = ['SimHei']
        matplotlib.rcParams['font.family'] = 'sans-serif'
        matplotlib.rcParams['axes.unicode_minus'] = False
        value = []
        x_list = [1,2,3,4,5,6,7,8,9,10]
        value.append(float(self.entry_test_value_1.get()))
        value.append(float(self.entry_test_value_2.get()))
        value.append(float(self.entry_test_value_3.get()))
        value.append(float(self.entry_test_value_4.get()))
        value.append(float(self.entry_test_value_5.get()))
        value.append(float(self.entry_test_value_6.get()))
        value.append(float(self.entry_test_value_7.get()))
        value.append(float(self.entry_test_value_8.get()))
        value.append(float(self.entry_test_value_9.get()))
        value.append(float(self.entry_test_value_10.get()))
        plt.figure(figsize=(10, 8))
        plt.plot(x_list, value, lw=1.5)
        plt.grid(True)
        plt.axis('tight')
        plt.xlabel(self.entry_hor_axis.get())
        plt.ylabel(self.entry_ver_axis.get())
        plt.title(self.entry_title.get())
        plt.show()

    def processButtonSS(self):
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
            bytesToSend = strToSend[0:-1].encode(encoding='utf-8')
            self.ser.write(bytesToSend)
            print(bytesToSend)
        else:
            print("Not In Connect!")

    def ReadUART(self):
        while True:
            if self.uartState:
                try:
                    line = self.ser.readline().decode(encoding='gb18030')
                    self.OutputText.insert(tkinter.END, line)
                    self.OutputText.see(tkinter.END)
                    self.OutputText.update()
                except :
                    continue
                # if line.split(',')[0] == '$ACKOK':
                #     self.OutputTest.insert(tkinter.END, "系统已经重启完毕，开始计时……" + '\n')
                #     data_test = []
                #     utc_time = False
                #     location = False
                #     get_target = False
                #     time_start = time.time()
                #     lock_target = False
                #     continue
                if line.split(',')[0] == '$GNRMC':
                    self.OutputText.insert(tkinter.END, '\n')
                    if not self.utc_time and line.split(',')[1] != '' and (line.split(',')[3]) == '':
                        self.data_test = []
                        self.location = False
                        self.get_target = False
                        self.time_start = time.time()
                        self.lock_target = False
                        self.utc_time = True
                        self.OutputTest.insert(tkinter.END, "系统已经成功获得UTC时间，还没开始定位……" + '\n')
                        self.OutputTest.see(tkinter.END)
                        self.OutputTest.update()
                        continue
                    elif line.split(',')[1] != '' and line.split(',')[3] == '':
                        if self.get_target:
                            self.get_target = False
                            self.lock_target = False
                            self.OutputTest.insert(tkinter.END, "系统丢失目标，开始重新定位……" + '\n')
                            self.OutputTest.see(tkinter.END)
                            self.OutputTest.update()
                            self.data_test = []
                            self.time_start = time.time()
                    elif line.split(',')[1] == '' and line.split(',')[3] == '':
                        if self.get_target:
                            self.get_target = False
                            self.utc_time = False
                            self.lock_target = False
                            self.OutputTest.insert(tkinter.END, "系统丢失信号，开始搜索信号……" + '\n')
                            self.OutputTest.see(tkinter.END)
                            self.OutputTest.update()
                            self.time_start = time.time()
                            self.data_test = []
                    elif line.split(',')[3] != '' and line.split(',')[5] != '' and line.split(',')[7] != '':
                        if not self.location:
                            self.location = True
                        self.data_test.append(line.split(',')[3])  # 提取纬度信息
                        self.data_test.append(line.split(',')[5])  # 提取精度信息
                        self.data_test.append(line.split(',')[7])  # 提取速度信息
                        continue
                elif line.split(',')[0] == '$GNGGA' and line.split(',')[3] != '':
                    if not self.get_target:
                        self.get_target = True
                        self.OutputTest.insert(tkinter.END, "系统开始定位" + '\n')  # 计算捕获时间
                        self.OutputTest.see(tkinter.END)
                        self.OutputTest.update()
                    time_get_target = time.time()
                    self.data_test.append(line.split(',')[9])  # 提取高度信息
                    self.data_test.append(time_get_target)  # 提取定位时间
                    if len(self.data_test) == 50 and not self.lock_target:
                        self.data_test = np.array(list(map(float, self.data_test))).reshape(10, 5)  # 转换成矩阵
                        data_test_detail = self.data_test[:, 0:4].sum(axis=0) / 10  # 矩阵每列求和
                        lat_default = 31.283508816666668
                        lng_default = 121.18034377500001
                        data_test_detail[0] = math.floor(data_test_detail[0] / 100) + (data_test_detail[0] / 100 - math.floor(data_test_detail[0] / 100)) / 0.6
                        data_test_detail[1] = math.floor(data_test_detail[1] / 100) + (data_test_detail[1] / 100 - math.floor(data_test_detail[1] / 100)) / 0.6
                        high_distance = data_test_detail[3]
                        geo_distance = self.geo_distance_two(data_test_detail[0], data_test_detail[1], lat_default, lng_default)
                        if geo_distance > 100 or high_distance > 100:
                            self.data_test = list(chain(*self.data_test))
                            del self.data_test[0:5]
                            geo_distance = str(geo_distance)
                            high_distance = str(high_distance)
                            self.OutputTest.insert(tkinter.END, "定位无效，水平误差为：" + geo_distance + '米' + '\n'
                                                   + '定位无效，垂直误差为：' + high_distance + '米' + '\n' + '\n')
                            self.OutputTest.see(tkinter.END)
                            self.OutputTest.update()
                            continue
                        elif geo_distance < 100 and high_distance < 100:
                            self.lock_target = True
                            geo_distance = str(geo_distance)
                            high_distance = str(high_distance)
                            final_time_get_target = self.data_test[0, -1] - self.time_start
                            final_time_get_target = str(final_time_get_target)
                            self.data_test = list(chain(*self.data_test))
                            self.OutputTest.insert(tkinter.END, '定位有效，水平误差为：' + geo_distance + '米' + '\n'
                                                   + '定位有效，垂直误差为：' + high_distance + '米' + '\n'
                                                   + '定位有效，首次定位时间为：' + final_time_get_target + '秒' + '\n' + '\n')
                            self.OutputTest.see(tkinter.END)
                            self.OutputTest.update()

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
    @staticmethod
    def geo_distance_two(lat_test, lng_test, lat_default, lng_default):
        lat1, lng1, lat2, lng2 = map(math.radians, [lat_test, lng_test, lat_default, lng_default])  # 角度转弧度
        d_lat = lat2 - lat1
        d_lng = lng2 - lng1
        a = math.sin(d_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lng / 2) ** 2
        dis = 2 * math.asin(math.sqrt(a)) * 6371 * 1000
        return dis


GUI()


