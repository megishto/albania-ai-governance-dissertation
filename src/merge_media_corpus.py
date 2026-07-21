import json
import os
import pandas as pd
from manual_articles import MANUAL_ARTICLES

OUTPUT_DIR = "../data/processed"
os.makedirs(OUTPUT_DIR, exist_ok=True)

GDELT_FILE = "../data/raw/media/gdelt_articles.json"
GUARDIAN_FILE = "../data/raw/media/guardian_articles.json"

# Manually verified relevant articles from automated collection
# (everything else in the raw JSON files was confirmed irrelevant/noise)
VERIFIED_GDELT_URLS = {
    # naked capitalism / slguardian Diella piece
    "https://www.nakedcapitalism.com/2026/05/ready-or-not-ai-government-is-already-here.html",
    "https://slguardian.org/ready-or-not-ai-government-is-already-here/",
    # Balkan Insight AKSHI graft piece
    "https://balkaninsight.com/2026/04/28/in-an-albanian-graft-case-fake-buyers-friendly-rates-cash-in-crates/bi/",
    # Rama in Seoul -- diplomatic framing of Diella
    "https://tiranaexaminer.com/rama-in-seoul-a-visit-that-brings-two-distant-histories-closer/",
    # Rama on EU accession, AKSHI split into AKSHI/Albanian Digital Solutions
    "https://tiranaexaminer.com/rama-addresses-eu-accession-final-phase-national-development-roadmap-un-strategic-partnership-and-albanian-digital-solutions/",
}

VERIFIED_GUARDIAN_URLS = {
    "https://www.theguardian.com/world/2025/sep/11/albania-diella-ai-minister-public-procurement",
}

def load_verified_automated():
    records = []

    if os.path.exists(GDELT_FILE):
        with open(GDELT_FILE, encoding="utf-8") as f:
            gdelt_data = json.load(f)
        for a in gdelt_data:
            if a.get("url") in VERIFIED_GDELT_URLS:
                records.append({
                    "title": a.get("title"),
                    "url": a.get("url"),
                    "outlet": a.get("domain"),
                    "date": a.get("seendate"),
                    "language": a.get("language"),
                    "source_type": "news",
                    "source_method": "gdelt_api_verified",
                    "notes": "",
                })

    if os.path.exists(GUARDIAN_FILE):
        with open(GUARDIAN_FILE, encoding="utf-8") as f:
            guardian_data = json.load(f)
        for a in guardian_data:
            if a.get("id") and any(vu in a.get("webUrl", "") for vu in VERIFIED_GUARDIAN_URLS):
                records.append({
                    "title": a.get("fields", {}).get("headline"),
                    "url": a.get("webUrl"),
                    "outlet": "The Guardian",
                    "date": a.get("webPublicationDate"),
                    "language": "English",
                    "source_type": "news",
                    "source_method": "guardian_api_verified",
                    "notes": "",
                })

    return records

if __name__ == "__main__":
    automated = load_verified_automated()
    print(f"Verified automated articles loaded: {len(automated)}")

    manual = [
        {
            "title": a["title"],
            "url": a["url"],
            "outlet": a["outlet"],
            "date": a["date"],
            "language": a["language"],
            "source_type": a["source_type"],
            "source_method": a["source_method"],
            "notes": a["notes"],
        }
        for a in MANUAL_ARTICLES
        if a["source_method"] != "already_in_automated_corpus"
    ]
    print(f"Manual articles loaded: {len(manual)}")

    all_records = automated + manual
    df = pd.DataFrame(all_records)

    # dedupe by URL just in case
    before = len(df)
    df = df.drop_duplicates(subset="url")
    after = len(df)
    if before != after:
        print(f"Removed {before - after} duplicate URL(s)")

    output_path = os.path.join(OUTPUT_DIR, "media_corpus_merged.csv")
    df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"\nTotal unique articles in merged corpus: {len(df)}")
    print(f"\nBy source_type:")
    print(df["source_type"].value_counts())
    print(f"\nSaved to {output_path}")