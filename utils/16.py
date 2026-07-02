import pandas as pd
df = pd.read_csv("sorted1.csv", encoding="utf-8-sig")
s1 = df.iloc[:, 126:126+10*8:8]
s2 = df.iloc[:, 205:205+10*7:7]
w = [10,9,8,7,6,5,4,3,2,1]
wa1 = (s1 * w).sum(axis=1) / s1.sum(axis=1)
wa2 = (s2 * w).sum(axis=1) / s2.sum(axis=1)
df['收藏1000+评分'] = wa1
df['注册大于3年评分'] = wa2
df = df.dropna()
df = df[df.iloc[:, 1] == 2]
df = df[df['是否被锁定'] != True]
t = [1, 2, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 342, 343, 344]
t.extend(range(20, 341))
ctdrop = [df.columns[i] for i in t]
df = df.drop(columns=ctdrop, errors='ignore')
df['收藏1000+排名'] = df['收藏1000+评分'].rank(ascending=False, method='min').astype(int)
df['注册大于3年排名'] = df['注册大于3年评分'].rank(ascending=False, method='min').astype(int)
df.to_csv("s.csv", index=False, encoding="utf-8-sig")
