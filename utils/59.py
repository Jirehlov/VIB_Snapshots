import argparse
import pandas as pd
import json
def main(json_file):
    df = pd.read_csv("sorted1.csv", encoding='utf-8-sig')
    with open(json_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    subject_ids = {item['subject_id'] for item in json_data}
    filtered_df = df[~df.iloc[:, 0].isin(subject_ids)]
    filtered_df.to_csv("VIB_yet_to_see.csv", index=False, encoding='utf-8-sig')
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='处理 CSV 和 JSON 文件')
    parser.add_argument('json_file', type=str, nargs='?', help='JSON 文件路径')
    args = parser.parse_args()
    if args.json_file is None:
        json_file = input('请输入 JSON 文件路径: ')
    else:
        json_file = args.json_file
    main(json_file)
