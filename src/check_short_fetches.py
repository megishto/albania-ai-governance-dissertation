import pandas as pd

df = pd.read_csv("../data/processed/media_full_text.csv")

# Show the shortest 10 "successful" fetches for manual inspection
short_ones = df[df["fetch_status"] == "ok"].sort_values("char_count").head(10)
for _, row in short_ones.iterrows():
    print(f"=== {row['title'][:60]} ({row['char_count']} chars) ===")
    print(row['full_text'][:300] if pd.notna(row['full_text']) else "[EMPTY]")
    print()