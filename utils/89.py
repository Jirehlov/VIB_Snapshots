import json, time, random, sys, requests
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
delay = 0.5
def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)
def get_user_date(user_id):
    url = f"https://bgm.tv/user/{user_id}"
    response = requests.get(url, headers=headers, allow_redirects=True)
    response.encoding = "utf-8"
    if response.status_code in (301, 302):
        return get_user_date(response.headers["Location"].split("/")[-1])
    if "\u52a0\u5165" in response.text:
        start = response.text.find('<span class="tip">') + len('<span class="tip">')
        end = response.text.find("</span>", start)
        return response.text[start:end].strip().replace("\u52a0\u5165", "").strip()
    return None
def main():
    data = load_json("userages.json")
    user_ids = [int(k) for k in data.keys() if k.isdigit()]
    random_ids = random.sample(user_ids, min(10, len(user_ids)))  
    for id in random_ids:
        actual_date = get_user_date(id)
        json_date = data[str(id)]
        status = "✔" if actual_date == json_date else "✘"
        print(f"ID: {id}, Actual Date: {actual_date}, JSON Date: {json_date} {status}")
        time.sleep(delay)
if __name__ == "__main__":
    main()
