import os
import re
import pandas as pd
import json

TEXT_DIR = "../data/processed/transcript_text"
OUTPUT_DIR = "../outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Expanded keyword set covering AI governance, cybersecurity, digital transformation
KEYWORD_GROUPS = {
    "artificial_intelligence": ["inteligjencë artificiale", "inteligjencën artificiale",
                                  "inteligjenca artificiale", "artificial"],
    "intelligence_services": ["inteligjenc"],
    "cybersecurity": ["kibernetik", "siguri kibernetike", "hakerat", "sulm kibernetik"],
    "akshi_institutional": ["AKSHI"],
    "digital_transformation": ["digjitalizim", "qeverisje elektronike", "e-albania", "digjitale"],
}

def extract_year_from_filename(filename):
    m = re.search(r"viti (\d{4})", filename.lower())
    return int(m.group(1)) if m else None

if __name__ == "__main__":
    results = []

    for f in os.listdir(TEXT_DIR):
        if not f.endswith(".txt"):
            continue
        text = open(os.path.join(TEXT_DIR, f), encoding="utf-8").read()
        text_lower = text.lower()
        year = extract_year_from_filename(f)

        row = {"file": f, "year": year}
        for group, keywords in KEYWORD_GROUPS.items():
            count = sum(text_lower.count(kw.lower()) for kw in keywords)
            row[group] = count
        results.append(row)

    df = pd.DataFrame(results).sort_values(["year", "file"])
    df.to_csv(os.path.join(OUTPUT_DIR, "ai_keyword_frequency.csv"), index=False)

    print("Per-file keyword counts:")
    print(df.to_string(index=False))

    print("\n" + "=" * 60)
    print("TOTALS BY YEAR")
    print("=" * 60)
    yearly = df.groupby("year")[list(KEYWORD_GROUPS.keys())].sum()
    print(yearly)

    print("\n" + "=" * 60)
    print("OVERALL TOTALS")
    print("=" * 60)
    print(df[list(KEYWORD_GROUPS.keys())].sum())