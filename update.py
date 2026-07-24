import requests

BASE_URL = "https://siberguvenlik.gov.tr/api/address/index"

urls = set()

page = 0
per_page = 9999

while True:
    print(f"Page {page} okunuyor...")

    response = requests.get(
        BASE_URL,
        params={
            "type": "url",
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
        url = item.get("url", "").strip()

        if url:
            urls.add(url)

    total_pages = data.get("pageCount", 1)

    if page >= total_pages - 1:
        break

    page += 1

print(f"Toplam URL: {len(urls)}")

with open("url.txt", "w", encoding="utf-8") as f:
    for url in sorted(urls):
        f.write(url + "\n")
