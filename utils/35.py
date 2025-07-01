import json
import csv
import os
import argparse
def find_tags(data, tags_dict):
    if isinstance(data, dict):
        for value in data.values():
            find_tags(value, tags_dict)
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict) and "name" in item and "count" in item:
                tags_dict[item["name"]] = tags_dict.get(item["name"], 0) + item["count"]
            find_tags(item, tags_dict)
def main(json_filename):
    with open(json_filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    tags_dict = {}
    find_tags(data, tags_dict)
    with open(f"{os.path.splitext(json_filename)[0]}.tags.csv", 'w', newline='', encoding='utf-8-sig') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['name', 'count'])
        writer.writerows(sorted(tags_dict.items(), key=lambda item: item[1], reverse=True))
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process JSON and extract tag counts.')
    parser.add_argument('json_filename', type=str, help='Path to the JSON file')
    args = parser.parse_args()
    main(args.json_filename)
