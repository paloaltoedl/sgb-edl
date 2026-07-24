import requests

BASE_URL = "https://siberguvenlik.gov.tr/api/address/index"


def download(address_type, output_file):
    addresses = set()

    page = 0
    per_page = 9999

    while True:
        print(f"[{address_type}] Page {page} okunuyor...")

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

        models = data.get("models", [])

        if not models:
            break

        for item in models:
            value = item.get("url", "").strip()

            if value:
                addresses.add(value)

        total_pages = data.get("pageCount", 1)

        if page >= total_pages - 1:
            break

        page += 1

    with open(output_file, "w", encoding="utf-8") as f:
        for value in sorted(addresses):
            f.write(value + "\n")

    print(f"[{address_type}] Toplam kayıt: {len(addresses)}")
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
