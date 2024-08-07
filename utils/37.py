import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
data = pd.read_csv('sorted1.csv', encoding='utf-8-sig')
one_score_rate = data.iloc[:, 7] / data.iloc[:, 6]
sns.set_theme(style="whitegrid")
vib_scores = data['VIB评分']
plt.figure(figsize=(12, 8))
sns.scatterplot(x=one_score_rate, y=vib_scores, marker='o', alpha=0.7, color='blue')
max_vib_score = data.loc[data['VIB评分'].idxmax()]
min_vib_score = data.loc[data['VIB评分'].idxmin()]
max_one_score_rate = data.loc[one_score_rate.idxmax()]
min_one_score_rate = data.loc[one_score_rate.idxmin()]
plt.scatter(x=one_score_rate[max_vib_score.name], y=max_vib_score['VIB评分'], color='red', s=100, label=f'Max VIB Score: {max_vib_score["VIB评分"]}')
plt.scatter(x=one_score_rate[min_vib_score.name], y=min_vib_score['VIB评分'], color='green', s=100, label=f'Min VIB Score: {min_vib_score["VIB评分"]}')
plt.scatter(x=one_score_rate[max_one_score_rate.name], y=max_one_score_rate['VIB评分'], color='orange', s=100, label=f'Max One Score Rate: {one_score_rate[max_one_score_rate.name]:.2f}')
plt.scatter(x=one_score_rate[min_one_score_rate.name], y=min_one_score_rate['VIB评分'], color='purple', s=100, label=f'Min One Score Rate: {one_score_rate[min_one_score_rate.name]:.2f}')
plt.title('VIB Scores vs One Score Rate', fontsize=16)
plt.xlabel('One Score Rate', fontsize=14)
plt.ylabel('VIB Score', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True)
plt.show()
