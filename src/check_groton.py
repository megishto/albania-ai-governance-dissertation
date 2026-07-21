import json

with open("../data/raw/media/gdelt_articles.json", encoding="utf-8") as f:
    data = json.load(f)

for a in data:
    if "groton" in a.get("url", "").lower():
        print(json.dumps(a, indent=2))