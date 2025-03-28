import os
import pandas as pd
import matplotlib.pyplot as plt
import re
from tqdm import tqdm
directory = './year_end_report/2024/'
if not os.path.exists(directory):
    exit()
file_pattern = re.compile(r'sorted_(\d+)\.csv')
csv_files = []
for filename in os.listdir(directory):
    match = file_pattern.match(filename)
    if match:
        csv_files.append((int(match.group(1)), filename))
csv_files.sort()
column_sums = []
file_labels = []
for file_index, csv_file in tqdm(csv_files, desc="Processing files", unit="file"):
    file_path = os.path.join(directory, csv_file)
    df = pd.read_csv(file_path)
    if len(df.columns) > 4:
        numeric_column = pd.to_numeric(df.iloc[:, 4], errors='coerce')
        column_sum = numeric_column.sum()
        column_sums.append(column_sum)
        file_labels.append(csv_file)
plt.figure(figsize=(12, 6))
plt.plot(column_sums, marker='o', linestyle='-')
plt.xticks([])
plt.tight_layout()
plt.savefig('sum.png')
plt.close()
print("sum.png saved.")
