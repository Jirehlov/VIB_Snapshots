import json
import csv
import datetime
from collections import defaultdict
with open('userages.json', 'r') as f:
    data = json.load(f)
date_by_id = {}
valid_ids = []
for key in data:
    if key.isdigit():
        id = int(key)
        valid_ids.append(id)
        date_str = data[key]
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        date_by_id[id] = date
date_to_ids = defaultdict(list)
for id, date in date_by_id.items():
    date_to_ids[date].append(id)
existing_ids = set()
for date, ids in date_to_ids.items():
    if ids:
        min_id = min(ids)
        max_id = max(ids)
        existing_ids.update(range(min_id, max_id + 1))
missing_ids = []
if existing_ids:
    min_existing = min(existing_ids)
    max_existing = max(existing_ids)
    all_possible = set(range(min_existing, max_existing + 1))
    missing_ids = sorted(all_possible - existing_ids)
with open('msid.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Missing IDs'])
    for mid in missing_ids:
        writer.writerow([mid])
existing_dates = set(date_by_id.values())
filled_dates = set()
sorted_original_ids = sorted(date_by_id.keys())
for i in range(len(sorted_original_ids) - 1):
    current_id = sorted_original_ids[i]
    next_id = sorted_original_ids[i + 1]
    if next_id - current_id == 1:
        current_date = date_by_id[current_id]
        next_date = date_by_id[next_id]
        start = min(current_date, next_date)
        end = max(current_date, next_date)
        delta_days = (end - start).days
        for d in range(delta_days + 1):
            filled_date = start + datetime.timedelta(days=d)
            filled_dates.add(filled_date)
all_dates = existing_dates.union(filled_dates)
missing_dates = []
if all_dates:
    min_date = min(all_dates)
    max_date = max(all_dates)
    current_date = min_date
    while current_date <= max_date:
        if current_date not in all_dates:
            missing_dates.append(current_date)
        current_date += datetime.timedelta(days=1)
with open('msdates.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Missing Dates'])
    for md in sorted(missing_dates):
        writer.writerow([md.strftime('%Y-%m-%d')])
