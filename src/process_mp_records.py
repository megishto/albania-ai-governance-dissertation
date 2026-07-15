import json
import pandas as pd
import os

INPUT_FILE = "../data/raw/parliament/mp_records.json"
OUTPUT_FILE = "../data/processed/mp_records.csv"

os.makedirs("../data/processed", exist_ok=True)

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
    df_clean = df[cols]

    df_clean.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print(f"Processed {len(df_clean)} MP records.")
    print(f"Saved to {OUTPUT_FILE}")
    print(f"\nParty distribution:")
    print(df_clean["partia"].value_counts())
    print(f"\nStatus distribution (1=active, likely):")
    print(df_clean["status"].value_counts())