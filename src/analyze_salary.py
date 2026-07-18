import pandas as pd
import os

MERGED_FILE = "../data/processed/salary_mp_merged.csv"
OUTPUT_DIR = "../outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

if __name__ == "__main__":
    df = pd.read_csv(MERGED_FILE)

    print("=" * 60)
    print("OVERALL SUMMARY STATISTICS")
    print("=" * 60)
    print(df[["gross_pay", "net_pay"]].describe())

    print("\n" + "=" * 60)
    print("BY PARTY (mean gross/net pay)")
    print("=" * 60)
    party_stats = df.groupby("partia_normalized")[["gross_pay", "net_pay"]].agg(["mean", "count"])
    print(party_stats)

    print("\n" + "=" * 60)
    print("YEARLY TREND (mean gross/net pay)")
    print("=" * 60)
    yearly = df.groupby("year")[["gross_pay", "net_pay"]].mean()
    print(yearly)

    # Deduction gap analysis (gross - net) / gross, flagging outliers
    df["deduction_pct"] = (df["gross_pay"] - df["net_pay"]) / df["gross_pay"] * 100

    print("\n" + "=" * 60)
    print("DEDUCTION PERCENTAGE — TOP 15 HIGHEST (possible absenteeism pattern)")
    print("=" * 60)
    top_deductions = df.nlargest(15, "deduction_pct")[
        ["full_name", "year", "month", "gross_pay", "net_pay", "deduction_pct"]
    ]
    print(top_deductions.to_string())

    print(f"\nOverall mean deduction %: {df['deduction_pct'].mean():.2f}%")
    print(f"Overall median deduction %: {df['deduction_pct'].median():.2f}%")

    yearly.to_csv(os.path.join(OUTPUT_DIR, "salary_yearly_trend.csv"))
    party_stats.to_csv(os.path.join(OUTPUT_DIR, "salary_by_party.csv"))