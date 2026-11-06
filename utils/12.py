import csv
def filter_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8-sig', errors='replace') as infile, open(output_file, 'w', encoding='utf-8-sig', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        for row in reader:
            column_value = str(row[2])
            if column_value.isascii():
                writer.writerow(row)
            else:
                print(f"Skipping row: {row}")
if __name__ == "__main__":
    input_csv = "sorted1.csv"
    output_csv = "out.csv"
    filter_csv(input_csv, output_csv)
