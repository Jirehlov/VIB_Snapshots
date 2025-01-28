import json, time, requests, sys
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
delay = 0.5
def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)
def save_json(data, file_path):
    cleaned_data = {}
    for date in set(data.values()):
        ids = [int(k[8:]) for k, v in data.items() if k.startswith("userAge_") and k[8:].isdigit() and v == date]
        if ids:
            cleaned_data[f"userAge_{min(ids)}"] = date
            cleaned_data[f"userAge_{max(ids)}"] = date
    cleaned_data.update({k: v for k, v in data.items() if not k[8:].isdigit()})
    with open(file_path, "w") as f:
        json.dump(dict(sorted(cleaned_data.items(),key=lambda x: (not x[0][8:].isdigit(),int(x[0][8:]) if x[0][8:].isdigit() else 0,),)),f,ensure_ascii=False,)
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
def calculate_skip_ranges(result):
    return [(min(ids), max(ids)) for date in set(result.values()) if (ids := sorted(int(k[8:]) for k, v in result.items() if k[8:].isdigit() and v == date))]
def binary_search(start, end, skip_ranges, result, missing_ids):
    if start > end: return
    mid = (start + end) // 2
    if any(r_start <= mid <= r_end for r_start, r_end in skip_ranges) or f"userAge_{mid}" in result:
        binary_search(start, mid - 1, skip_ranges, result, missing_ids)
        binary_search(mid + 1, end, skip_ranges, result, missing_ids)
        return
    date = get_user_date(mid)
    print(f"Fetched {mid} with date {date}")
    if date:
        result[f"userAge_{mid}"] = date
        save_json(result, "user_data.json")
        skip_ranges[:] = calculate_skip_ranges(result)
        binary_search(start, mid - 1, skip_ranges, result, missing_ids)
        binary_search(mid + 1, end, skip_ranges, result, missing_ids)
    else:
        print(f"Date for userAge_{mid} not found. Trying +1 and -1...")
        adjacent_dates = []
        for offset in [-1, 1]:
            adjacent_id = mid + offset
            if adjacent_id > 0:
                for r_start, r_end in skip_ranges:
                    if r_start <= adjacent_id <= r_end:
                        adjacent_date = result.get(f"userAge_{r_start}", None)
                        print(f"Skipping fetch for {adjacent_id}. Using date {adjacent_date}")
                        adjacent_dates.append((adjacent_id, adjacent_date))
                        break
                else:
                    adjacent_date = get_user_date(adjacent_id)
                    print(f"Fetched {adjacent_id} with date {adjacent_date}")
                    adjacent_dates.append((adjacent_id, adjacent_date))
        if len(adjacent_dates) == 2 and adjacent_dates[0][1] == adjacent_dates[1][1]:
            result[f"userAge_{mid-1}"] = adjacent_dates[0][1]
            result[f"userAge_{mid}"] = adjacent_dates[0][1]
            result[f"userAge_{mid+1}"] = adjacent_dates[0][1]
            print(f"Mid {mid} and its neighbors have the same date: {adjacent_dates[0][1]}")
            save_json(result, "user_data.json")
            skip_ranges[:] = calculate_skip_ranges(result)
            return
        else:
            print(f"The date of {mid} is still a mystery.")
        missing_ids.append(mid)
def main():
    upper_limit = int(sys.argv[1])
    data = load_json("user_data.json")
    result = {k: v for k, v in data.items() if k.startswith("userAge_")}
    skip_ranges = calculate_skip_ranges(result)
    missing_ids = []
    binary_search(1, upper_limit, skip_ranges, result, missing_ids)
    with open("missing_ids.json", "w") as f:
        json.dump(missing_ids, f)
if __name__ == "__main__":
    main()
