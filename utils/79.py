import sys, json
def compare_ids(json_file):
    input_ids = {item['subject_id'] for item in json.load(open(json_file, 'r', encoding='utf-8')) if 'subject_id' in item}
    subject_ids = {json.loads(line.strip())['id'] for line in open('subject.jsonlines', 'r', encoding='utf-8') if 'id' in json.loads(line.strip())}
    for diff_id in input_ids - subject_ids:
        print(f"https://bgm.tv/subject/{diff_id}")
if __name__ == "__main__":
    compare_ids(sys.argv[1]) if len(sys.argv) == 2 else print("Usage: python 79.py <json_file>")
