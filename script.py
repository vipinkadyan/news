import os
import time
import requests
from urllib.parse import quote, urlparse
from datetime import datetime

# ================= CONFIG =================
DATA_DIR = os.getenv("DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
PIC_FOLDER = os.path.join(DATA_DIR, "pic")
os.makedirs(PIC_FOLDER, exist_ok=True)

URL_FILE = os.path.join(DATA_DIR, "weblink.txt")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Render Bot)",
    "Accept": "image/*,*/*;q=0.8"
}
# =========================================

today = datetime.utcnow().strftime("%d/%m/%Y")
encoded_date = quote(today)

edition_id = 1
api_url = (
    "https://epaper.hindustantimes.com/Home/GetAllpages"
    f"?editionid={edition_id}&editiondate={encoded_date}"
)

response = requests.get(api_url, headers=HEADERS, timeout=20)

if response.status_code != 200:
    raise SystemExit(f"API failed: {response.status_code}")

data = response.json()

image_links = []
seen_links = set()


def extract_image_urls(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "MrImageUrl" and isinstance(v, str):
                if v not in seen_links:
                    seen_links.add(v)
                    image_links.append(v)
            else:
                extract_image_urls(v)
    elif isinstance(obj, list):
        for i in obj:
            extract_image_urls(i)


extract_image_urls(data)

with open(URL_FILE, "w", encoding="utf-8") as f:
    for link in image_links:
        f.write(link + "\n")

session = requests.Session()
session.headers.update(HEADERS)

for idx, url in enumerate(image_links, start=1):
    try:
        r = session.get(url, timeout=20, stream=True)
        r.raise_for_status()

        ext = os.path.splitext(urlparse(url).path)[1].lower()
        if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
            ext = ".jpg"

        filename = f"image_{idx}{ext}"
        filepath = os.path.join(PIC_FOLDER, filename)

        with open(filepath, "wb") as img:
            for chunk in r.iter_content(8192):
                if chunk:
                    img.write(chunk)

        time.sleep(1)

    except Exception as e:
        print(f"Skipped {url} | {e}")

print(f"Saved {len(image_links)} images to {PIC_FOLDER}")
