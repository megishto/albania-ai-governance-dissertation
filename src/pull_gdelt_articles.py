import requests
import json
import os
import time

OUTPUT_DIR = "../data/raw/media"
os.makedirs(OUTPUT_DIR, exist_ok=True)

GDELT_URL = "https://api.gdeltproject.org/api/v2/doc/doc"

# Per proposal: keywords "Diella", "Albania AI", "AKSHI", "Albanian Parliament"
QUERIES = [
    "Diella Albania",
    "Albania AI minister",
    "AKSHI Albania",
    "Albanian Parliament AI",
]

# Per proposal scope: news from September 2025 onward (Diella's appointment)
START_DATE = "20250901000000"
END_DATE = "20260718000000"  # today, per proposal's live-collection approach

def fetch_gdelt(query, max_records=250):
    params = {
        "query": query,
        "mode": "artlist",
        "maxrecords": max_records,
        "format": "json",
        "startdatetime": START_DATE,
        "enddatetime": END_DATE,
        "sort": "datedesc",
    }
    resp = requests.get(GDELT_URL, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()

if __name__ == "__main__":
    all_articles = []

    for query in QUERIES:
        print(f"Querying GDELT for: '{query}'")
        try:
            result = fetch_gdelt(query)
            articles = result.get("articles", [])
            print(f"  Retrieved {len(articles)} articles")
            for a in articles:
                a["matched_query"] = query
            all_articles.extend(articles)
        except Exception as e:
            print(f"  FAILED: {e}")
        time.sleep(2)  # polite pacing between queries

    print(f"\nTotal articles retrieved (before dedup): {len(all_articles)}")

    # Deduplicate by URL, since the same article may match multiple queries
    seen_urls = set()
    deduped = []
    for a in all_articles:
        url = a.get("url")
        if url and url not in seen_urls:
            seen_urls.add(url)
            deduped.append(a)

    print(f"Total unique articles after dedup: {len(deduped)}")

    output_path = os.path.join(OUTPUT_DIR, "gdelt_articles.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(deduped, f, ensure_ascii=False, indent=2)

    print(f"Saved to {output_path}")

    if deduped:
        print("\nSample article:")
        print(json.dumps(deduped[0], ensure_ascii=False, indent=2))