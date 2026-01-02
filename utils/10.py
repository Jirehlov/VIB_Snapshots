import csv
import itertools
def count_peak(row):
    count = 0
    newrow = [k for k, _ in itertools.groupby(list(map(int, row)))]
    n = len(newrow)
    if newrow[0] > newrow[1]:
        count += 1
    for i in range(1, n-1):
        if newrow[i] >= newrow[i-1] and newrow[i] >= newrow[i+1]:
            count += 1
    if newrow[n-1] > newrow[n-2]:
        count += 1
    return count
input_file = 'sorted1.csv'
peakmost_file = 'peakmost.csv'
peakleast_file = 'peakleast.csv'
max_rows_count_1 = []
max_rows_count_2 = []
with open(input_file, 'r', encoding='utf-8-sig') as infile, open(peakmost_file, 'w', encoding='utf-8-sig', newline='') as outfile:
    reader = csv.reader(infile)
    headers = next(reader)
    writer = csv.writer(outfile)
    writer.writerow(headers)
    for row in reader:
        count_1 = count_peak(row[7:17])
        count_2 = count_peak(row[20:30])
        max_rows_count_1.append((count_1, row))
        max_rows_count_1.sort(key=lambda x: x[0], reverse=True)
        max_rows_count_1 = max_rows_count_1[:10]
        max_rows_count_2.append((count_2, row))
        max_rows_count_2.sort(key=lambda x: x[0], reverse=True)
        max_rows_count_2 = max_rows_count_2[:10]
    for i, (count, row) in enumerate(max_rows_count_1):
        writer.writerow(row)
    for i, (count, row) in enumerate(max_rows_count_2):
        writer.writerow(row)
with open(input_file, 'r', encoding='utf-8-sig') as infile, open(peakleast_file, 'w', encoding='utf-8-sig', newline='') as outfile:
    reader = csv.reader(infile)
    headers = next(reader)
    writer = csv.writer(outfile)
    writer.writerow(headers)
    for row in reader:
        count_1 = count_peak(row[7:17])
        count_2 = count_peak(row[20:30])
        if count_1 == 1 and count_2 == 1:
            writer.writerow(row)
