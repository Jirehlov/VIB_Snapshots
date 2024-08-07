import requests, zipfile, os, urllib3
urllib3.disable_warnings()
r = requests.get("https://api.github.com/repos/bangumi/Archive/releases/tags/archive", verify=False).json()
a = max(r["assets"], key=lambda x: x["created_at"])
p = f"./{a['name']}"
open(p, 'wb').write(requests.get(a["browser_download_url"], verify=False).content)
with zipfile.ZipFile(p, 'r') as z:
    for member in z.namelist():
        z.extract(member, '.')
os.remove(p)
