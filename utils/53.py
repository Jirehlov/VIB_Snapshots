import os
import argparse
import csv
def detect_line_ending(file_path):
    with open(file_path, 'rb') as f:
        first_line = f.readline()
        if b'\r\n' in first_line:
            return 'CRLF'
        elif b'\r' in first_line:
            return 'CR'
        elif b'\n' in first_line:
            return 'LF'
    return 'Unknown'
def convert_to_crlf(file_path):
    with open(file_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, lineterminator='\r\n')
        writer.writerows(rows)
def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                line_ending = detect_line_ending(file_path)
                print(f'{file}: {line_ending}')
                if line_ending != 'CRLF':
                    convert_to_crlf(file_path)
                    print(f'Converted {file} to CRLF')
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Batch check and convert CSV line endings in a directory.')
    parser.add_argument('directory', type=str, help='Path to the directory containing CSV files')
    args = parser.parse_args()
    process_directory(args.directory)
