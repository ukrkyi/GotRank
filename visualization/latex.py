import glob
import pandas as pd


path = 'tables'

files = [f for f in glob.glob(path + "**/*.csv", recursive=True)]



dataframes  = [pd.read_csv(i) for  i in files]
dicts = []
for i in dataframes:
    i  = i.to_dict()
    newd = {}
    for j in i['name']:
        newd[i['name'][j]] = j
    dicts.append(newd)

res = {}
for i in dicts[0]:
    res[i] = 0
    for j in dicts:
        res[i] += j[i]

print(min(res, key=lambda x: res[x]))
del res[min(res, key=lambda x: res[x])]

print(min(res, key=lambda x: res[x]))
del res[min(res, key=lambda x: res[x])]

print(min(res, key=lambda x: res[x]))
del res[min(res, key=lambda x: res[x])]


# for i in dataframes:
#     print(i.to_latex(column_format='|l|c|r|', longtable=True, multicolumn=True, multirow=True))