import json

with open("../data/raw/media/gdelt_articles.json", encoding="utf-8") as f:
    data = json.load(f)

print(f"Total articles: {len(data)}")
for a in data:
    print(f"- [{a.get('seendate')}] {a.get('title')} ({a.get('domain')})")