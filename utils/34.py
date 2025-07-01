import pandas as pd
import json
import argparse
from collections import defaultdict

def main(HOW_OLD, json_file):
    df = pd.read_csv("sorted1.csv", encoding='utf-8-sig')
    with open(json_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    subjects_info = {item['subject_id']: (item['rate'], item['subject_type'], item['collection_type']) for item in json_data}
    total_sum = 0.0
    frequency_counters = defaultdict(lambda: defaultdict(int))
    for subject_id, (_, subject_type, collection_type) in subjects_info.items():
        frequency_counters[subject_type][collection_type] += 1
    def to_offset(fc):
        return next((i for i, t in enumerate([1, 10, 50, 100, 200, 500, 1000]) if fc <= t), 7)
    times = 0
    for index, row in df.iterrows():
        subject_id = row['subject']
        if subject_id in subjects_info:
            rate, subject_type, collection_type = subjects_info[subject_id]
            if rate != 0:
                val1 = row.iloc[rate + 6]
                val2 = row.iloc[rate + 19]
                val3 = row.iloc[88 + collection_type - rate * 5]
                val4 = row.iloc[199 + to_offset(frequency_counters[subject_type][2]) - rate * 8]
                val5 = row.iloc[268 + HOW_OLD  - rate * 7]
                if val1 != 0 and val2 != 0 and val3 != 0 and val4 != 0 and val5 != 0:
                    times += 1
                    addition = 1 / val1 + 1 / val2 + 1 / val3 + 1 / val4 + 1 / val5
                    total_sum += addition
                else:
                    print(f"跳过数据零点:{rate} {collection_type} {frequency_counters[subject_type][2]} {subject_id} {val1} {val2} {val3} {val4} {val5}")
    if times > 0:
        per = total_sum / times * 100.0
        print(f"叛逆指数：{total_sum}\r\n命中的VIB条目数：{times}\r\n百倍单位命中条目的叛逆指数：100 * {total_sum} / {times} = {per}")
    else:
        print("无评分条目或评分条目未命中VIB")
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='叛逆指数计算。请先运行32.py获取个人收藏json、运行48.py获取VIB数据csv')
    parser.add_argument('HOW_OLD', type=int, nargs='?', help='1：10天 2：1个月 3：6个月 4：1年 5：2年 6：3年 7：>3年 不足则取大，例如不足1年取2年，即输入5')
    parser.add_argument('json_file', type=str, nargs='?', help='JSON文件路径')
    args = parser.parse_args()
    if args.HOW_OLD is None or args.json_file is None:
        HOW_OLD = int(input('请输入站龄（1：10天 2：1个月 3：6个月 4：1年 5：2年 6：3年 7：>3年 不足则取大，例如不足1年取2年，即输入5）: '))
        json_file = input('请输入JSON文件路径: ')
        main(HOW_OLD, json_file)
    else:
        main(args.HOW_OLD, args.json_file)
