import pandas as pd

df = pd.read_csv("../data/processed/salary_mp_merged.csv")

subset_cols = ["mp_name_raw", "gross_pay", "net_pay", "month", "year"]
dupes = df[df.duplicated(subset=subset_cols, keep=False)].sort_values(subset_cols)

# check whether duplicates come from different source files or the same file
sample = dupes.head(20)
print(sample[["mp_name_raw", "month", "year", "gross_pay", "source_file"]].to_string())

print()
print("Unique source_file pairs among duplicate name/month/year groups:")
grouped = dupes.groupby(subset_cols)["source_file"].apply(lambda x: list(x.unique()))
print(grouped.head(10))