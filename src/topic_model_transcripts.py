import os
import re
import pandas as pd
from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer
import json

TEXT_DIR = "../data/processed/transcript_text"
OUTPUT_DIR = "../outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def split_into_documents(text, min_words=15):
    """Split transcript text into paragraph-like chunks suitable for
    topic modelling (whole transcripts are too long/heterogeneous for
    single-document topic assignment)."""
    text = re.sub(r'\s+', ' ', text)
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current = []
    word_count = 0
    for s in sentences:
        current.append(s)
        word_count += len(s.split())
        if word_count >= min_words:
            chunks.append(" ".join(current))
            current = []
            word_count = 0
    if current:
        chunks.append(" ".join(current))
    return chunks

if __name__ == "__main__":
    all_docs = []
    doc_sources = []

    for f in os.listdir(TEXT_DIR):
        if not f.endswith(".txt"):
            continue
        text = open(os.path.join(TEXT_DIR, f), encoding="utf-8").read()
        chunks = split_into_documents(text)
        all_docs.extend(chunks)
        doc_sources.extend([f] * len(chunks))

    print(f"Total document chunks for topic modelling: {len(all_docs)}")

    # BERTopic
    print("\nRunning BERTopic...")
    topic_model = BERTopic(language="multilingual", min_topic_size=15, verbose=True)
    topics, probs = topic_model.fit_transform(all_docs)

    topic_info = topic_model.get_topic_info()
    print("\nBERTopic — Top topics found:")
    print(topic_info.head(20).to_string())

    topic_info.to_csv(os.path.join(OUTPUT_DIR, "bertopic_topics.csv"), index=False)

    # Save per-document topic assignment
    doc_topics_df = pd.DataFrame({
        "source_file": doc_sources,
        "text": all_docs,
        "topic": topics
    })
    doc_topics_df.to_csv(os.path.join(OUTPUT_DIR, "bertopic_document_topics.csv"), index=False)

    print(f"\nSaved topic model outputs to {OUTPUT_DIR}/")