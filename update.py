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

url_count = download("url", "url.txt")
domain_count = download("domain", "domain.txt")

with open("last_update.txt", "w", encoding="utf-8") as f:
    f.write(f"Last Update : {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
    f.write(f"URL Count   : {url_count}\n")
    f.write(f"Domain Count: {domain_count}\n")
