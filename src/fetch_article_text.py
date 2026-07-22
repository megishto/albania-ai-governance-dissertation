import pandas as pd
from newspaper import Article
import time
import json
import os

INPUT_FILE = "../data/processed/media_corpus_merged.csv"
OUTPUT_DIR = "../data/processed"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_text(url, retries=2):
    for attempt in range(retries):
        try:
            article = Article(url)
            article.download()
            article.parse()
            return article.text, "ok"
        except Exception as e:
            if attempt == retries - 1:
                return None, f"failed: {e}"
            time.sleep(2)

if __name__ == "__main__":
    df = pd.read_csv(INPUT_FILE)

    results = []
    for i, row in df.iterrows():
        print(f"[{i+1}/{len(df)}] Fetching: {row['title'][:60]}...")
        text, status = fetch_text(row["url"])
        results.append({
            "url": row["url"],
            "title": row["title"],
            "source_type": row["source_type"],
            "full_text": text,
            "char_count": len(text) if text else 0,
            "fetch_status": status,
        })
        print(f"    Status: {status}, chars: {len(text) if text else 0}")
        time.sleep(1)

    results_df = pd.DataFrame(results)
    output_path = os.path.join(OUTPUT_DIR, "media_full_text.csv")
    results_df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"\n{'='*60}")
    print(f"Successful fetches: {(results_df['fetch_status'] == 'ok').sum()}/{len(results_df)}")
    print(f"Saved to {output_path}")

    print("\nFailed fetches (will need manual text entry):")
    failed = results_df[results_df["fetch_status"] != "ok"]
    for _, row in failed.iterrows():
        print(f"  - {row['title'][:60]} ({row['url']})")