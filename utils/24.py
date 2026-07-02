import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
data = pd.read_csv('sorted1.csv', encoding='utf-8-sig')
sns.set_theme(style="whitegrid")
vib_scores = data['VIB评分']
ratings_count = data['VIB评分数']
plt.figure(figsize=(12, 8))
sns.scatterplot(x=ratings_count, y=vib_scores, marker='o', alpha=0.7, color='blue')
max_vib_score = data.loc[data['VIB评分'].idxmax()]
min_vib_score = data.loc[data['VIB评分'].idxmin()]
max_rating_count = data.loc[data['VIB评分数'].idxmax()]
min_rating_count = data.loc[data['VIB评分数'].idxmin()]
plt.scatter(x=max_vib_score['VIB评分数'], y=max_vib_score['VIB评分'], color='red', s=100, label=f'Max VIB Score: {max_vib_score["VIB评分"]}')
plt.scatter(x=min_vib_score['VIB评分数'], y=min_vib_score['VIB评分'], color='green', s=100, label=f'Min VIB Score: {min_vib_score["VIB评分"]}')
plt.scatter(x=max_rating_count['VIB评分数'], y=max_rating_count['VIB评分'], color='orange', s=100, label=f'Max Ratings Count: {max_rating_count["VIB评分数"]}')
plt.scatter(x=min_rating_count['VIB评分数'], y=min_rating_count['VIB评分'], color='purple', s=100, label=f'Min Ratings Count: {min_rating_count["VIB评分数"]}')
plt.title('VIB Scores vs Ratings Count', fontsize=16)
plt.xlabel('Ratings Count', fontsize=14)
plt.ylabel('VIB Score', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True)
plt.show()
