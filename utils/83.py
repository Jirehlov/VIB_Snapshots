import os
import pandas as pd
import re
directory = './year_end_report/2024/'
if not os.path.exists(directory):
    print(f"目录 {directory} 不存在。")
    exit()
file_pattern = re.compile(r'sorted_(\d+)\.csv')
csv_files = []
for filename in os.listdir(directory):
    match = file_pattern.match(filename)
    if match:
        csv_files.append((int(match.group(1)), filename))
csv_files.sort()
def initialize_changes():
    return {f"{i}.1": {"count": 0, "values": [], "first_values":[], "third_values":[]} for i in range(1, 11)}
def initialize_prev_first_values():
    return {f"{i}.1": None for i in range(1, 11)}
def initialize_prev_third_values():
    return {f"{i}.1": None for i in range(1, 11)}
changes = initialize_changes()
prev_first_values = initialize_prev_first_values()
prev_third_values = initialize_prev_third_values()
for _, csv_file in csv_files:
    file_path = os.path.join(directory, csv_file)
    df = pd.read_csv(file_path)
    for col in changes.keys():
        if col in df.columns:
            max_val_index = df[col].idxmax()
            if pd.notna(max_val_index):
                first_col_value = df.iloc[max_val_index, 0]
                third_col_value = df.iloc[max_val_index, 2] if len(df.columns) > 2 else None
                if prev_first_values[col] is None:
                    changes[col]["first_values"].append(first_col_value)
                    changes[col]["third_values"].append(third_col_value)
                elif prev_first_values[col] != first_col_value:
                    changes[col]["count"] += 1
                    changes[col]["values"].append(first_col_value)
                    changes[col]["first_values"].append(first_col_value)
                    changes[col]["third_values"].append(third_col_value)
                prev_first_values[col] = first_col_value
                prev_third_values[col] = third_col_value
for col, change_data in changes.items():
    count = change_data["count"]
    values = change_data["values"]
    first_values = change_data["first_values"]
    third_values = change_data["third_values"]
    print(f"\"{col}\"列最大值的行的第一列和第三列的值变化了{count}次:")
    if count == 0:
      if first_values:
        print(f"\t初始第一列值: {first_values[0]}, 初始第三列值: {third_values[0]}")
      else:
        print(f"\t没有数据")
    else:
        for i in range(len(values)):
            print(f"\t第{i+1}次变化：第一列值: {first_values[i+1]}, 第三列值: {third_values[i+1]}")
