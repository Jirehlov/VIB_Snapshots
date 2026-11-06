import requests
import json
import time
import urllib3
import httpx
import os
from datetime import datetime
import argparse

urllib3.disable_warnings()
limit = 50
guess = 1000000
subject_type = [1, 2, 3, 4, 6]
collection_type = [1, 2, 3, 4, 5]
default_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
headers = {'Accept': 'application/json'}
def fetch_data(u, subject_type_index, ct, offset, h):
    url = f"https://api.bgm.tv/v0/users/{u}/collections?subject_type={subject_type[subject_type_index]}&type={ct}&limit={limit}&offset={offset}"
    r = requests.get(url, headers=h, verify=False, timeout=60)
    time.sleep(0.5)
    return r.json()
def main(u, c, ua, au):
    a = []
    total_items = 0
    if c:
        headers['Cookie'] = c
    if ua:
        headers['User-Agent'] = ua
    else:
        headers['User-Agent'] = default_ua
    if au:
        headers['Authorization'] = "Bearer " + au
    for ct in collection_type:
        for i in range(len(subject_type)):
            initial_data = fetch_data(u, i, ct, guess, headers)
            if 'description' in initial_data and 'equal to' in initial_data['description']:
                total_items = int(initial_data['description'].split('equal to ')[1])
                print(f"已设定上限: {total_items}")
            else:
                total_items = 0
            for offset in range(0, total_items, limit):
                data = fetch_data(u, i, ct, offset, headers)
                for item in data.get('data', []):
                    item['collection_type'] = ct
                    a.append(item)
                print(f"已获取区间[{offset + 1}, {offset + limit}]")
    return a
def download_json(data, u):
    if not data:
        print('No data to download. Please try again.')
        return
    try:
        timestamp = datetime.now().isoformat().replace(':', '-')
        filename = f"BgmSyncFdata_{u}_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as o:
            json.dump(data, o, ensure_ascii=False, separators=(',', ':'))
        print(f"JSON成功写入到文件：{filename}")
    except Exception as error:
        print('An error occurred!')
        print(error)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch BGM collections and download as JSON.')
    parser.add_argument('username', type=str, nargs='?', help='Username')
    parser.add_argument('cookie', type=str, nargs='?', help='Cookie')
    parser.add_argument('user_agent', type=str, nargs='?', help='User-Agent')
    parser.add_argument('access_token', type=str, nargs='?', help='Access Token')
    args = parser.parse_args()
    if args.username:
        username = args.username
        cookie = args.cookie
        useragent = args.user_agent
        auth = args.access_token
    else:
        username = input("输入用户名: ")
        if not username:
            os._exit(1)
        cookie = input("输入cookie（没有就空着）: ")
        useragent = input("输入user-agent（没有就空着）: ")
        auth = input("输入Access Token（没有就空着）: ")
    all_data = main(username, cookie, useragent, auth)
    download_json(all_data, username)
