import json, time, requests, sys, csv
from collections import defaultdict
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
delay = 0.8
def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)
def load_msid(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return {int(row[0]) for row in csv.reader(f) if row and row[0].isdigit()}
def save_json(data, file_path):
    date_map = {}
    cleaned_data = {}
    for k, v in data.items():
        if k.isdigit():
            uid = int(k)
            if v in date_map:
                date_map[v][0] = min(date_map[v][0], uid)
                date_map[v][1] = max(date_map[v][1], uid)
            else:
                date_map[v] = [uid, uid]
        else:
            cleaned_data[k] = v
    cleaned_data.update({str(min_id): date for date, (min_id, max_id) in date_map.items()})
    cleaned_data.update({str(max_id): date for date, (min_id, max_id) in date_map.items() if min_id != max_id})
    with open(file_path, "w") as f:
        json.dump(cleaned_data, f, ensure_ascii=False, separators=(",", ":"))
session = requests.Session()
def get_user_date(user_id):
    url = f"https://bgm.tv/user/{user_id}"
    response = session.get(url, headers=headers, allow_redirects=True)
    time.sleep(delay)
    response.encoding = "utf-8"
    if response.status_code in (301, 302):
        return get_user_date(response.headers["Location"].split("/")[-1])
    if "\u52a0\u5165" in response.text:
        start = response.text.find('<span class="tip">') + len('<span class="tip">')
        end = response.text.find("</span>", start)
        return response.text[start:end].strip().replace("\u52a0\u5165", "").strip()
    return None
def calculate_skip_ranges(result):
    date_to_ids = defaultdict(list)
    for k, v in result.items():
        if k.isdigit():
            date_to_ids[v].append(int(k))
    return [(min(ids), max(ids)) for ids in map(sorted, date_to_ids.values())]
def binary_search(start, end, skip_ranges, result, msid_set):
    if start > end: return
    mid = (start + end) // 2
    if mid in msid_set or any(r_start <= mid <= r_end for r_start, r_end in skip_ranges) or str(mid) in result:
        binary_search(start, mid - 1, skip_ranges, result, msid_set)
        binary_search(mid + 1, end, skip_ranges, result, msid_set)
        return
    date = get_user_date(mid)
    print(f"Fetched {mid} with date {date}")
    if date:
        result[str(mid)] = date
        save_json(result, "userages.json")
        skip_ranges[:] = calculate_skip_ranges(result)
        binary_search(start, mid - 1, skip_ranges, result, msid_set)
        binary_search(mid + 1, end, skip_ranges, result, msid_set)
    else:
        print(f"Date for {mid} not found. Trying +1 and -1...")
        adjacent_dates = []
        for offset in [-1, 1]:
            adjacent_id = mid + offset
            if adjacent_id > 0 and adjacent_id not in msid_set:
                for r_start, r_end in skip_ranges:
                    if r_start <= adjacent_id <= r_end:
                        adjacent_date = result.get(str(r_start), None)
                        print(f"Skipping fetch for {adjacent_id}. Using date {adjacent_date}")
                        adjacent_dates.append((adjacent_id, adjacent_date))
                        break
                else:
                    adjacent_date = get_user_date(adjacent_id)
                    print(f"Fetched {adjacent_id} with date {adjacent_date}")
                    adjacent_dates.append((adjacent_id, adjacent_date))
        if len(adjacent_dates) == 2 and adjacent_dates[0][1] == adjacent_dates[1][1] and adjacent_dates[0][1] is not None:
            result[str(mid - 1)] = adjacent_dates[0][1]
            result[str(mid)] = adjacent_dates[0][1]
            result[str(mid + 1)] = adjacent_dates[0][1]
            print(f"Mid {mid} and its neighbors have the same date: {adjacent_dates[0][1]}")
            save_json(result, "userages.json")
            skip_ranges[:] = calculate_skip_ranges(result)
            return
        else:
            print(f"The date of {mid} is still a mystery.")
def main():
    if len(sys.argv) > 1 and sys.argv[1] == "m":
        msid_set = load_msid("msid.csv")
        result = load_json("userages.json")
        save_json(result, "userages.json")
        skip_ranges = calculate_skip_ranges(result)
        for mid in sorted(msid_set):
            if any(r_start <= mid <= r_end for r_start, r_end in skip_ranges) or str(mid) in result:
                continue
            date = get_user_date(mid)
            print(f"Fetched {mid} with date {date}")
            if date:
                result[str(mid)] = date
                save_json(result, "userages.json")
                skip_ranges[:] = calculate_skip_ranges(result)
        return
    upper_limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    msid_set = load_msid("msid.csv")
    result = load_json("userages.json")
    save_json(result, "userages.json")
    skip_ranges = calculate_skip_ranges(result)
    if upper_limit is None:
        print(f"No upper_limit given. Trying to determine...")
        existing_ids = [int(k) for k in result if k.isdigit()]
        if existing_ids:
            lower_bound, upper_limit = max(existing_ids), max(existing_ids) + 15000
            while lower_bound < upper_limit:
                mid = (lower_bound + upper_limit) // 2
                date = get_user_date(mid)
                print(f"Fetched {mid} with date {date}")
                if date:
                    result[str(mid)] = date
                    save_json(result, "userages.json")
                    skip_ranges[:] = calculate_skip_ranges(result)
                    lower_bound = mid + 1
                else:
                    upper_limit = mid
            upper_limit = lower_bound - 1
    print(f"set upper_limit to {upper_limit}")
    binary_search(1, upper_limit, skip_ranges, result, msid_set)
if __name__ == "__main__":
    main()
