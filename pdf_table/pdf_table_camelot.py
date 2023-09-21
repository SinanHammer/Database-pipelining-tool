import camelot.io as camelot
import os

import pandas as pd

os.chdir('F:\PycharmProjects\Database-pipelining-tool\pdf_table')

data1= camelot.read_pdf("test.pdf", pages='1',flavor='stream')
print(data1)
print(data1[0].data)
for i in range(len(data1)):
    data1[i].to_csv('data'+str({i})+'.csv',encoding='utf_8_sig')