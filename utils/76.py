import json, sys
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.dates import MonthLocator, DateFormatter
rcParams['font.sans-serif'] = ['SimHei']
rcParams['axes.unicode_minus'] = False
data = json.load(open(sys.argv[1]))
dates = [datetime.strptime(v, "%Y-%m-%d") for v in data.values()]
dates.sort()
plt.hist(dates, bins=len(set(dates)), color='skyblue', edgecolor='black', alpha=0.7)
plt.title("用户注册日期分布")
plt.xlabel("日期")
plt.ylabel("用户数量")
ax = plt.gca()
ax.xaxis.set_major_locator(MonthLocator(interval=3))
ax.xaxis.set_major_formatter(DateFormatter("%Y-%m"))
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
