import csv
import argparse
import os
def process_csv(file_path, print_entries):
    count_7 = count_20 = 0
    with open(file_path, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            try:
                num_7 = sum((i + 1) * float(row[7 + i]) for i in range(10))
                denom_7 = sum(float(row[7 + i]) for i in range(10))
                if denom_7 != 0 and num_7 % denom_7 == 0:
                    if print_entries:
                        print(['VIB'] + row[:4] + [row[4], row[6]])
                    count_7 += 1
                num_20 = sum((i + 1) * float(row[20 + i]) for i in range(10))
                denom_20 = sum(float(row[20 + i]) for i in range(10))
                if denom_20 != 0 and num_20 % denom_20 == 0:
                    if print_entries:
                        print(['Surface'] + row[:4] + [row[19], row[18]])
                    count_20 += 1
            except (ValueError, IndexError):
                continue
    return count_7, count_20
def main():
    parser = argparse.ArgumentParser(description='Process CSV files or directories.')
    parser.add_argument('path', type=str, help='Path to a CSV file or directory')
    args = parser.parse_args()
    if os.path.isfile(args.path):
        count_7, count_20 = process_csv(args.path, print_entries=True)
        print(f"Total count for VIB: {count_7}")
        print(f"Total count for Surface: {count_20}")
    elif os.path.isdir(args.path):
        for filename in os.listdir(args.path):
            if filename.startswith('sorted') and filename.endswith('.csv'):
                file_path = os.path.join(args.path, filename)
                count_7, count_20 = process_csv(file_path, print_entries=False)
                print(f"{filename}: VIB count = {count_7}, Surface count = {count_20}")
    else:
        print(f"Error: {args.path} is neither a file nor a directory")
if __name__ == '__main__':
    main()
