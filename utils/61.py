import pandas as pd
df = pd.read_csv('sorted1.csv', encoding="utf-8-sig")
df['更新时间'] = pd.to_datetime(df['更新时间'], format='%Y-%m-%dT%H:%M:%SZ')
df_sorted = df.sort_values(by='更新时间')
start, end = None, None
for i in range(len(df_sorted) - 1):
    if df_sorted['subject'].iloc[i] < df_sorted['subject'].iloc[i + 1]:
        if start is None:
            start = i
        end = i + 1
    else:
        start = None
if start is not None:
    print(f"更新时间区间大约是从{df_sorted['更新时间'].iloc[start].strftime('%Y-%m-%dT%H:%M:%SZ')}到{df_sorted['更新时间'].iloc[end].strftime('%Y-%m-%dT%H:%M:%SZ')}")
