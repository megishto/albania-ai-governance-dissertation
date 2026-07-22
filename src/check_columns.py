import pandas as pd

text_df = pd.read_csv("../data/processed/media_full_text.csv")
print("Columns in media_full_text.csv:")
print(text_df.columns.tolist())