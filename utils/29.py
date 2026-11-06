import pandas as pd
import matplotlib.pyplot as plt
import os
skip_counts = pd.read_csv(os.path.expandvars('%USERPROFILE%\\Documents\\GitHub\\VIB_Snapshots\\server_backup\\skip_counts.csv'))['subject_id'].value_counts().groupby(lambda x: x // 10000).sum()
sorted_counts = pd.read_csv('sorted1.csv', encoding="utf-8-sig")['subject'].value_counts().groupby(lambda x: x // 10000).sum()
max_subject_id = max(pd.read_csv(os.path.expandvars('%USERPROFILE%\\Documents\\GitHub\\VIB_Snapshots\\server_backup\\skip_counts.csv'))['subject_id'].max(), pd.read_csv('sorted1.csv', encoding="utf-8-sig")['subject'].max())
total_range = max_subject_id // 10000
skip_values = skip_counts.reindex(range(total_range + 1), fill_value=0)
sorted_values = sorted_counts.reindex(range(total_range + 1), fill_value=0)
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.bar(range(total_range + 1), skip_values, color='blue', label='skip')
plt.bar(range(total_range + 1), sorted_values, bottom=skip_values, color='orange', label='sorted')
plt.title('Distribution of subject_id (Bar)')
plt.xlabel('subject_id / 10000')
plt.ylabel('Count')
plt.legend()
plt.ylim(0, 10000)
plt.subplot(1, 2, 2)
total_skip = skip_values.sum()
total_sorted = sorted_values.sum()
total_other = max(0, max_subject_id - total_skip - total_sorted)
sizes = [total_skip, total_sorted, total_other]
labels = ['Skip', 'Sorted', 'Processing']
colors = ['blue', 'orange', 'green']
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
plt.axis('equal')
plt.title('Distribution of subject_id (Pie)')
plt.tight_layout()
plt.savefig("distribution.png")
plt.show()
