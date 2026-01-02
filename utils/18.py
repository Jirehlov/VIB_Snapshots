import os
import csv
from datetime import datetime
import matplotlib.pyplot as plt
input_ids = input("请输入subject(s)_id：")
subject_ids = [s.strip() for s in input_ids.split(',') if s.strip()]
csv_directory = os.path.expandvars(r'%USERPROFILE%\Documents\GitHub\VIB_Snapshots')
font_path = os.path.expandvars(r'%LocalAppData%\Microsoft\Windows\Fonts\DFHannotateW7-A.ttf')
plt.rcParams['font.family'] = 'DFHannotateW7-A'
plt.rcParams['font.size'] = 12
subject_data = {sid: [] for sid in subject_ids}
subject_titles = {sid: sid for sid in subject_ids}
for file_name in os.listdir(csv_directory):
    if file_name.startswith('sorted_') and file_name.endswith('.csv'):
        file_path = os.path.join(csv_directory, file_name)
        with open(file_path, 'r', encoding='utf-8-sig') as csv_file:
            csv_reader = csv.reader(csv_file)
            try:
                headers = next(csv_reader)
            except StopIteration:
                continue
            try:
                idx_title = headers.index('中文标题')
                idx_update = headers.index('更新时间')
                idx_vib = headers.index('VIB评分')
            except ValueError:
                continue
            for row in csv_reader:
                current_id = row[0].strip()
                if current_id in subject_ids:
                    if subject_titles[current_id] == current_id and row[idx_title].strip():
                        subject_titles[current_id] = row[idx_title].strip()
                    try:
                        update_time = datetime.strptime(row[idx_update].strip(), "%Y-%m-%dT%H:%M:%SZ")
                        vib_score = float(row[idx_vib].strip())
                    except Exception:
                        continue
                    subject_data[current_id].append((update_time, vib_score))
plt.figure(figsize=(10, 6))
for sid in subject_ids:
    data = subject_data[sid]
    if data:
        sorted_data = sorted(data, key=lambda x: x[0])
        update_times, vib_scores = zip(*sorted_data)
        plt.plot(update_times, vib_scores, marker='o', label=subject_titles[sid])
    else:
        print(f"没有找到 subject id {sid} 的数据。")
plt.xlabel('更新时间')
plt.ylabel('VIB评分')
plt.title('VIB评分随时间变化图')
plt.legend()
plt.show()
