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
column_sums = [[] for _ in range(10)]
for file_index, csv_file in tqdm(csv_files, desc="Processing files", unit="file"):
    file_path = os.path.join(directory, csv_file)
    df = pd.read_csv(file_path)
    for col_idx in range(7, 17):
        numeric_column = pd.to_numeric(df.iloc[:, col_idx], errors='coerce')
        column_sums[col_idx - 7].append(numeric_column.sum())
plt.figure(figsize=(12, 6))
colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'cyan', 'magenta']
for i, col_sum in enumerate(column_sums):
    plt.plot(col_sum, marker='o', linestyle='-', color=colors[i], label=str(i+1))
plt.legend()
plt.xticks([])
plt.yscale('log')
plt.tight_layout()
plt.savefig('all_sums.png')
plt.close()
