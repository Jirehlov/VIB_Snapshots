import json
import re
import argparse
from collections import defaultdict
import csv
def get_subject_ids(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    subject_ids = [item['subject_id'] for item in json_data if item['subject_type'] == 2 and item['collection_type'] == 2]
    return subject_ids
def load_person_names(jsonlines_file):
    person_info = {}
    pattern = re.compile(r'\|简体中文名= *(.*?)\r\n\|')
    with open(jsonlines_file, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            person_id = data['id']
            name = data['name']
            infobox = data.get('infobox', '')
            match = pattern.search(infobox)
            chinese_name = match.group(1) if match else None
            person_info[person_id] = {
                'name': name,
                'chinese_name': chinese_name
            }
    return person_info
def count_person_hits(subject_ids, jsonlines_file, person_info, mode):
    person_hits = defaultdict(int)
    with open(jsonlines_file, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            if data['subject_id'] in subject_ids:
                person_hits[data['person_id']] += 1
    sorted_hits = sorted(person_hits.items(), key=lambda x: x[1], reverse=True)
    print("姓名, 简体中文名, 命中")
    for person_id, hits in sorted_hits[:25]:
        if person_id in person_info:
            name = person_info[person_id]['name']
            chinese_name = person_info[person_id]['chinese_name'] or ''
            print(f"{name}, {chinese_name}, {hits}")
    output_file = 'cv_hits.csv' if mode == 1 else 'staff_hits.csv'
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["姓名", "简体中文名", "命中"])
        for person_id, hits in sorted_hits:
            if person_id in person_info:
                name = person_info[person_id]['name']
                chinese_name = person_info[person_id]['chinese_name'] or ''
                writer.writerow([name, chinese_name, hits])
def main(json_file, jsonlines_file, mode):
    subject_ids = get_subject_ids(json_file)
    person_info = load_person_names('person.jsonlines')
    count_person_hits(subject_ids, jsonlines_file, person_info, mode)
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='统计用户看过动画命中的制作人员或声优。请先运行32.py获取用户收藏JSON，运行45.py获取官方Archive。')
    parser.add_argument('json_file', type=str, nargs='?', help='JSON文件路径')
    parser.add_argument('mode', type=int, choices=[1, 2], nargs='?', help='选择统计模式: 1-声优统计, 2-制作人员统计')
    args = parser.parse_args()
    if args.json_file is None or args.mode is None:
        json_file = input('请输入JSON文件路径: ')
        mode = int(input('请选择统计模式 (1-声优统计, 2-制作人员统计): '))
    else:
        json_file = args.json_file
        mode = args.mode
    jsonlines_file = 'person-characters.jsonlines' if mode == 1 else 'subject-persons.jsonlines'
    main(json_file, jsonlines_file, mode)
