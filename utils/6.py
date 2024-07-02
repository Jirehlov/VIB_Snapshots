import csv
import numpy as np
import pandas as pd
left_weight = 5 # 低分权重
right_weight = 80 # 高分权重
threshold = 1.0 # 标准差阈值
header_line = ["subject", "类型", "标题", "中文标题", "VIB评分", "VIB标准差", "VIB评分数", "1.1", "2.1", "3.1", "4.1", "5.1", "6.1", "7.1", "8.1", "9.1", "10.1", "表面排名", "表面评分数", "表面评分", "1.2", "2.2", "3.2", "4.2", "5.2", "6.2", "7.2", "8.2", "9.2", "10.2", "是否被锁定", "发布发售放送时间", "NSFW", "子类型", "搁置", "抛弃", "想", "已", "在", "更新时间","VIB朴素排名","类型内VIB总平均分","类型内前250的最小VIB评分数","类型内加权VIB平均分","VIB加权排名（最终）","修正分数"]
df = pd.DataFrame(columns=header_line)
with open('sorted1.csv', mode='r', encoding='utf-8') as input_file:
    csv_reader = csv.reader(input_file)
    next(csv_reader, None)
    for row in csv_reader:
        data_str = row[7:17]
        data = [int(item) for item in data_str]
        while True:
            scores = []
            for i, count in enumerate(data):
                scores.extend([i + 1] * count)
            if np.std(scores) < threshold:
                break
            left_idx = 0
            while data[left_idx] == 0:
                left_idx += 1
            right_idx = len(data) - 1
            while data[right_idx] == 0:
                right_idx -= 1
            data[left_idx] -= round(left_weight/(left_idx+1))
            if data[left_idx] < 0:
                data[left_idx] = 0
            data[right_idx] -= round(right_weight/(right_idx+1))
            if data[right_idx] < 0:
                data[right_idx] = 0
        average_score = np.mean(scores)
        row.append(average_score)
        df.loc[len(df)] = row
locked_items = df[df['是否被锁定'] == "True"].copy()
locked_items['修正排名'] = 0
unlocked_items = df[df['是否被锁定'] != "True"].copy()
unlocked_items.sort_values(by=['类型', '修正分数'], ascending=[True, False], inplace=True)
unlocked_items['修正排名'] = unlocked_items.groupby('类型').cumcount() + 1
result_df = pd.concat([locked_items, unlocked_items])
result_df.to_csv('output.csv', index=False, encoding='utf-8')
print("处理完成，结果已写入output.csv文件。")
