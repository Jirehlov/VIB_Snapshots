import os
import csv
from datetime import datetime
import matplotlib.pyplot as plt
target_subject = input("请输入目标主题：")
csv_directory = os.path.expandvars('%USERPROFILE%\\Documents\\GitHub\\VIB_Snapshots\\')
font_path = os.path.expandvars('%LocalAppData%\\Microsoft\\Windows\\Fonts\\DFHannotateW7-A.ttf')
plt.rcParams['font.family'] = 'DFHannotateW7-A'
plt.rcParams['font.size'] = 12
subject_title = ''
for file_name in os.listdir(csv_directory):
    if file_name.startswith('sorted_') and file_name.endswith('.csv'):
        with open(os.path.join(csv_directory, file_name), 'r', encoding='utf-8-sig') as csv_file:
            csv_reader = csv.reader(csv_file)
            headers = next(csv_reader)
            for row in csv_reader:
                if row[0] == target_subject:
                    subject_title = row[headers.index('中文标题')]
                    break
data = [(datetime.strptime(row[header.index('更新时间')], "%Y-%m-%dT%H:%M:%SZ"), float(row[header.index('VIB评分')])) for file_name in os.listdir(csv_directory) if file_name.startswith('sorted_') and file_name.endswith('.csv') for row in csv.reader(open(os.path.join(csv_directory, file_name), 'r', encoding='utf-8')) if row[0] == target_subject for header in [next(csv.reader(open(os.path.join(csv_directory, file_name), 'r', encoding='utf-8-sig')))]]
sorted_data = sorted(data, key=lambda x: x[0])
update_times, vib_scores = zip(*sorted_data)
plt.plot(update_times, vib_scores)
plt.xlabel('更新时间')
plt.ylabel('VIB评分')
plt.title(f'{subject_title} VIB评分随时间变化图')
plt.show()
