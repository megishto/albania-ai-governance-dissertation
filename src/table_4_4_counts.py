import pandas as pd
import os

"""
Reproduces the Table 4.4 category-level sentiment counts for the
dissertation, using the cached, already-translated/classified sentence
set in outputs/ai_cyber_sentiment.csv (produced by sentiment_transcripts.py)
and the category rule from categorize_sentiment.py (reproduced here
verbatim, not imported, since categorize_sentiment.py is a standalone
script with no importable function boundary).

Does not re-translate or re-classify anything — reads the existing cached
CSV only, so results are stable regardless of Google Translate drift.
"""

INPUT_CSV = "../outputs/ai_cyber_sentiment.csv"
OUTPUT_CSV = "../outputs/table_4_4_category_counts.csv"

# Verbatim copy of categorize_sentiment.py's categorize() function,
# for provenance-preserving re-use without importing/modifying that script.
def categorize(text):
    text = text.lower()
    if any(k in text for k in ["hakerat", "sulm kibernetik", "sulmet"]):
        return "attack_specific"
    elif "kibernetik" in text:
        return "cyber_general"
    elif "akshi" in text:
        return "akshi_institutional"
    elif "inteligjencë artificiale" in text or "inteligjencën artificiale" in text:
        return "ai_specific"
    else:
        return "other"

# Independent (non-elif) keyword checks, used only to test whether the
# category definitions overlap if the priority order were removed.
CATEGORY_KEYWORDS = {
    "attack_specific": ["hakerat", "sulm kibernetik", "sulmet"],
    "cyber_general": ["kibernetik"],
    "akshi_institutional": ["akshi"],
    "ai_specific": ["inteligjencë artificiale", "inteligjencën artificiale"],
}

if __name__ == "__main__":
    df = pd.read_csv(INPUT_CSV)
    print(f"Loaded cached sentiment file: {INPUT_CSV}")
    print(f"Total sentences (cached, not re-translated/re-classified): {len(df)}")

    # --- Reproduce the reported 287 / 55% / 45% top-line figures ---
    overall_counts = df["sentiment_label"].value_counts()
    total_n = len(df)
    pos_n = int(overall_counts.get("positive", 0))
    neg_n = int(overall_counts.get("negative", 0))
    other_labels = total_n - pos_n - neg_n
    print("\n--- Overall (reported: 287 total, 158 positive/55%, 129 negative/45%) ---")
    print(f"n={total_n}, positive={pos_n} ({pos_n/total_n:.1%}), "
          f"negative={neg_n} ({neg_n/total_n:.1%}), other_labels={other_labels}")

    # --- Category assignment (mutually exclusive, matches categorize_sentiment.py) ---
    df["category"] = df["original_text"].apply(categorize)

    # --- Overlap check: how many sentences match >1 category's keywords
    #     if priority order were NOT applied ---
    def matched_categories(text):
        t = text.lower()
        return [cat for cat, kws in CATEGORY_KEYWORDS.items() if any(kw in t for kw in kws)]

    df["_matches"] = df["original_text"].apply(matched_categories)
    df["_n_matches"] = df["_matches"].apply(len)
    overlap_n = (df["_n_matches"] > 1).sum()
    zero_match_n = (df["_n_matches"] == 0).sum()

    print(f"\n--- Overlap check ---")
    print(f"Sentences matching >1 category's raw keywords (pre-priority-order): {overlap_n}")
    print(f"Sentences matching 0 category keywords (would only land in 'other'): {zero_match_n}")

    # --- Category-level counts ---
    rows = []
    for cat, group in df.groupby("category"):
        n = len(group)
        pos = int((group["sentiment_label"] == "positive").sum())
        neg = int((group["sentiment_label"] == "negative").sum())
        rows.append({
            "category": cat,
            "n": n,
            "positive": pos,
            "negative": neg,
            "pct_positive": round(pos / n * 100, 1) if n else 0.0,
            "pct_negative": round(neg / n * 100, 1) if n else 0.0,
        })

    result = pd.DataFrame(rows).sort_values("n", ascending=False).reset_index(drop=True)
    print("\n--- Category breakdown ---")
    print(result.to_string(index=False))

    os.makedirs("../outputs", exist_ok=True)
    result.to_csv(OUTPUT_CSV, index=False)
    print(f"\nSaved to {OUTPUT_CSV}")
