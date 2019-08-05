import os.path
import numpy as np
import math

filename = "e:/测试数据/碰撞起始点.txt"
data_gnrmc = []
data_test = []
with open(filename, 'r') as file:
    data = file.readlines()
    num = len(data)
for line in range(num):
    if data[line].split(',')[0] == '$GNRMC' and data[line].split(',')[3]:
        data_test.append(data[line].split(',')[3])
        data_test.append(data[line].split(',')[5])
        data_test.append(data[line].split(',')[7])
test_num = len(data_test)
data_test = np.array(list(map(float, data_test))).reshape(int(test_num/3), 3)
print(data_test)
print("平均值为：", np.mean(data_test, axis=0))
