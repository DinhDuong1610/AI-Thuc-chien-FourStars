from pathlib import PurePosixPath
import os, re, requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

SITES = [
    "https://vtv.vn/dong-su-kien/80-nam-cach-mang-thang-tam-va-quoc-khanh-2-9-1410.htm"
]

OUT_DIR = "round-2-test/de-1-video/assets"
os.makedirs(OUT_DIR, exist_ok=True)

def fetch(url):
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    return r.text

def save_images(html, base):
    soup = BeautifulSoup(html, "html.parser")
    count = 0
    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src")
        if not src: continue
        link = urljoin(base, src)
        if not any(x in link for x in [".jpg", ".jpeg", ".png", ".webp"]): continue
        try:
            b = requests.get(link, timeout=20).content
            ext = PurePosixPath(link).suffix.lower()
            if '?' in ext:
                ext = ext.split('?')[0]
            if not ext or not ext.startswith('.'):
                ext = '.jpg'
            name = re.sub(r"[^a-zA-Z0-9_-]", "_", link[-80:])
            file_path = f"{OUT_DIR}/{name}{ext}"
            with open(file_path, "wb") as f: f.write(b)
            count += 1
        except: pass
    return count

for s in SITES:
    html = fetch(s)
    got = save_images(html, s)
    print(s, "->", got, "images")
