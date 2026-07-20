import json

with open("../data/raw/media/gdelt_articles.json", encoding="utf-8") as f:
    data = json.load(f)

for a in data:
    title = a.get("title", "")
    if any(kw in title for kw in ["AI Government", "public procurement", "Fake Buyers"]):
        print(f"Title: {title}")
        print(f"URL: {a.get('url')}")
        print()