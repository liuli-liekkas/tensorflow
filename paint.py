import pandas as pd
import os
import numpy as np


path = "e:/闻颂/"
files = os.listdir(path)
for filename in files:
    portion = os.path.splitext(filename)
    if portion[1] == '.dat':
        new_name = portion[0] + '.txt'
        os.chdir(path)
        os.rename(filename, new_name)
data = pd.read_csv(path+'水平20190321.txt', sep='\t')
print(data.values)