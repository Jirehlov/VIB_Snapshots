import pandas as pd
import os
out_path = 'output.txt'
in_path1 = 'sorted1.csv'
in_path2 = 'sorted2.csv'
if os.path.exists(out_path):
    os.remove(out_path)
def w(str):
    with open(out_path, 'a', encoding='utf-8') as file:
        file.write(str)
def c(DataFrame):
    DataFrame.to_csv(out_path, sep='\t', index=False, mode='a')
def s(str1, str2, str3, str4):
    m2[str1] = (m2[str2 + '_x'] - m2[str2 + '_y'])
    if str1 == '排名变化': m2[str1] = -m2[str1]
    sorted1 = m2.sort_values(by=str1, ascending=False)
    if str1 == '评分变化':
        sorted1[str1] = sorted1[str1].apply(lambda x: f'{x:+.8f}')
    else:
        sorted1[str1] = sorted1[str1].apply(lambda x: f'{int(x):+d}')
    w(str3)
    c(sorted1.head(15)[['subject', '中文标题', str1]])
    w(str4)
    c(sorted1.tail(15)[['subject', '中文标题', str1]][::-1])
df1 = pd.read_csv(in_path1)
df2 = pd.read_csv(in_path2)
mfull = pd.merge(df1, df2, on='subject', how='outer')
mfull.rename(columns={'中文标题_x': '中文标题'}, inplace=True)
df1 = df1[df1['类型'] == 2]
df2 = df2[df2['类型'] == 2]
m2 = pd.merge(df1, df2, on='subject', how='outer')
m2.rename(columns={'中文标题_x': '中文标题'}, inplace=True)
new = df1[~df1['subject'].isin(df2['subject'])]
new.loc[:, 'VIB评分'] = new['VIB评分'].round(8)
new = new[['subject', '中文标题', 'VIB评分', 'VIB朴素排名', 'VIB加权排名']]
w("新增条目如下，\n")
c(new)
m2 = m2[m2['VIB朴素排名_y'].notna()]
z = mfull[(mfull['VIB朴素排名_x'] == 0) & (mfull['VIB朴素排名_y'] != 0)]
if not z.empty:
    m2 = m2[~m2['subject'].isin(z['subject'])]
s('排名变化', 'VIB朴素排名', "\n\n对于已有的条目，朴素排名增加的最多的15个是，\n", "\n\n朴素排名减少的最多的15个是，\n")
s('排名变化', 'VIB加权排名', "\n\n加权排名增加的最多的15个是，\n", "\n\n加权排名减少的最多的15个是，\n")
s('评分变化', 'VIB评分', "\n\n评分增加的最多的15个是，\n", "\n\n评分减少的最多的15个是，\n")
s('评分人数变化', 'VIB评分数', "\n\n评分人数增加的最多的15个是，\n", "\n\n评分人数减少的最多的15个是，\n")
if not z.empty:
    w("\n\n需要特别注意的是，以下条目失去了排名资格：\n")
    c(z[['subject', '中文标题']])
