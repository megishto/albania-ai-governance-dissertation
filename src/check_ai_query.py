import json

with open("../data/raw/media/gdelt_articles.json", encoding="utf-8") as f:
    data = json.load(f)

ai_query_articles = [a for a in data if a.get("matched_query") == '"Albania" "artificial intelligence"']
print(f"Total: {len(ai_query_articles)}")
for a in ai_query_articles[:10]:
    print(f"- {a.get('title')} ({a.get('domain')})")