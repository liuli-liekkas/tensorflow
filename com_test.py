import serial
import time
import math
import numpy as np
import tkinter


class Application():
    def __init__(self):
        self.serial = serial.Serial('COM5', 115200, timeout=0.1)
        self.hot_set = '$reset,1,2'
        self.col_set = '$reset,1,0'

        def get_data():
            utc_time = False
            location = False
            data_test = []
            while True:
                line = serial.readline()
                line = line.decode('utf-8')
                if line:
                    if line.split(',')[0] == '$reset':
                        print('已发送指令：', self.hot_set)
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
                                time_delta = time.time() - time_start
                                print("系统开始定位,首次捕获时间为：", time_delta)  # 计算捕获时间
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

            def geodistance(lng_test, lat_test, h_test, lng_default, lat_default, h_default):
                lng_test, lat_test, lng_default, lat_default = map(math.radians,
                                                                   [lng_test, lat_test, lng_default, lat_default])
                delta_x = h_test * math.cos(lat_test) * math.cos(lng_test) - h_test * math.cos(lat_default) * math.cos(
                    lng_default)
                delta_y = h_test * math.cos(lat_test) * math.sin(lng_test) - h_test * math.cos(lat_default) * math.sin(
                    lng_default)
                delta_z = h_test - h_default
                dis = math.sqrt(delta_x + delta_y + delta_z)
                return dis

        if serial.isOpen():
            print("串口打开成功，开始接收数据……")
            window = tkinter.Tk()
            self.window_set(window)
            # self.entry = tkinter.Entry(window, show=None)
            # self.entry.pack()
            self.var1 = tkinter.StringVar()
            self.l = tkinter.Label(window, width=30, textvariable=self.var1)
            self.l.pack()
            self.b1 = tkinter.Button(window,  text='发送指令', width=15, height=2, command=self.print_selection)
            self.b1.pack()

            # self.text = tkinter.Text(window, height=10)
            # self.text.pack()
            # # button1 = tkinter.Button(window, text='insert point', width=15, height=2, command=self.insert_point)
            # button1.pack()
            # button2 = tkinter.Button(window, text='insert end', command=self.insert_end)
            # button2.pack()
            self.var2 = tkinter.StringVar()
            self.var2.set((self.hot_set, self.col_set))
            self.lb = tkinter.Listbox(window, listvariable=self.var2)
            self.lb.pack()
        else:
            print("串口打开失败")



    def window_set(self, window):
        window.title("导航测试系统")
        window.geometry('800x600')

    def insert_point(self):
        var = self.entry.get()
        self.text.insert('insert', var)

    def insert_end(self):
        var = self.entry.get()
        self.text.insert(2.2, var)

    def print_selection(self):
        value = self.lb.get(self.lb.curselection())
        print(value)
        serial.write((value + '\n').encode())
        self.var1.set(value)
        return value

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
    app.mainloop()








