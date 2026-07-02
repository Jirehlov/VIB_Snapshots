import sys
import json
input_array = list(map(int, sys.argv[1].strip("[]").split(",")))
subject_data = {}
with open('subject.jsonlines', 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line.strip())
        subject_data[data['id']] = {
            'name_cn': data.get('name_cn'),
            'name': data.get('name'),
            'type': data.get('type'),
            'score_details': data.get('score_details', {})
        }
for id in input_array:
    if id in subject_data:
        info = subject_data[id]
        showname = info['name_cn'] or info['name'] or 'N/A'
        score_sum = sum(info['score_details'].values())
        if score_sum < 5:
            stars = "★" * (5 - score_sum)
        else:
            stars = "★" * (score_sum // 100)
        print(f"{id}, {info['type']}, {showname}, {score_sum} {stars}")
    else:
        print(f"{id} 没有找到喔～ (´；ω；`)")
