import pandas as pd

df = pd.read_csv("../outputs/ai_cyber_sentiment.csv")

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

df["category"] = df["original_text"].apply(categorize)

print(df.groupby("category")["sentiment_label"].value_counts())
print()
print(df["category"].value_counts())