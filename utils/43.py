import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
data = pd.read_csv('sorted1.csv', encoding='utf-8')
sns.set_theme(style="whitegrid")
rating_counts = data['表面评分数']
delta = data['表面标准差']
plt.figure(figsize=(12, 8))
sns.scatterplot(x=delta, y=rating_counts, marker='o', alpha=0.7, color='blue')
max_rating_count = data.loc[data['表面评分数'].idxmax()]
min_rating_count = data.loc[data['表面评分数'].idxmin()]
max_delta = data.loc[data['表面标准差'].idxmax()]
min_delta = data.loc[data['表面标准差'].idxmin()]
plt.scatter(x=max_rating_count['表面标准差'], y=max_rating_count['表面评分数'], color='red', s=100, label=f'Max Surface Ratings Count: {max_rating_count["表面评分数"]}')
plt.scatter(x=min_rating_count['表面标准差'], y=min_rating_count['表面评分数'], color='green', s=100, label=f'Min Surface Ratings Count: {min_rating_count["表面评分数"]}')
plt.scatter(x=max_delta['表面标准差'], y=max_delta['表面评分数'], color='orange', s=100, label=f'Max Delta: {max_delta["表面标准差"]}')
plt.scatter(x=min_delta['表面标准差'], y=min_delta['表面评分数'], color='purple', s=100, label=f'Min Delta: {min_delta["表面标准差"]}')
plt.title('Surface Ratings Count vs Delta', fontsize=16)
plt.xlabel('Delta', fontsize=14)
plt.ylabel('Surface Ratings Count', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True)
plt.show()
