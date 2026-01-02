import json
import re
def load_jsonlines(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return [json.loads(line.strip()) for line in f]
def person_satisfies_conditions(person_positions, required, either_or):
    if required and not required.issubset(person_positions): return False
    if any(group and not (person_positions & group) for group in either_or): return False
    return True
def extract_name(d):
    m = re.search(r'\|简体中文名= ([^\r\n]+)', d.get('infobox', ''))
    return m.group(1) if m else d.get('name_cn', d.get('name', ''))
def find_matching_person_ids(data, required, either_or):
    person_positions_map = {}
    for record in data:
        person_positions_map.setdefault(record['person_id'], set()).add(record['position'])
    return [pid for pid, positions in person_positions_map.items() if person_satisfies_conditions(positions, required, either_or)]
subject_persons_file = 'subject-persons.jsonlines'
persons_file = 'person.jsonlines'
subject_data = load_jsonlines(subject_persons_file)
persons_data = {person['id']: person for person in load_jsonlines(persons_file)}
required_positions = {2, 3, 6}
either_or_groups = [{4, 5}, {7, 8}]
matching_person_ids = find_matching_person_ids(subject_data, required_positions, either_or_groups)
matching_person_ids.sort()
for person_id in matching_person_ids:
    person_info = persons_data.get(person_id, {})
    person_name = extract_name(person_info)
    print(f"{person_id}: {person_name}")
