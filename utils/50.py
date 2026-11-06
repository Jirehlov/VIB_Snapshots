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
num_groups = (total_ids + 29999) // 30000
labels = np.concatenate([np.full(30000, i) for i in range(num_groups)])[:total_ids]
np.random.shuffle(labels)
new_df = pd.DataFrame({
    'subject_id': remaining_ids,
    'count': labels
})
new_df.to_csv('randomed_skip_counts.csv', index=False)
