import csv
import json
input_file = "subject-relations.jsonlines"
csv_file = "sorted1.csv"
output_file = "out.csv"
subject_types = {}
with open(csv_file, "r", encoding="utf-8-sig") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        subject_id = row[0].strip()
        vib_type = row[1].strip()
        vib_score = row[4].strip()
        score = sum((i+1)*int(row[20+i].strip()) for i in range(10)) / int(row[18].strip())
        name_cn = row[3].strip()
        subject_types[f'"{subject_id}"'] = (vib_type, vib_score, score, name_cn)
with open(output_file, "w", encoding="utf-8-sig", newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(["subject_id", "subject_name", "related_subject_id", "related_subject_name", "vib_score_diff", "score_diff"])
    with open(input_file, "r", encoding="utf-8") as infile:
        for line in infile:
            try:
                data = json.loads(line)
                subject_id = data.get("subject_id")
                v = subject_types.get(f'"{subject_id}"')
                if v and v[0] == "2" and data.get("relation_type") == 3:
                    related_subject_id = data.get("related_subject_id")
                    related_v = subject_types.get(f'"{related_subject_id}"')
                    if related_v:
                        vib_score_diff =  float(related_v[1]) - float(v[1])
                        score_diff =  float(related_v[2]) - float(v[2])
                        v_name = v[3]
                        related_v_name = related_v[3]
                        writer.writerow([subject_id, v_name, related_subject_id, related_v_name, vib_score_diff, score_diff])
            except json.JSONDecodeError:
                continue
