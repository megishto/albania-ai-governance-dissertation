import json
import pandas as pd
import os

INPUT_FILE = "../data/raw/parliament/mp_records.json"
OUTPUT_FILE = "../data/processed/mp_records.csv"

os.makedirs("../data/processed", exist_ok=True)

# Maps observed raw party-name variants (lowercased, stripped) to a single
# canonical name. Built from inspecting the raw value_counts() output —
# the underlying API data has inconsistent party naming across records,
# likely due to different data-entry sessions/CMS users over time.
PARTY_NORMALIZATION = {
    "ps": "Partia Socialiste",
    "partia socialiste": "Partia Socialiste",
    "partia socialiste e shqipërisë": "Partia Socialiste",
    "socialiste e shqipërisë": "Partia Socialiste",   # <-- add this line
    "pd-ashm": "Partia Demokratike",
    "partia demokratike": "Partia Demokratike",
    "partia demokratike \"aleanca për ndryshim\"": "Partia Demokratike",
    "partia demokratike - aleanca për ndryshim": "Partia Demokratike",
    "partia socialdemokrate": "Partia Socialdemokrate",
    "socialdemokrate": "Partia Socialdemokrate",
    "psd": "Partia Socialdemokrate",
    "lëvizja socialiste për integrim": "Lëvizja Socialiste për Integrim",
    "lsi": "Lëvizja Socialiste për Integrim",
    "partia lëvizja bashkë": "Lëvizja Bashkë",
    "mundësia": "Partia Mundësia",
    "partia mundësia": "Partia Mundësia",
    "nisma-shb": "Nisma Shqipëria Bëhet",
}


def normalize_party(name):
    """Collapse known raw party-name variants into a single canonical label.
    Falls back to the stripped original if no mapping is found, so unmapped
    values are still visible (not silently dropped) for later inspection."""
    if pd.isna(name):
        return name
    key = name.strip().lower()
    return PARTY_NORMALIZATION.get(key, name.strip())


if __name__ == "__main__":
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        records = json.load(f)

    df = pd.DataFrame(records)

    # Build a clean full name column
    df["full_name"] = (
        df["emer"].str.title() + " " +
        df["atesi"].str.title() + " " +
        df["mbiemer"].str.title()
    )

    # Parse birthdate
    df["ditlindje"] = pd.to_datetime(df["ditlindje"], errors="coerce")

    # Keep the analytically useful columns
    cols = [
        "id", "full_name", "emer", "atesi", "mbiemer", "ditlindje",
        "vendlindje", "email", "qarku", "partia", "status",
        "dateKrijimi", "dateModifikimi"
    ]
    df_clean = df[cols].copy()

    # Add normalized party column alongside the raw one, so both are
    # available for analysis (raw preserved for transparency/audit trail)
    df_clean["partia_normalized"] = df_clean["partia"].apply(normalize_party)

    df_clean.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print(f"Processed {len(df_clean)} MP records.")
    print(f"Saved to {OUTPUT_FILE}")

    print(f"\nRaw party distribution (before normalization):")
    print(df_clean["partia"].value_counts())

    print(f"\nNormalized party distribution:")
    print(df_clean["partia_normalized"].value_counts())

    print(f"\nStatus distribution (1=active, likely):")
    print(df_clean["status"].value_counts())