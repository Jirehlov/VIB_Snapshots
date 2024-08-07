import pandas as pd
df1 = pd.read_csv('sorted1.csv', encoding='utf-8-sig')
df2 = pd.read_csv('sorted3.csv', encoding='utf-8-sig')
columns_to_compare = [f'tc{i}' for i in range(1, 74, 8)]
df1 = df1.set_index('subject')
df2 = df2.set_index('subject')
score_counter = 10
df1_total_sum = 0
df2_total_sum = 0
with open('hitnrun.txt', 'w', encoding='utf-8') as f:
    for col in columns_to_compare:
        df1[col] = pd.to_numeric(df1[col], errors='coerce').fillna(0)
        df2[col] = pd.to_numeric(df2[col], errors='coerce').fillna(0)
        df1[f'{col}_diff'] = df1[col] - df2[col]
        df1_total_sum += df1[col].sum()
        df2_total_sum += df2[col].sum()
        df1_filtered = df1[abs(df1[f'{col}_diff']) >= 1].copy()
        top_positive_changes = df1_filtered.nlargest(10, f'{col}_diff')
        top_negative_changes = df1_filtered.nsmallest(5, f'{col}_diff')[::-1]
        f.write(f'{col}（{score_counter}分）一击脱离人数变化：\n')
        for index, row in top_positive_changes.iterrows():
            f.write(f"{index}, {row['类型']}, {row['中文标题']}, {row[col]} - {df2.loc[index, col]} = {int(row[f'{col}_diff']):+d}\n")
        f.write('...\n')
        for index, row in top_negative_changes.iterrows():
            f.write(f"{index}, {row['类型']}, {row['中文标题']}, {row[col]} - {df2.loc[index, col]} = {int(row[f'{col}_diff']):+d}\n")
        f.write('\n\n\n')
        score_counter -= 1
total_sum_diff = df1_total_sum - df2_total_sum
with open('hitnrun.txt', 'a', encoding='utf-8') as f:
    f.write(f'一击脱离评分点位总和变化：{df1_total_sum} - {df2_total_sum} = {total_sum_diff:+d}\n')
