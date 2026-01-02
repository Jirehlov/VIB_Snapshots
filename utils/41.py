import pandas as pd
import json
import argparse
from datetime import datetime
def main(json_file):
    df = pd.read_csv("sorted1.csv", encoding='utf-8-sig')
    with open(json_file, 'r', encoding='utf-8') as f:
        subjects_info = {item['subject_id']: {'rate': item['rate'], 'date': item['subject']['date']} for item in json.load(f)}
    total_subjects = zero_count = one_count = equal_count = 0
    today = datetime.now().date()
    for index, row in df.iterrows():
        subject_id = row['subject']
        if subject_id in subjects_info:
            rate = subjects_info[subject_id]['rate']
            date = subjects_info[subject_id]['date']
            if date and datetime.strptime(date, '%Y-%m-%d').date() > today:
                continue
            VIB_score = row.iloc[rate + 6]
            Surface_score = row.iloc[rate + 19]
            total_subjects += 1
            if VIB_score == 0:
                zero_count += 1
                print(f"VIB评评分数为0的条目: subject_id: {subject_id}, rate: {rate}")
            elif VIB_score == Surface_score == 1:
                one_count += 1
                print(f"表评与VIB评评分数均为1的条目: subject_id: {subject_id}, rate: {rate}")
            elif VIB_score == Surface_score:
                equal_count += 1
                print(f"表评与VIB评评分数相等但不是1的条目: subject_id: {subject_id}, rate: {rate}")
    if total_subjects > 0:
        print(f"总条目数：{total_subjects}")
        print(f"VIB评评分数为0的条目数：{zero_count}")
        print(f"表评与VIB评评分数均为1的条目数：{one_count}")
        print(f"表评与VIB评评分数相等但不是1的条目数：{equal_count}")
        if zero_count > 1 and one_count == equal_count == 0:
            print("用户极可能不是VIB")
        elif zero_count == 0 and (one_count > 1 or equal_count > 2):
            print("用户极可能是VIB")
        elif zero_count == 1 and one_count == equal_count == 0:
            print("用户可能不是VIB")
        elif zero_count == 0 and (one_count == 1 or equal_count == 2):
            print("用户可能是VIB")
        else:
            print("无法判定")
    else:
        print("无评分条目")
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='VIB判定。请先运行32.py获取个人收藏json以及VIB数据csv')
    parser.add_argument('json_file', type=str, nargs='?', help='JSON文件路径')
    args = parser.parse_args()
    main(args.json_file if args.json_file else input('请输入JSON文件路径: '))
