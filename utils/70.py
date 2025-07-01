import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import os
data = pd.read_csv(os.path.expandvars('%USERPROFILE%\\Documents\\GitHub\\VIB_Snapshots\\server_backup\\skip_counts.csv'))
min_id, max_id = data['subject_id'].min(), data['subject_id'].max()
size = max_id - min_id + 1
side_length = math.ceil(math.sqrt(size))
colors = np.zeros((side_length * side_length, 3), dtype=np.uint8)
for _, row in data.iterrows():
    index = row['subject_id'] - min_id
    count = row['count']
    if 0 <= count <= 12:
        red_value = int((count / 12) * 255)
        colors[index] = [red_value, 0, 0]
colors = colors.reshape(side_length, side_length, 3)
plt.imsave('70.png', colors)
