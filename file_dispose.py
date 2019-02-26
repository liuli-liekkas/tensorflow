
import os
import os.path
import numpy as np
import math
from math import radians, cos, sin, asin, sqrt


def geodistance(lng1, lat1, lng2, lat2):
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
    dlon = lng2 - lng1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    dis = 2 * asin(sqrt(a)) * 6371 * 1000
    print(dis)


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
new_data = []
data_test = []
n_distance = []
e_distance = []
h_distance = []
for filename in files:
    with open(filename, 'r') as file:
        data = file.readlines()
        num = len(data)
    for line in range(num):
        if data[line].split(',')[0] == '$GNRMC':
            new_data.append(data[line])
        for num in range(len(new_data)):
            for i in range(10):
                if new_data[num + i].split(',')[3]:
                    data_test.append(new_data[num + i])
            if len(data_test) == 10:
                break
            else:
                data_test = []
            for num in range(len(data_test)):
                n_distance.append(data_test[num].split(',')[3])
                e_distance.append(data_test[num].split(',')[5])
                h_distance.append(data_test[num].split(',')[7])
            n_distance = np.array(list(map(float, n_distance)))
            e_distance = np.array(list(map(float, e_distance)))
            h_distance = np.array(list(map(float, h_distance)))
            # print(n_distance)
            # print(e_distance)
            # print(h_distance)
            # n_distance_true = np.zeros(10) + 3200.000000
            # e_distance_true = np.zeros(10) + 12000.000000
            # h_distance_true = np.zeros(10) + 0000.000000
            # print(n_distance_true)
            # print(e_distance_true)
            # print(h_distance_true)
            # n = n_distance - n_distance_true
            # e = e_distance - e_distance_true
            # h = h_distance - h_distance_true
            # print(n)
            # print(e)
            # print(h)
            lng1 = math.floor(e_distance.sum()/1000) + (e_distance.sum()/1000-math.floor(e_distance.sum()/1000))/0.6
            lat1 = math.floor(n_distance.sum()/1000) + (n_distance.sum()/1000-math.floor(n_distance.sum()/1000))/0.6
            lng2 = 130.000000
            lat2 = 40.000000
            if geodistance(lng1, lat1, lng2, lat2) > 100:
                data_test = []
                break
            else:
                print(geodistance(lng1, lat1, lng2, lat2))