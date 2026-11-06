import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
data = pd.read_csv('sorted1.csv', encoding='utf-8-sig')
data['发布发售放送时间'] = pd.to_datetime(data['发布发售放送时间'], errors='coerce')
sns.set_theme(style="whitegrid")
vib_scores = data['VIB评分']
release_dates = data['发布发售放送时间']
plt.figure(figsize=(12, 8))
sns.scatterplot(x=release_dates, y=vib_scores, marker='o', alpha=0.7, color='blue')
max_vib_score = data.loc[data['VIB评分'].idxmax()]
min_vib_score = data.loc[data['VIB评分'].idxmin()]
data_non_na = data.dropna(subset=['发布发售放送时间'])
max_release_date = data_non_na.loc[data_non_na['发布发售放送时间'].idxmax()]
min_release_date = data_non_na.loc[data_non_na['发布发售放送时间'].idxmin()]
plt.scatter(x=max_vib_score['发布发售放送时间'], y=max_vib_score['VIB评分'], color='red', s=100, label=f'Max VIB Score: {max_vib_score["VIB评分"]}')
plt.scatter(x=min_vib_score['发布发售放送时间'], y=min_vib_score['VIB评分'], color='green', s=100, label=f'Min VIB Score: {min_vib_score["VIB评分"]}')
plt.scatter(x=max_release_date['发布发售放送时间'], y=max_release_date['VIB评分'], color='orange', s=100, label=f'Max Release Date: {max_release_date["发布发售放送时间"].strftime("%Y-%m-%d")}')
plt.scatter(x=min_release_date['发布发售放送时间'], y=min_release_date['VIB评分'], color='purple', s=100, label=f'Min Release Date: {min_release_date["发布发售放送时间"].strftime("%Y-%m-%d")}')
plt.title('VIB Scores vs Release Dates', fontsize=16)
plt.xlabel('Release Date', fontsize=14)
plt.ylabel('VIB Score', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
