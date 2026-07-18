import json

with open("../data/raw/media/guardian_articles.json", encoding="utf-8") as f:
    data = json.load(f)

print(f"Total articles: {len(data)}")
for a in data:
    headline = a.get("fields", {}).get("headline")
    date = a.get("webPublicationDate")
    section = a.get("sectionName")
    print(f"- [{date}] ({section}) {headline}")