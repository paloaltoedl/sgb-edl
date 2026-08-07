import time
import requests

BASE_URL = "https://siberguvenlik.gov.tr/api/address/index"


def download(address_type, output_file):
    addresses = set()

    page = 1
    per_page = 9999

    while True:
        print(f"[{address_type}] Page {page} okunuyor...")

        data = None

for attempt in range(5):
    try:
        data = None

for attempt in range(5):
    try:
        response = requests.get(
            BASE_URL,
            params={
                "type": address_type,
                "page": page,
                "per-page": per_page
            },
            headers={
                "User-Agent": "GitHub-Actions-EDL"
            },
            timeout=60
        )

        response.raise_for_status()
        data = response.json()
        break

    except requests.RequestException as e:
        print(f"[{address_type}] Sayfa {page} hata: {e}")
        print(f"[{address_type}] 15 saniye sonra tekrar denenecek... ({attempt+1}/5)")
        time.sleep(15)

if data is None:
    raise Exception(f"{address_type} page {page} alınamadı.")
        break

    except requests.RequestException as e:
        print(f"[{address_type}] Sayfa {page} hata: {e}")
        print(f"[{address_type}] 15 sn bekleniyor... ({attempt+1}/5)")
        time.sleep(15)

if data is None:
    raise Exception(f"{address_type} page {page} alınamadı.")

        models = data.get("models", [])
        print(
    f"[{address_type}] page={page} "
    f"count={data.get('count')} "
    f"totalCount={data.get('totalCount')} "
    f"pageCount={data.get('pageCount')}"
)

        if not models:
            break
        print(f"[{address_type}] İlk kayıt: {models[0]['url']}")
        for item in models:
            value = item.get("url", "").strip()

            if value:
                addresses.add(value)

        total_pages = data.get("pageCount", 1)

        if page >= total_pages:
            break

        page += 1

    with open(output_file, "w", encoding="utf-8") as f:
        for value in sorted(addresses):
            f.write(value + "\n")

    print(f"[{address_type}] Unique kayıt: {len(addresses)}")
    return len(addresses)

from datetime import datetime, timezone
from pathlib import Path

url_count = download("url", "url.txt")
domain_count = download("domain", "domain.txt")
ip_count = download("ip", "ip.txt")

line = (
    f"{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')} | "
    f"URL:{url_count} | "
    f"Domain:{domain_count} | "
    f"IP:{ip_count}\n"
)

history = []

if Path("last_update.txt").exists():
    with open("last_update.txt", "r", encoding="utf-8") as f:
        history = f.readlines()

history.append(line)

# Son 10 kayıt kalsın
history = history[-10:]

with open("last_update.txt", "w", encoding="utf-8") as f:
    f.writelines(history)
