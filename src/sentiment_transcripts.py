import os
import re
import json
import time
import pandas as pd
from deep_translator import GoogleTranslator
from transformers import pipeline

TEXT_DIR = "../data/processed/transcript_text"
OUTPUT_DIR = "../outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SIEBERT_MODEL = "siebert/sentiment-roberta-large-english"

AI_CYBER_KEYWORDS = ["kibernetik", "akshi", "inteligjencë artificiale",
                       "inteligjencën artificiale", "hakerat", "sulm kibernetik"]

def split_sentences(text):
    text = re.sub(r'\s+', ' ', text)
    return re.split(r'(?<=[.!?])\s+', text)

def is_usable_sentence(s, min_words=8, max_words=45):
    s = s.strip()
    word_count = len(s.split())
    if word_count < min_words or word_count > max_words:
        return False
    letters = sum(c.isalpha() for c in s)
    if letters < len(s) * 0.6:
        return False
    return True

if __name__ == "__main__":
    print("Loading SiEBERT model...")
    classifier = pipeline("sentiment-analysis", model=SIEBERT_MODEL, truncation=True)
    translator = GoogleTranslator(source="sq", target="en")

    # Collect AI/cyber-relevant sentences specifically
    ai_cyber_sentences = []
    for f in os.listdir(TEXT_DIR):
        if not f.endswith(".txt"):
            continue
        text = open(os.path.join(TEXT_DIR, f), encoding="utf-8").read()
        sentences = split_sentences(text)
        for s in sentences:
            s_lower = s.lower()
            if any(kw in s_lower for kw in AI_CYBER_KEYWORDS) and is_usable_sentence(s):
                ai_cyber_sentences.append({"source_file": f, "text": s.strip()})

    print(f"Found {len(ai_cyber_sentences)} AI/cyber-relevant sentences for sentiment analysis.")

    results = []
    for i, item in enumerate(ai_cyber_sentences):
        try:
            translated = translator.translate(item["text"])
            sentiment = classifier(translated)[0]
            results.append({
                "source_file": item["source_file"],
                "original_text": item["text"],
                "translated_text": translated,
                "sentiment_label": sentiment["label"].lower(),
                "sentiment_confidence": round(sentiment["score"], 3)
            })
            print(f"[{i+1}/{len(ai_cyber_sentences)}] {sentiment['label']} ({sentiment['score']:.2f})")
        except Exception as e:
            print(f"[{i+1}/{len(ai_cyber_sentences)}] FAILED: {e}")
        time.sleep(0.3)

    df = pd.DataFrame(results)
    df.to_csv(os.path.join(OUTPUT_DIR, "ai_cyber_sentiment.csv"), index=False, encoding="utf-8-sig")

    print(f"\n{'='*60}")
    print("SENTIMENT DISTRIBUTION — AI/Cyber discourse sentences")
    print(f"{'='*60}")
    print(df["sentiment_label"].value_counts())
    print(f"\nMean confidence: {df['sentiment_confidence'].mean():.3f}")
    print(f"\nSaved to {OUTPUT_DIR}/ai_cyber_sentiment.csv")