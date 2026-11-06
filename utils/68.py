import json
import argparse
from collections import defaultdict
parser = argparse.ArgumentParser(description='Process subject data.')
parser.add_argument('-t', type=int, default=20, help='Number of top subjects to display.')
parser.add_argument('-p', type=int, nargs='+', help='Positions to filter subjects (can provide multiple positions).')
args = parser.parse_args()
subject_counts = defaultdict(int)
with open('subject-persons.jsonlines', 'r') as f:
    for line in f:
        data = json.loads(line)
        if not args.p or data['position'] in args.p:
            subject_counts[data['subject_id']] += 1
with open('subject.jsonlines', 'r', encoding='utf-8') as f:
    subject_names = {data['id']: data.get('name_cn', data.get('name', "?")) for data in map(json.loads, f)}
for subject_id, count in sorted(subject_counts.items(), key=lambda x: x[1], reverse=True)[:args.t]:
    print(f"{subject_id}, {subject_names.get(subject_id, '?')}, {count}")
