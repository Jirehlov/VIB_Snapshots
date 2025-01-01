import requests, zipfile, os, urllib3
urllib3.disable_warnings()
json_url = "https://raw.githubusercontent.com/bangumi/Archive/master/aux/latest.json"
latest_info = requests.get(json_url, verify=False).json()
download_url = latest_info["browser_download_url"]
updated_at = latest_info["updated_at"]
timestamp_file = "dump_timestamp.txt"
if not os.path.exists(timestamp_file) or open(timestamp_file).read().strip() != updated_at:
    with open(latest_info["name"], 'wb') as f:
        f.write(requests.get(download_url, verify=False).content)
    with zipfile.ZipFile(latest_info["name"], 'r') as z:
        z.extractall('.')
    os.remove(latest_info["name"])
    with open(timestamp_file, "w") as f:
        f.write(updated_at)
else:
    print("文件已经是最新的，跳过下载。")
