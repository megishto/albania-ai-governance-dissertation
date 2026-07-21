import json

with open("../data/raw/media/gdelt_articles.json", encoding="utf-8") as f:
    data = json.load(f)

# Search for the Seoul visit and EU accession/AKSHI-split articles
# by matching distinctive words from their titles
search_terms = ["seoul", "korea", "accession", "digital solutions", "ads"]

for a in data:
    title = a.get("title", "").lower()
    if any(term in title for term in search_terms):
        print(f"Title: {a.get('title')}")
        print(f"URL: {a.get('url')}")
        print(f"Domain: {a.get('domain')}")
        print(f"Seen date: {a.get('seendate')}")
        print()
        