import httpx
url = 'https://jirehlov.com/sorted.csv'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}
with httpx.Client(http2=True, verify=False) as client:
    r = client.get(url, headers=headers)
    with open('sorted1.csv', 'wb') as f:
        f.write(r.content)
        print("Successfully downloaded latest sorted.csv.")
