import pandas as pd
import numpy as np
import sys
if len(sys.argv) != 2:
    print("Usage: python 50.py <max_subjects>")
    sys.exit(1)
max_subjects = int(sys.argv[1])
df = pd.read_csv('sorted1.csv', encoding="utf-8-sig")
excluded_ids = set(df.iloc[:, 0])
all_ids = set(range(0, max_subjects + 1))
remaining_ids = list(all_ids - excluded_ids)
total_ids = len(remaining_ids)
num_groups = (total_ids // 40000) + 1
labels = np.concatenate([np.full(40000, i) for i in range(num_groups)])[:total_ids]
np.random.shuffle(labels)
max_label = labels.max()
remaining_labels = labels[labels != max_label]
new_labels = np.arange(len(remaining_labels)) // 40000
new_df = pd.DataFrame({
    'subject_id': remaining_ids[:len(remaining_labels)],
    'count': new_labels
})
new_df.to_csv('randomed_skip_counts.csv', index=False)
