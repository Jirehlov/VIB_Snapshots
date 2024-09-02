import pandas as pd
df1 = pd.read_csv('sorted1.csv', encoding='utf-8-sig').set_index('subject')
df2 = pd.read_csv('sorted4.csv', encoding='utf-8-sig').set_index('subject')
column_to_compare = '在'
common_subjects = df1.index.intersection(df2.index)
df1_common = df1.loc[common_subjects]
df2_common = df2.loc[common_subjects]
df1_common[column_to_compare] = pd.to_numeric(df1_common[column_to_compare], errors='coerce').fillna(0)
df2_common[column_to_compare] = pd.to_numeric(df2_common[column_to_compare], errors='coerce').fillna(0)
df1_common['diff'] = df1_common[column_to_compare] - df2_common[column_to_compare]
filtered_df = df1_common[(df1_common['类型'] == 2)]
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
