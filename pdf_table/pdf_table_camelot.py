import camelot.io as camelot
import os

import pandas as pd

os.chdir('C:/Users/DELL/Desktop')
import cv2
data1= camelot.read_pdf("22.pdf", pages='1-10',flavor='stream')
print(data1)
print(data1[0].data)
for i in range(len(data1)):
    data1[i].to_csv('data'+str({i})+'.csv',encoding='utf_8_sig')