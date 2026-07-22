import pandas as pd
from transformers import pipeline
import os

INPUT_FILE = "../data/processed/media_full_text.csv"
CORPUS_FILE = "../data/processed/media_corpus_merged.csv"
OUTPUT_DIR = "../outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SIEBERT_MODEL = "siebert/sentiment-roberta-large-english"
EMOTION_MODEL = "j-hartmann/emotion-english-distilroberta-base"

TRUNCATE_CHARS = 2000  # lead paragraphs, roughly first 350-450 words

if __name__ == "__main__":
    text_df = pd.read_csv(INPUT_FILE)
    meta_df = pd.read_csv(CORPUS_FILE)

    # merge to bring in outlet, date (source_type already in text_df)
    df = text_df.merge(meta_df[["url", "outlet", "date"]], on="url", how="left")

    # sentiment/emotion analysis applies only to news articles
    news_df = df[df["source_type"] == "news"].copy()
    print(f"Running sentiment analysis on {len(news_df)} news articles...")

    print("Loading SiEBERT (sentiment)...")
    sentiment_classifier = pipeline("sentiment-analysis", model=SIEBERT_MODEL, truncation=True)

    print("Loading Emotion DistilRoBERTa...")
    emotion_classifier = pipeline("text-classification", model=EMOTION_MODEL, truncation=True, top_k=1)

    results = []
    for i, row in news_df.iterrows():
        full_text = str(row["full_text"]) if pd.notna(row["full_text"]) else ""
        lead_text = full_text[:TRUNCATE_CHARS]

        if not lead_text.strip():
            print(f"[{i}] SKIPPED (empty text): {row['title'][:50]}")
            continue

        sentiment = sentiment_classifier(lead_text)[0]
        emotion = emotion_classifier(lead_text)[0][0]

        results.append({
            "url": row["url"],
            "title": row["title"],
            "outlet": row["outlet"],
            "date": row["date"],
            "char_count_used": len(lead_text),
            "was_truncated": len(full_text) > TRUNCATE_CHARS,
            "sentiment_label": sentiment["label"],
            "sentiment_score": round(sentiment["score"], 3),
            "emotion_label": emotion["label"],
            "emotion_score": round(emotion["score"], 3),
        })
        print(f"[{i}] {row['title'][:50]}... -> {sentiment['label']} ({sentiment['score']:.2f}), {emotion['label']} ({emotion['score']:.2f})")

    results_df = pd.DataFrame(results)
    output_path = os.path.join(OUTPUT_DIR, "media_sentiment_results.csv")
    results_df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"\n{'='*60}")
    print(f"Sentiment distribution:")
    print(results_df["sentiment_label"].value_counts())
    print(f"\nEmotion distribution:")
    print(results_df["emotion_label"].value_counts())
    print(f"\nArticles truncated (exceeded {TRUNCATE_CHARS} chars): {results_df['was_truncated'].sum()}/{len(results_df)}")
    print(f"\nSaved to {output_path}")
