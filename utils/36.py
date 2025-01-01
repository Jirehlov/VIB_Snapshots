import json
import csv
subject_data = {}
with open('subject.jsonlines', 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line.strip())
        subject_data[data['id']] = {'rank': data['rank'], 'score_details': data['score_details'], 'type': data['type']}
sorted_ids = []
with open('sorted1.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        sorted_ids.append(int(row[0]))
missing_ids = [id for id in subject_data if id not in sorted_ids]
with open('missing_ids_with_rank.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'type', 'rank', 'score_sum'])
    for id in missing_ids:
        score_sum = sum(subject_data[id]['score_details'].values())
        writer.writerow([id, subject_data[id]['type'], subject_data[id]['rank'], score_sum])
print("完成！结果已保存到 missing_ids_with_rank.csv")
