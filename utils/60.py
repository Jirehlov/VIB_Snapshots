import pandas as pd
from datetime import timedelta
import argparse
parser = argparse.ArgumentParser(description="比较两个 CSV 文件中的一击脱离变化")
parser.add_argument("csv1")
parser.add_argument("csv2")
parser.add_argument("-k", "--keep-all", action="store_true", help="保留所有交集 subject，不筛选更新时间间隔")
args = parser.parse_args()
df1 = pd.read_csv(args.csv1, encoding='utf-8-sig').set_index('subject')
df2 = pd.read_csv(args.csv2, encoding='utf-8-sig').set_index('subject')
df1['更新时间'] = pd.to_datetime(df1['更新时间'])
df2['更新时间'] = pd.to_datetime(df2['更新时间'])
columns_to_compare = [f'tc{i}' for i in range(1, 74, 8)]
df1[columns_to_compare] = df1[columns_to_compare].apply(pd.to_numeric, errors='coerce').fillna(0)
df2[columns_to_compare] = df2[columns_to_compare].apply(pd.to_numeric, errors='coerce').fillna(0)
if args.keep_all:
    valid_subjects = df1.index.intersection(df2.index)
else:
    valid_subjects = [
        subject for subject in df1.index.intersection(df2.index)
        if abs(df1.at[subject, '更新时间'] - df2.at[subject, '更新时间']) <= timedelta(days=10)
    ]
df1, df2 = df1.loc[valid_subjects], df2.loc[valid_subjects]
df1['total_change'] = df1[columns_to_compare].sum(axis=1)
df2['total_change'] = df2[columns_to_compare].sum(axis=1)
df1['total_diff'] = df1['total_change'] - df2['total_change']
df1_filtered_total = df1[abs(df1['total_diff']) >= 1].sort_values('total_diff', ascending=False)
with open('hitnrun.txt', 'w', encoding='utf-8') as f:
    f.write("总变化：\n")
    for subset, label in [(df1_filtered_total.head(10), 'top'), (df1_filtered_total.tail(len(df1_filtered_total[df1_filtered_total['total_diff'] < 0]) + 1), 'bottom')]:
        for index, row in subset.iterrows():
            f.write(f"{index}, {row['类型']}, {row['中文标题']}, {row['total_change']} - {df2.loc[index, 'total_change']} = {int(row['total_diff']):+d}\n")
        f.write('...\n' if label == 'top' else '\n\n\n')
    score_counter = 10
    for col in columns_to_compare:
        df1[f'{col}_diff'] = df1[col] - df2[col]
        df1_filtered = df1[abs(df1[f'{col}_diff']) >= 1]
        for subset, label in [(df1_filtered.nlargest(10, f'{col}_diff'), 'top'), (df1_filtered.nsmallest(5, f'{col}_diff')[::-1], 'bottom')]:
            if label == 'top':
                f.write(f'{col}（{score_counter}分）一击脱离人数变化：\n')
            for index, row in subset.iterrows():
                f.write(f"{index}, {row['类型']}, {row['中文标题']}, {row[col]} - {df2.loc[index, col]} = {int(row[f'{col}_diff']):+d}\n")
            f.write('...\n' if label == 'top' else '\n\n\n')
        score_counter -= 1
    total_sum_diff = df1[columns_to_compare].sum().sum() - df2[columns_to_compare].sum().sum()
    f.write(f'\n一击脱离评分点位总和变化：{df1[columns_to_compare].sum().sum()} - {df2[columns_to_compare].sum().sum()} = {total_sum_diff:+d}\n')
