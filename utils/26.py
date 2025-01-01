import csv
from collections import Counter
def count_characters(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8-sig') as file:
        text = file.read()
    char_count = Counter(text)
    with open(output_file, 'w', encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Character', 'Frequency'])
        for char, freq in char_count.items():
            writer.writerow([char, freq])
input_file = 'sorted1.csv'
output_file = 'char.csv'
count_characters(input_file, output_file)
