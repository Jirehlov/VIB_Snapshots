import requests
from bs4 import BeautifulSoup
import csv
from collections import Counter
import time
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"}
authors = []
for i in range(1, 74):
    url = f"https://bgm.tv/group/qpz/forum?page={i}"
    response = requests.get(url, headers=headers)
    response.encoding = "utf-8"
    time.sleep(1)
    if response.status_code != 200: continue
    soup = BeautifulSoup(response.text, "html.parser")
    author_tags = soup.find_all("td", class_="author")
    for tag in author_tags:
        a = tag.find("a", class_="l")
        if a and "href" in a.attrs:
            bbcode = f"[url=https://bgm.tv{a['href']}] {a.text.strip()} [/url]"
            authors.append(bbcode)
author_counts = Counter(authors)
sorted_author_counts = sorted(author_counts.items(), key=lambda x: x[1], reverse=True)
output_file = "author_frequency.csv"
with open(output_file, mode="w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Author", "Frequency"])
    writer.writerows(sorted_author_counts)
