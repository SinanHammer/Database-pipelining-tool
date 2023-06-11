import pandas as pd

# 导入数据
data1 = pd.read_excel('1.xlsx')
data2 = pd.read_excel('2.xlsx')
pre_data = pd.read_excel('规范.xlsx')

print(data1)
print(data2)
print(pre_data)

#函数构建
# def comb(d1):
#     output1 = None
#     if d1['cc'] is None:
#         output1 = ''
#     elif d1['state'] is None:
#         output1 = d1['cc']
#     elif d1['county'] is None:
#         output1 = (str(d1['state']) + 'State,' if d1['state'] else '') + (str(d1['cc']) if d1['cc'] else '')
#     else:
#         output1 = str(d1['county']) + 'Country,' + str(d1['state']) + 'State,' + str(d1['cc'])
#
#     return output1
#
# def ref_com(d1, data2):
#     d2 = data2[data2['reference_no'] == d1['reference_no']]
#     output2 = ''
#     if d2['doi'] is None:
#         output2 = str(d2['author1last']) + 'et al.' + str(d2['pubyr']) + "." + str(d2['reftitle'])
#     else:
#         output2 = str(d2['author1last']) + 'et al.' + str(d2['pubyr'])
#     return output2



#构建最终结果
result = pd.DataFrame()
for i in range(len(data1)):
    d1 = data1.iloc[i]
    d2 = data2[data2['reference_no'] == d1['reference_no']]
    result['Group'] = 'Tetrapod'
    result['Guild'] = ''
    result['Taxon'] = d1['accepted_name']
    result['Location'] = (str(d1['state']) + 'State,' if d1['state'] else '') + (str(d1['cc']) if d1['cc'] else '')
    result['Foamation'] = d1['formation']
    result['Age'] = str(d1['early_interval']) + '-' + str(d1['late_interval'])
    result['Length of Skull (头骨长度, mm）'] = ''
    result['Length of whole body （身体长度,cm）'] = ''
    result['Reference'] = str(d2['author1last'].values[0]) + 'et al.' + str(d2['pubyr'].values[0]) + "." + str(d2['reftitle'].values[0]) if d2['doi'].isnull().values[0] else str(d2['author1last'].values[0]) + 'et al.' + str(d2['pubyr'].values[0])
    result['DOI'] = d2['doi']
    result['title'] = d2['reftitle']
print(result)
result.to_csv("恐龙数据库.csv")










