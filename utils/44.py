import csv
with open('sorted1.csv', mode='r', encoding='utf-8-sig') as file:
    data = list(csv.reader(file))
    total_cells = sum(len(row) for row in data)
    zero_count = sum(cell == '0' for row in data for cell in row)
    zero_ratio = zero_count / total_cells if total_cells else 0
print(f"Number of cells with value 0: {zero_count}")
print(f"Proportion of cells with value 0: {zero_ratio:.2%}")
