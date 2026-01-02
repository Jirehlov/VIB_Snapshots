import json, re
def load(file):
    with open(file, 'r', encoding='utf-8') as f:
        return [json.loads(l.strip()) for l in f]
def name(d):
    m = re.search(r'\|简体中文名= ([^\r\n]+)', d.get('infobox', ''))
    return m.group(1) if m else d.get('name_cn', d.get('name', ''))
def count_pos(data):
    pos_map = {}
    for r in data: pos_map.setdefault(r['person_id'], set()).add(r['position'])
    return {pid: len(pos) for pid, pos in pos_map.items()}
subject_data = load('subject-persons.jsonlines')
persons = {p['id']: p for p in load('person.jsonlines')}
chars = {r['person_id'] for r in load('person-characters.jsonlines')}
pos_count = count_pos(subject_data)
for pid in pos_count: 
    if pid in chars: pos_count[pid] += 1
top = sorted((i for i in pos_count.items() if i[1] > 19), key=lambda x: x[1], reverse=True)
print("person_id: 人物姓名, 职位数量")
for pid, count in top:
    print(f"{pid}: {name(persons.get(pid, {}))}, {count}")
