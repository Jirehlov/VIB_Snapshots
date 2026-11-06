import json
import csv
type_counts = {t: {'json': 0, 'csv': 0} for t in ['1', '2', '3', '4', '6']}
types = ['书籍', '动画', '音乐', '游戏', '', '三次元']
with open('subject.jsonlines', 'r', encoding='utf-8') as file:
    for line in file:
        data = json.loads(line)
        type_str = str(data.get('type'))
        if data.get('rank') > 0 and type_str in type_counts:
            type_counts[type_str]['json'] += 1
with open('sorted1.csv', 'r', encoding='utf-8-sig') as file:
    next(file)
    for row in csv.reader(file):
        type_str = row[1].strip()
        rank = float(row[-1].strip())
        if int(rank) > 0 and type_str in type_counts:
            type_counts[type_str]['csv'] += 1
total_json = total_csv = 0
print("VIB条目命中比例:")
for t, counts in type_counts.items():
    total_json += counts['json']
    total_csv += counts['csv']
    ratio = 100.0 * counts['csv'] / counts['json'] if counts['json'] else 0
    print(f"{types[int(t)-1]}: 表面评分条目数: {counts['json']}, VIB条目数: {counts['csv']}, 占比: {ratio:.3f}%")
overall_ratio = 100.0 * total_csv / total_json if total_json else 0
print(f"总计：表面评分条目数 {total_json}, VIB条目数: {total_csv}, 总占比: {overall_ratio:.3f}%")
