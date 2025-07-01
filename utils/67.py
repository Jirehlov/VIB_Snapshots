import json
import re
import argparse
from collections import defaultdict
import csv
def get_subject_ids(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        return [item['subject_id'] for item in json.load(f) if item['subject_type'] == 2 and item['collection_type'] == 2]
def load_person_names(jsonlines_file):
    person_info = {}
    pattern = re.compile(r'\|简体中文名= *(.*?)\r\n\|')
    with open(jsonlines_file, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            match = pattern.search(data.get('infobox', ''))
            person_info[data['id']] = { 'name': data['name'], 'chinese_name': match.group(1) if match else None }
    return person_info
def count_person_hits(subject_ids, jsonlines_file, person_info, mode):
    person_hits = defaultdict(int)
    with open(jsonlines_file, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            if data['subject_id'] in subject_ids:
                person_hits[data['person_id']] += 1
    output_file = 'cv_hits.csv' if mode == 1 else 'staff_hits.csv'
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(["姓名", "简体中文名", "命中"])
        for person_id, hits in sorted(person_hits.items(), key=lambda x: x[1], reverse=True):
            if person_id in person_info:
                writer.writerow([person_info[person_id]['name'], person_info[person_id]['chinese_name'] or '', hits])
    with open(output_file, 'r', encoding='utf-8-sig') as file:
        [print(', '.join(row)) for i, row in enumerate(csv.reader(file)) if i < 26]
def main(json_file, jsonlines_file, mode):
    subject_ids = get_subject_ids(json_file)
    person_info = load_person_names('person.jsonlines')
    count_person_hits(subject_ids, jsonlines_file, person_info, mode)
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='统计用户看过动画命中的制作人员或声优。请先运行32.py获取用户收藏JSON，运行45.py获取官方Archive。')
    parser.add_argument('json_file', type=str, nargs='?', help='JSON文件路径')
    parser.add_argument('mode', type=int, choices=[1, 2], nargs='?', help='选择统计模式: 1-声优统计, 2-制作人员统计')
    args = parser.parse_args()
    json_file = args.json_file or input('请输入JSON文件路径: ')
    mode = args.mode or int(input('请选择统计模式 (1-声优统计, 2-制作人员统计): '))
    jsonlines_file = 'person-characters.jsonlines' if mode == 1 else 'subject-persons.jsonlines'
    main(json_file, jsonlines_file, mode)
