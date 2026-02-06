import os
import time
import requests
from urllib.parse import quote, urlparse
from datetime import datetime

DOWNLOAD_FOLDER = "static/pic"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

today = datetime.utcnow().strftime("%d/%m/%Y")
encoded_date = quote(today)

edition_id = 1
api_url = (
    "https://epaper.hindustantimes.com/Home/GetAllpages"
    f"?editionid={edition_id}&editiondate={encoded_date}"
)

headers = {
    "User-Agent": "Mozilla/5.0 (GitHub Actions)"
}

response = requests.get(api_url, headers=headers, timeout=20)
response.raise_for_status()
data = response.json()

image_links = []
seen = set()

def extract(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "MrImageUrl" and isinstance(v, str):
                if v not in seen:
                    seen.add(v)
                    image_links.append(v)
            else:
                extract(v)
    elif isinstance(obj, list):
        for i in obj:
            extract(i)

extract(data)

session = requests.Session()
session.headers.update(headers)

for i, url in enumerate(image_links, start=1):
    try:
        r = session.get(url, timeout=20, stream=True)
        r.raise_for_status()

        ext = os.path.splitext(urlparse(url).path)[1].lower()
        if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
            ext = ".jpg"

        filename = f"image_{i}{ext}"
        path = os.path.join(DOWNLOAD_FOLDER, filename)

        with open(path, "wb") as f:
            for chunk in r.iter_content(8192):
                if chunk:
                    f.write(chunk)

        time.sleep(1)

    except Exception as e:
        print("Skipped:", url, e)

print(f"Downloaded {len(image_links)} images")

