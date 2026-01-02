import pandas as pd
import numpy as np
import os
import requests
import time
import shutil
import json
def load_data(fp):
    df = pd.read_csv(fp, encoding="utf-8-sig")
    df['更新时间'] = pd.to_datetime(df['更新时间'], format='%Y-%m-%dT%H:%M:%SZ')
    df['发布发售放送时间'] = pd.to_datetime(df['发布发售放送时间'], format='%Y-%m-%d', errors='coerce')
    return df.sort_values('更新时间')
def valid_time(df):
    start, end = None, None
    for i in range(len(df) - 1):
        if df['subject'].iloc[i] < df['subject'].iloc[i + 1]:
            if start is None:
                start = i
            end = i + 1
        else:
            start = None
    if start is not None:
        return (df['更新时间'].iloc[start], df['更新时间'].iloc[end])
    return None
def valid_ratio(df, vt): return len(df[(df['更新时间'] >= vt[0]) & (df['更新时间'] <= vt[1])]) / len(df) if vt else 0
def filter_df(df, inv_subs, end_time, incl_end):
    df = df[~df['subject'].isin(inv_subs)]
    if not incl_end and end_time:
        df = df[(df['发布发售放送时间'].isna()) | (end_time - df['发布发售放送时间'] > pd.Timedelta(days=182.5))]
    return df
def top_changes(data, merged, col, label, subjects):
    def format_value(value, is_top):
        if col == 'VIB率增减':
            value = float(value) * 100
            return f"+{value:.2f}%" if is_top else f"{value:.2f}%"
        return f"+{value}" if is_top else str(value)
    top = merged.nlargest(10, col)[['subject', '中文标题', col]]
    bottom = merged.nsmallest(10, col)[['subject', '中文标题', col]].iloc[::-1]
    top[col] = top[col].apply(lambda x: format_value(x, is_top=True))
    bottom[col] = bottom[col].apply(lambda x: format_value(x, is_top=False))
    data[label] = {
        "largest": top.to_dict(orient="records"),
        "smallest": bottom.to_dict(orient="records")
    }
    subjects.update(merged.nlargest(10, col)['subject'].unique())
    subjects.update(merged.nsmallest(10, col)['subject'].unique())
    return subjects
def report_section(data, d1, d5, sec_name, all_subjects):
    section = {}
    added = d1[~d1['subject'].isin(d5['subject'])]
    section["新增条目数量"] = len(added)
    worst_vib = added.nsmallest(10, 'VIB朴素排名')
    all_subjects.update(set(worst_vib['subject']))
    section["新增条目中VIB朴素排名最高的10个"] = worst_vib[['subject', '中文标题', 'VIB朴素排名']].to_dict(orient="records")
    added_anime = added[added['类型'] == 2]
    worst_vib_anime = added_anime.nsmallest(10, 'VIB朴素排名')
    all_subjects.update(set(worst_vib_anime['subject']))
    section["新增条目（动画）中VIB朴素排名最高的10个"] = worst_vib_anime[['subject', '中文标题', 'VIB朴素排名']].to_dict(orient="records")
    merged = d1.merge(d5, on='subject', suffixes=('_1', '_5'))
    merged['中文标题'] = merged['中文标题_1'].combine_first(merged['中文标题_5'])
    for col, label in [('VIB朴素排名', 'VIB朴素排名增减'), ('VIB评分', 'VIB评分增减'), ('VIB评分数', 'VIB评分数增减')]:
        merged[label] = merged[f'{col}_1'] - merged[f'{col}_5']
    merged['VIB率增减'] = (merged['VIB评分数_1'] / merged['表面评分数_1'].replace(0, np.nan)) - (merged['VIB评分数_5'] / merged['表面评分数_5'].replace(0, np.nan))
    for col in ['VIB朴素排名增减', 'VIB评分增减', 'VIB评分数增减', 'VIB率增减']:
        all_subjects = top_changes(section, merged, col, col, all_subjects)
    cols = [f"{i}.1" for i in range(1, 11)]
    for col in cols:
        label = col.replace(".1", "分") + "增减"
        merged[label] = merged[f'{col}_1'] - merged[f'{col}_5']
        all_subjects = top_changes(section, merged, label, label, all_subjects)
    merged['绝对值和'] = merged[[col.replace(".1", "分") + "增减" for col in cols]].abs().sum(axis=1)
    merged['VIB评分数增减'] = (merged['VIB评分数_1'] - merged['VIB评分数_5']).abs()
    merged['比值'] = merged['VIB评分数增减'] / merged['绝对值和'].replace(0, np.nan)
    ratio_decrease = merged[merged['比值'] > 0].nsmallest(10, '比值')[['subject', '中文标题', '比值']]
    ratio_decrease['比值'] = (ratio_decrease['比值'] * 100).apply(lambda x: f"{x:.2f}%")
    section["比值最小的10个"] = ratio_decrease.to_dict(orient="records")
    all_subjects.update(ratio_decrease['subject'].unique())
    data[sec_name] = section
    return data, all_subjects
