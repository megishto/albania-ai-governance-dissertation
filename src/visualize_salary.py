import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

MERGED_FILE = "../data/processed/salary_mp_merged.csv"
OUTPUT_DIR = "../outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

sns.set_style("whitegrid")
plt.rcParams["figure.dpi"] = 150

if __name__ == "__main__":
    df = pd.read_csv(MERGED_FILE)
    df["deduction_pct"] = (df["gross_pay"] - df["net_pay"]) / df["gross_pay"] * 100

    # ---------------------------------------------------------------
    # Chart 1: Yearly salary trend (gross vs net)
    # ---------------------------------------------------------------
    yearly = df.groupby("year")[["gross_pay", "net_pay"]].mean().reset_index()

    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.plot(yearly["year"], yearly["gross_pay"], marker="o", linewidth=2, label="Gross pay")
    ax.plot(yearly["year"], yearly["net_pay"], marker="o", linewidth=2, label="Net pay")
    ax.set_title("Mean MP Salary by Year, 2018–2026 (ALL)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Monthly salary (ALL)")
    ax.legend()
    ax.set_xticks(yearly["year"])
    ax.axvspan(2019.5, 2021.5, alpha=0.1, color="gray")
    ax.text(2020.5, ax.get_ylim()[1]*0.95, "No data\n(2020–2021)",
            ha="center", va="top", fontsize=8, color="gray")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "salary_yearly_trend.png"))
    plt.close()
    print("Saved: salary_yearly_trend.png")

    # ---------------------------------------------------------------
    # Chart 2: Party comparison (mean gross pay, with sample size shown)
    # ---------------------------------------------------------------
    party_stats = df.groupby("partia_normalized").agg(
        mean_gross=("gross_pay", "mean"),
        n=("gross_pay", "count")
    ).sort_values("mean_gross", ascending=True).reset_index()

    fig, ax = plt.subplots(figsize=(9, 5.5))
    bars = ax.barh(party_stats["partia_normalized"], party_stats["mean_gross"], color="steelblue")
    ax.set_title("Mean Gross Monthly Salary by Party")
    ax.set_xlabel("Mean gross pay (ALL)")
    for bar, n in zip(bars, party_stats["n"]):
        ax.text(bar.get_width() + 2000, bar.get_y() + bar.get_height()/2,
                f"n={n}", va="center", fontsize=8, color="gray")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "salary_by_party.png"))
    plt.close()
    print("Saved: salary_by_party.png")

    # ---------------------------------------------------------------
    # Chart 3: Deduction % distribution
    # ---------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(9, 5.5))
    sns.histplot(df["deduction_pct"].dropna(), bins=40, ax=ax, color="indianred")
    ax.axvline(df["deduction_pct"].mean(), color="black", linestyle="--", linewidth=1,
               label=f"Mean = {df['deduction_pct'].mean():.1f}%")
    ax.set_title("Distribution of Salary Deduction Percentage (Gross → Net)")
    ax.set_xlabel("Deduction %")
    ax.set_ylabel("Number of salary records")
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "deduction_distribution.png"))
    plt.close()
    print("Saved: deduction_distribution.png")

    print(f"\nAll charts saved to {OUTPUT_DIR}/")