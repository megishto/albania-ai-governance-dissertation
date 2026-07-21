import requests
import json
import os
import time
from dotenv import load_dotenv

# .env lives at repo root, one level up from src/
load_dotenv(dotenv_path="../.env")

API_KEY = os.getenv("GUARDIAN_API_KEY")
if not API_KEY:
    raise RuntimeError("GUARDIAN_API_KEY not found — check .env file exists at repo root")

OUTPUT_DIR = "../data/raw/media"
os.makedirs(OUTPUT_DIR, exist_ok=True)

GUARDIAN_URL = "https://content.guardianapis.com/search"

# Per proposal: keywords "Diella", "Albania AI", "AKSHI", "Albanian Parliament"
QUERIES = [
    '"Diella"',
    '"Albania" AND "artificial intelligence" AND "minister"',
    '"AKSHI"',
    '"Edi Rama" AND "AI"',
    '"AKSHI" AND "arrest"',
    '"Albania" AND "corruption" AND "AI"',
    '"Albania" AND "data" AND "breach"',
]

FROM_DATE = "2025-09-01"  # Diella's appointment, per proposal scope
TO_DATE = "2026-07-21"    # today

def fetch_guardian_page(query, page=1, page_size=50):
    params = {
        "q": query,
        "from-date": FROM_DATE,
        "to-date": TO_DATE,
        "page": page,
        "page-size": page_size,
        "order-by": "newest",
        "show-fields": "headline,trailText,bodyText,byline",
        "api-key": API_KEY,
    }
    resp = requests.get(GUARDIAN_URL, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()

def fetch_all_for_query(query):
    all_results = []
    page = 1
    while True:
        data = fetch_guardian_page(query, page=page)
        response = data.get("response", {})
        results = response.get("results", [])
        total_pages = response.get("pages", 1)

        for r in results:
            r["matched_query"] = query
        all_results.extend(results)

        print(f"  Page {page}/{total_pages}: {len(results)} articles")

        if page >= total_pages:
            break
        page += 1
        time.sleep(0.5)

    return all_results

if __name__ == "__main__":
    all_articles = []

    for query in QUERIES:
        print(f"Querying Guardian API for: '{query}'")
        try:
            results = fetch_all_for_query(query)
            all_articles.extend(results)
        except Exception as e:
            print(f"  FAILED: {e}")
        time.sleep(1)

    print(f"\nTotal articles retrieved (before dedup): {len(all_articles)}")

    # Deduplicate by article ID (Guardian's stable identifier)
    seen_ids = set()
    deduped = []
    for a in all_articles:
        aid = a.get("id")
        if aid and aid not in seen_ids:
            seen_ids.add(aid)
            deduped.append(a)

    print(f"Total unique articles after dedup: {len(deduped)}")

    output_path = os.path.join(OUTPUT_DIR, "guardian_articles.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(deduped, f, ensure_ascii=False, indent=2)

    print(f"Saved to {output_path}")

    if deduped:
        print("\nSample article:")
        sample = deduped[0]
        print(f"  Headline: {sample.get('fields', {}).get('headline')}")
        print(f"  Date: {sample.get('webPublicationDate')}")
        print(f"  Section: {sample.get('sectionName')}")