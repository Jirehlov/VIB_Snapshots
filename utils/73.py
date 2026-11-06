import json
import re
import csv
pattern = re.compile(r'^[\u3040-\u30FF\uFF66-\uFF9F0-9A-Za-z\u4E00-\u9FFF\uAC00-\uD7AF\u0400-\u04FF\uFF21-\uFF3A\uFF41-\uFF5A\u0370-\u03FF\uFF10-\uFF19\u3400-\u4DBF\u20000-\u2A6DF\uF900-\uFAFF]')
blocklist = ['【','「','&','-','～','〜','#','(','[','{','〈','〔','《','“','"','\'','『','/','＜','=','≠','［','（','?','!','+','÷','☆','♡','…','.','－']
output_data = []
with open('episode.jsonlines', 'r', encoding='utf-8') as file:
    for line in file:
        data = json.loads(line)
        name = data.get('name', '')
        if not name or pattern.match(name) or name[0] in blocklist:
            continue
        unicode_value = ord(name[0])
        output_data.append({
            'ID': data.get('id'),
            'Name': name,
            'Unicode': unicode_value
        })
output_data.sort(key=lambda x: x['Unicode'])
with open('anomaly_ep.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['ID', 'Name', 'Unicode'])
    for row in output_data:
        csvwriter.writerow([row['ID'], row['Name'], f"U+{row['Unicode']:04X}"])
