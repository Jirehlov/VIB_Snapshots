import pandas as pd
from datetime import datetime, timedelta
df1 = pd.read_csv('sorted1.csv', encoding='utf-8-sig').set_index('subject')
df2 = pd.read_csv('sorted4.csv', encoding='utf-8-sig').set_index('subject')
df1['更新时间'] = pd.to_datetime(df1['更新时间'], format='%Y-%m-%dT%H:%M:%SZ')
df2['更新时间'] = pd.to_datetime(df2['更新时间'], format='%Y-%m-%dT%H:%M:%SZ')
column_to_compare = '在'
common_subjects = df1.index.intersection(df2.index)
valid_subjects = [
    subject for subject in common_subjects
    if abs(df1.at[subject, '更新时间'] - df2.at[subject, '更新时间']) <= timedelta(days=10)
]
df1_common = df1.loc[valid_subjects].copy()
df2_common = df2.loc[valid_subjects].copy()
df1_common[column_to_compare] = pd.to_numeric(df1_common[column_to_compare], errors='coerce').fillna(0)
df2_common[column_to_compare] = pd.to_numeric(df2_common[column_to_compare], errors='coerce').fillna(0)
df1_common['diff'] = df1_common[column_to_compare] - df2_common[column_to_compare]
filtered_df = df1_common[df1_common['类型'] == 2]
with open('watching.txt', 'w', encoding='utf-8') as f:
    f.write(f'在看人数变化：\n')
    for index, row in filtered_df[filtered_df['diff'] > 5].sort_values('diff', ascending=False).iterrows():
        f.write(f"{index}, {row['中文标题']}, {row[column_to_compare]} - {df2_common.loc[index, column_to_compare]} = {int(row['diff']):+d}\n")
    f.write('...\n')
    for index, row in filtered_df[filtered_df['diff'] < -5].sort_values('diff', ascending=False).iterrows():
        f.write(f"{index}, {row['中文标题']}, {row[column_to_compare]} - {df2_common.loc[index, column_to_compare]} = {int(row['diff']):+d}\n")
    f.write('\n\n\n')
    total_sum_diff = filtered_df[column_to_compare].sum() - df2_common.loc[filtered_df.index, column_to_compare].sum()
    f.write(f"\n在看总变化：{filtered_df[column_to_compare].sum()} - {df2_common.loc[filtered_df.index, column_to_compare].sum()} = {total_sum_diff:+d}\n")
