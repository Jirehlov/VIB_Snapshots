import json
import csv
type_counts = {t: {'json': 0, 'csv': 0} for t in ['1', '2', '3', '4', '6']}
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
        if type_str in type_counts:
            type_counts[type_str]['csv'] += 1
total_json = total_csv = 0
print("Counts and ratios by type:")
for t, counts in type_counts.items():
    count_json, count_csv = counts['json'], counts['csv']
    total_json += count_json
    total_csv += count_csv
    ratio = 100.0 * count_csv / count_json if count_json else 0
    print(f"Type {t}: JSON count: {count_json}, CSV count: {count_csv}, Ratio: {ratio:.3f}%")
overall_ratio = 100.0 * total_csv / total_json if total_json else 0
print(f"\nOverall counts and ratio:\nTotal JSON count: {total_json}\nTotal CSV count: {total_csv}\nOverall ratio: {overall_ratio:.3f}%")