def download_cover(subject_id, cover_dir="covers"):
    if not os.path.exists(cover_dir):
        os.makedirs(cover_dir)
    filename = os.path.join(cover_dir, f"{subject_id}.jpg")
    if os.path.exists(filename):
        return
    url = f"https://api.bgm.tv/v0/subjects/{subject_id}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        if "images" in data and "common" in data["images"]:
            cover_url = data["images"]["common"]
            cover_response = requests.get(cover_url, stream=True)
            time.sleep(2)
            cover_response.raise_for_status()
            with open(filename, "wb") as f:
                for chunk in cover_response.iter_content(1024):
                    f.write(chunk)
        else:
            shutil.copy("covers/e.jpg", filename)
    except:
        shutil.copy("covers/e.jpg", filename)
def detect_poincare_regression(d1, d5, valid_time_range):
    merged = d1.merge(d5, on='subject', suffixes=('_1', '_5'))
    poincare_regression = merged[merged['VIB评分_1'] == merged['VIB评分_5']]
    if valid_time_range:
        start_time, end_time = valid_time_range
        poincare_regression = poincare_regression[
            (poincare_regression['更新时间_1'] >= start_time) &
            (poincare_regression['更新时间_1'] <= end_time)
        ]
    return poincare_regression[['subject', '中文标题_1', 'VIB评分_1']].rename(
        columns={'中文标题_1': '中文标题', 'VIB评分_1': 'VIB评分'}
    ).to_dict(orient="records")
d1 = load_data('sorted1.csv')
d5 = load_data('sorted5.csv')
vt1 = valid_time(d1)
vt5 = valid_time(d5)
r1 = valid_ratio(d1, vt1)
r5 = valid_ratio(d5, vt5)
inv_subs = set(d1[d1['VIB朴素排名'] == 0]['subject']).union(set(d5[d5['VIB朴素排名'] == 0]['subject']))
invalid_entries = {
    "sorted1.csv": sum(d1['表面排名'] == 0),
    "sorted5.csv": sum(d5['表面排名'] == 0)
}
poincare_regression_entries = detect_poincare_regression(d1, d5, vt1)
data = {
    "快照有效时间区间": {
        "sorted1.csv": (vt1[0].strftime('%Y-%m-%dT%H:%M:%S') if vt1 else None, vt1[1].strftime('%Y-%m-%dT%H:%M:%S') if vt1 else None),
        "sorted5.csv": (vt5[0].strftime('%Y-%m-%dT%H:%M:%S') if vt5 else None, vt5[1].strftime('%Y-%m-%dT%H:%M:%S') if vt5 else None)
    },
    "快照有效时间内条目数量占总条目数量的比值": {
        "sorted1.csv": f"{r1*100:.2f}%",
        "sorted5.csv": f"{r5*100:.2f}%"
    },
    "无效条目": invalid_entries,
    "庞加莱回归条目": poincare_regression_entries
}
all_subjects = set()
for incl_end, sec_label in [(True, "包含完结效应条目"), (False, "不包含完结效应条目")]:
    s1 = filter_df(d1.copy(), inv_subs, vt1[1] if vt1 else None, incl_end)
    s5 = filter_df(d5.copy(), inv_subs, vt5[1] if vt5 else None, incl_end)
    data, all_subjects = report_section(data, s1, s5, sec_label, all_subjects)
with open('year_end_report.json', 'w', encoding='utf-8') as report:
    json.dump(data, report, ensure_ascii=False, indent=4)
for subject_id in all_subjects:
    download_cover(subject_id)