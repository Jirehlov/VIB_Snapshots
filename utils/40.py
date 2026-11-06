import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
data = pd.read_csv('sorted1.csv', encoding='utf-8-sig')
ten_score_rate = data.iloc[:, 29] / data.iloc[:, 18]
sns.set_theme(style="whitegrid")
surface_scores = data['表面评分']
plt.figure(figsize=(12, 8))
sns.scatterplot(x=ten_score_rate, y=surface_scores, marker='o', alpha=0.7, color='blue')
max_surface_score = data.loc[data['表面评分'].idxmax()]
min_surface_score = data.loc[data['表面评分'].idxmin()]
max_ten_score_rate = data.loc[ten_score_rate.idxmax()]
min_ten_score_rate = data.loc[ten_score_rate.idxmin()]
plt.scatter(x=ten_score_rate[max_surface_score.name], y=max_surface_score['表面评分'], color='red', s=100, label=f'Max Surface Score: {max_surface_score["表面评分"]}')
plt.scatter(x=ten_score_rate[min_surface_score.name], y=min_surface_score['表面评分'], color='green', s=100, label=f'Min Surface Score: {min_surface_score["表面评分"]}')
plt.scatter(x=ten_score_rate[max_ten_score_rate.name], y=max_ten_score_rate['表面评分'], color='orange', s=100, label=f'Max Ten Score Rate: {ten_score_rate[max_ten_score_rate.name]:.2f}')
plt.scatter(x=ten_score_rate[min_ten_score_rate.name], y=min_ten_score_rate['表面评分'], color='purple', s=100, label=f'Min Ten Score Rate: {ten_score_rate[min_ten_score_rate.name]:.2f}')
plt.title('Surface Scores vs Ten Score Rate', fontsize=16)
plt.xlabel('Ten Score Rate', fontsize=14)
plt.ylabel('Surface Score', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True)
plt.show()
