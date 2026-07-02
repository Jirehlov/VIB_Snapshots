import sys
import csv
input_array = list(map(int, sys.argv[1].strip("[]").split(",")))
with open("sorted1.csv", "r", encoding="utf-8-sig") as file:
    csv_reader = csv.reader(file)
    next(csv_reader)
    csv_column = {int(row[0]) for row in csv_reader}
common_numbers = [num for num in input_array if num in csv_column]
print(common_numbers)
