import csv
import os
def are_column_values_unique(file_path, column_index):
    with open(file_path, newline='', encoding = 'utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        seen = set()
        return all(value not in seen and not seen.add(value) for value in (row[column_index] for row in reader))
file_path = os.path.expandvars('%USERPROFILE%\\Documents\\GitHub\\VIB_Snapshots\\server_backup\\skip_counts.csv')
column_index = 0
is_unique = are_column_values_unique(file_path, column_index)
print(f"All values in column {column_index} are unique: {is_unique}")
