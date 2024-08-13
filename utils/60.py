import pandas as pd
import matplotlib.pyplot as plt
df1 = pd.read_csv('sorted1.csv', encoding='utf-8-sig').set_index('subject')
df2 = pd.read_csv('sorted3.csv', encoding='utf-8-sig').set_index('subject')
columns_to_compare = [f'tc{i}' for i in range(1, 74, 8)]
df1[columns_to_compare] = df1[columns_to_compare].apply(pd.to_numeric, errors='coerce').fillna(0)
df2[columns_to_compare] = df2[columns_to_compare].apply(pd.to_numeric, errors='coerce').fillna(0)
df1['total_change'] = df1[columns_to_compare].sum(axis=1)
df2['total_change'] = df2[columns_to_compare].sum(axis=1)
df1['total_diff'] = df1['total_change'] - df2['total_change']
with open('hitnrun.txt', 'w', encoding='utf-8') as f:
    df1_filtered_total = df1[abs(df1[f'total_diff']) >= 1].copy()
    top_total = df1_filtered_total.nlargest(10, 'total_diff')
    bottom_total = df1_filtered_total.nsmallest(5, 'total_diff')[::-1]
    f.write('总变化：\n')
    for index, row in top_total.iterrows():
        f.write(f"{index}, {row['类型']}, {row['中文标题']}, {row['total_change']} - {df2.loc[index, 'total_change']} = {int(row['total_diff']):+d}\n")
    f.write('...\n')
    for index, row in bottom_total.iterrows():
        f.write(f"{index}, {row['类型']}, {row['中文标题']}, {row['total_change']} - {df2.loc[index, 'total_change']} = {int(row['total_diff']):+d}\n")
    f.write('\n\n\n')
    score_counter = 10
    for col in columns_to_compare:
        df1[f'{col}_diff'] = df1[col] - df2[col]
        df1_filtered = df1[abs(df1[f'{col}_diff']) >= 1].copy()
        top_positive = df1_filtered.nlargest(10, f'{col}_diff')
        top_negative = df1_filtered.nsmallest(5, f'{col}_diff')[::-1]
        f.write(f'{col}（{score_counter}分）一击脱离人数变化：\n')
        for index, row in top_positive.iterrows():
            f.write(f"{index}, {row['类型']}, {row['中文标题']}, {row[col]} - {df2.loc[index, col]} = {int(row[f'{col}_diff']):+d}\n")
        f.write('...\n')
        for index, row in top_negative.iterrows():
            f.write(f"{index}, {row['类型']}, {row['中文标题']}, {row[col]} - {df2.loc[index, col]} = {int(row[f'{col}_diff']):+d}\n")
        f.write('\n\n\n')
        score_counter -= 1
    total_sum_diff = df1[columns_to_compare].sum().sum() - df2[columns_to_compare].sum().sum()
    f.write(f'\n一击脱离评分点位总和变化：{df1[columns_to_compare].sum().sum()} - {df2[columns_to_compare].sum().sum()} = {total_sum_diff:+d}\n')
