import pandas as pd
import re
import os

SALARY_FILE = "../data/processed/salary_unified.csv"
MP_FILE = "../data/processed/mp_records.csv"
OUTPUT_FILE = "../data/processed/salary_mp_merged.csv"
UNMATCHED_LOG = "../data/processed/salary_mp_unmatched.csv"

def normalize_name(name):
    """Collapse whitespace, lowercase, strip accents-insensitive comparison
    isn't needed here since Albanian names should match on diacritics too —
    but we do need to handle irregular spacing and case."""
    if pd.isna(name):
        return ""
    name = str(name).strip().lower()
    name = re.sub(r'\s+', ' ', name)  # collapse multiple spaces
    return name

def build_mp_name_lookup(mp_df):
    """Build a lookup from normalized 'first last' and 'last first' name
    strings to MP id, so salary records (first-name-first) can match
    against MP records (split first/father/surname)."""
    lookup = {}
    for _, row in mp_df.iterrows():
        first = normalize_name(row.get("emer", ""))
        last = normalize_name(row.get("mbiemer", ""))
        if not first or not last:
            continue
        # try both orderings since salary files aren't consistent
        lookup[f"{first} {last}"] = row["id"]
        lookup[f"{last} {first}"] = row["id"]
    return lookup

if __name__ == "__main__":
    salary = pd.read_csv(SALARY_FILE)
    mps = pd.read_csv(MP_FILE)

    salary["name_normalized"] = salary["mp_name_raw"].apply(normalize_name)

    lookup = build_mp_name_lookup(mps)

    salary["mp_id"] = salary["name_normalized"].map(lookup)

    matched = salary[salary["mp_id"].notna()]
    unmatched = salary[salary["mp_id"].isna()]

    print(f"Total salary records: {len(salary)}")
    print(f"Matched to MP records: {len(matched)} ({len(matched)/len(salary)*100:.1f}%)")
    print(f"Unmatched: {len(unmatched)} ({len(unmatched)/len(salary)*100:.1f}%)")

    merged = matched.merge(
        mps[["id", "full_name", "partia_normalized", "qarku"]],
        left_on="mp_id", right_on="id", how="left"
    )

    merged.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
    unmatched.to_csv(UNMATCHED_LOG, index=False, encoding="utf-8-sig")

    print(f"\nSaved merged dataset to {OUTPUT_FILE}")
    print(f"Saved unmatched records to {UNMATCHED_LOG} for review")

    print(f"\nSample of unmatched names (for manual review):")
    print(unmatched["mp_name_raw"].drop_duplicates().head(20).to_string())