import os.path
import numpy as np
import math


# 经典两点计算公式
# def geodistance(lng_test, lat_test, lng_default, lat_default):
#     lng1, lat1, lng2, lat2 = map(math.radians, [lng_test, lat_test, lng_default, lat_default])  # 角度转弧度
#     d_lng = lng2 - lng1
#     d_lat = lat2 - lat1
#     a = math.sin(d_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lng / 2) ** 2
#     dis = 2 * math.asin(math.sqrt(a)) * 6371 * 1000
#     print(dis)


def geodistance(lng_test, lat_test, h_test, lng_default, lat_default, h_default):
    lng_test, lat_test, lng_default, lat_default = map(math.radians, [lng_test, lat_test, lng_default, lat_default])
    delta_x = h_test * math.cos(lat_test) * math.cos(lng_test) - h_test * math.cos(lat_default) * math.cos(lng_default)
    delta_y = h_test * math.cos(lat_test) * math.sin(lng_test) - h_test * math.cos(lat_default) * math.sin(lng_default)
    delta_z = h_test - h_default
    dis = math.sqrt(delta_x + delta_y + delta_z)
    return dis


path1 = "e:/测试数据/"
files = os.listdir(path1)
for filename in files:
    portion = os.path.splitext(filename)
    if portion[1] == '.dat':
        new_name = portion[0] + '.txt'
        os.chdir(path1)
        os.rename(filename, new_name)
files = os.listdir(path1)
os.chdir(path1)
data_gnrmc = []
data_gngga = []
data_test = []
n_test = []
e_test = []
h_test = []
v_test = []
lng_default = 130.000000
lat_default = 40.000000
h_default = 50
for filename in files:
    with open(filename, 'r') as file:
        data = file.readlines()
        num = len(data)
    for line in range(num):
        if data[line].split(',')[0] == '$GNRMC':
            data_gnrmc.append(data[line])
        if data[line].split(',')[0] == '$GNGGA':
            data_gngga.append(data[line])
        for num in range(len(data_gnrmc)):
            for i in range(10):
                if data_gnrmc[num + i].split(',')[3] and data_gngga[num + i].split(',')[9]:
                    data_test.append(data_gnrmc[num + i].split(',')[3])
                    data_test.append(data_gnrmc[num + i].split(',')[5])
                    data_test.append(data_gnrmc[num + i].split(',')[7])
                    data_test.append(data_gngga[num + i].split(',')[9])
            if len(data_test) == 40:
                data_test = np.array(list(map(float, data_test))).reshape(4, 10)
                lng_test = math.floor(data_test.sum(axis=1)[1] / 1000) + (
                            data_test.sum(axis=1)[1] / 1000 - math.floor(data_test.sum(axis=1)[1] / 1000)) / 0.6
                lat_test = math.floor(data_test.sum(axis=1)[0] / 1000) + (
                            data_test.sum(axis=1)[0] / 1000 - math.floor(data_test.sum(axis=1)[0] / 1000)) / 0.6
                h_test = data_test.sum(axis=1)[3]
                if geodistance(lng_test, lat_test, h_test, lng_default, lat_default, h_default) > 100:
                    data_test = []
                    continue
                else:
                    print("定位误差为:", geodistance(lng_test, lat_test, h_test, lng_default, lat_default, h_default))
                    print("定位时间为:", num, "秒")
                    break
            else:
                data_test = []

