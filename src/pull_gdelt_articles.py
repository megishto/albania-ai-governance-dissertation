import requests
import json
import os
import time

OUTPUT_DIR = "../data/raw/media"
os.makedirs(OUTPUT_DIR, exist_ok=True)

GDELT_URL = "https://api.gdeltproject.org/api/v2/doc/doc"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

QUERIES = [
    '"Diella"',
    '"Albania" "artificial intelligence"',
    '"AKSHI"',
    '"Albanian Parliament" "AI"',
    '"AKSHI" "arrest"',
    '"Albania" "corruption" "AI minister"',
    '"Albania" "data breach"',
    '"Albania" "parliament" "leak"',
]


START_DATE = "20250901000000"
END_DATE = "20260721000000"

def fetch_gdelt(query, max_records=250, retries=3):
    params = {
        "query": query,
        "mode": "artlist",
        "maxrecords": max_records,
        "format": "json",
        "startdatetime": START_DATE,
        "enddatetime": END_DATE,
        "sort": "datedesc",
    }
    last_error = None
    for attempt in range(retries):
        try:
            resp = requests.get(GDELT_URL, params=params, headers=HEADERS, timeout=30)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            last_error = e
            print(f"    Attempt {attempt+1}/{retries} failed: {e}")
            time.sleep(15)
    raise last_error

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
        time.sleep(15)  # GDELT rate limit: max 1 request per 15 seconds

    print(f"\nTotal articles retrieved (before dedup): {len(all_articles)}")

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