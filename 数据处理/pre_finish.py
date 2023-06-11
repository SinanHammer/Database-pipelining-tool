# -*- coding: utf-8 -*-
import pandas as pd

# 导入数据
data1 = pd.read_excel('1.xlsx')
data2 = pd.read_excel('2.xlsx')

print(data1)
print(data2)

# 构建最终结果
result_data = []

for i in range(len(data1)):
    d1 = data1.iloc[i]
    d2 = data2[data2['reference_no'] == d1['reference_no']]
    row_data = {
        'Group': 'Tetrapod',
        'Guild': '',
        'Taxon': d1['accepted_name'],
        'Location': (str(d1['state']) + 'State,' if d1['state'] else '') + (str(d1['cc']) if d1['cc'] else ''),
        'Foamation': d1['formation'],
        'Age': str(d1['early_interval']) + '-' + str(d1['late_interval']),
        'Length of Skull (头骨长度, mm）': '',
        'Length of whole body （身体长度,cm）': '',
        'Reference': str(d2['author1last'].values[0]) +' ' +'et al.' + str(d2['pubyr'].values[0]) + "." + str(d2['reftitle'].values[0]) if d2['doi'].isnull().values[0] else str(d2['author1last'].values[0]) +' '+'et al.' + str(d2['pubyr'].values[0]) + '.' +str(d2['pubtitle'].values[0]),
        'DOI': d2['doi'],
        'title': d2['reftitle']
    }
    row_df = pd.DataFrame(row_data)
    result_data.append(row_df)

result = pd.concat(result_data, ignore_index=True)
print(result)
result.to_excel("恐龙数据库.xlsx")
