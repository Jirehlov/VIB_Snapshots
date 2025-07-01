import json
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from collections import defaultdict
import pandas as pd
def export_and_plot(json_file, csv_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    daily_users = defaultdict(list)
    for key, date in data.items():
        if key.isdigit():
            daily_users[date].append(int(key))
    daily_counts = {date: max(ids) - min(ids) + 1 if ids else 0 for date, ids in daily_users.items()}
    dates_counts = sorted((datetime.strptime(d, '%Y-%m-%d').date(), c) for d, c in daily_counts.items())
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'New Users'])
        writer.writerows((d.strftime('%Y-%m-%d'), c) for d, c in dates_counts)
    df = pd.DataFrame(dates_counts, columns=['Date', 'New Users'])
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.to_period('M').dt.to_timestamp()
    monthly_counts = df.groupby('Month')['New Users'].sum().reset_index()
    yearly_counts = df.groupby('Year')['New Users'].sum().reset_index()
    def plot_chart(x, y, xlabel, title, date_format=None):
        plt.figure(figsize=(12, 6))
        plt.bar(x, y, color='skyblue', width=20 if date_format else 1, align='center')
        plt.xlabel(xlabel)
        plt.ylabel("New Users")
        plt.title(title)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        if date_format:
            ax = plt.gca()
            ax.xaxis.set_major_locator(mdates.AutoDateLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))
            plt.xticks(rotation=45)
        plt.show()
    plot_chart(df['Date'], df['New Users'], "Date", "Daily New Users Over Time")
    plot_chart(monthly_counts['Month'], monthly_counts['New Users'], "Month", "Monthly New Users Over Time", date_format='%Y-%m')
    plot_chart(yearly_counts['Year'].astype(str), yearly_counts['New Users'], "Year", "Yearly New Users Over Time")
export_and_plot('userages.json', '93.csv')
