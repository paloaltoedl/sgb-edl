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


download("url", "url.txt")
download("domain", "domain.txt")
