import os
import re
import pandas as pd
from gensim import corpora
from gensim.models import LdaModel
from gensim.utils import simple_preprocess

TEXT_DIR = "../data/processed/transcript_text"
OUTPUT_DIR = "../outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

N_TOPICS = 15

ALBANIAN_STOPWORDS = set("""
të që dhe në për një me nuk nga është ka të nderuar zoti zonja faleminderit
ju e i të një do jam jemi janë ishte ishin kam keni kanë kemi
por edhe si pra kjo ky kjo këto këta atë ata ajo ai
sepse nëse kur cila cili çfarë kush ku sa shumë më
tim tuaj saj tij tonë tuaja jonë vetë çdo asnjë disa
mund duhet kështu gjithashtu prandaj megjithatë ndërkohë
zonja fjala fjalën lutem procedurë mikrofon ndërhyrje
""".split())

def split_into_documents(text, min_words=15):
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

def preprocess(text):
    tokens = simple_preprocess(text, deacc=False, min_len=3)
    return [t for t in tokens if t not in ALBANIAN_STOPWORDS]

if __name__ == "__main__":
    all_docs = []

    for f in os.listdir(TEXT_DIR):
        if not f.endswith(".txt"):
            continue
        text = open(os.path.join(TEXT_DIR, f), encoding="utf-8").read()
        chunks = split_into_documents(text)
        all_docs.extend(chunks)

    print(f"Total document chunks: {len(all_docs)}")

    print("Preprocessing (tokenizing, removing stopwords)...")
    processed_docs = [preprocess(doc) for doc in all_docs]
    processed_docs = [doc for doc in processed_docs if len(doc) >= 3]
    print(f"Documents after filtering short/empty: {len(processed_docs)}")

    print("Building dictionary and corpus...")
    dictionary = corpora.Dictionary(processed_docs)
    dictionary.filter_extremes(no_below=10, no_above=0.5)
    corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

    print(f"Vocabulary size after filtering: {len(dictionary)}")

    print(f"Training LDA with {N_TOPICS} topics...")
    lda_model = LdaModel(
        corpus=corpus,
        id2word=dictionary,
        num_topics=N_TOPICS,
        random_state=42,
        passes=10,
        alpha="auto",
        per_word_topics=True
    )

    print("\n" + "=" * 60)
    print("LDA TOPICS")
    print("=" * 60)

    topic_rows = []
    for idx, topic in lda_model.print_topics(num_topics=N_TOPICS, num_words=10):
        print(f"\nTopic {idx}: {topic}")
        words = [w.split("*")[1].strip().strip('"') for w in topic.split(" + ")]
        topic_rows.append({"topic_id": idx, "top_words": ", ".join(words)})

    pd.DataFrame(topic_rows).to_csv(os.path.join(OUTPUT_DIR, "lda_topics.csv"), index=False)

    lda_model.save(os.path.join(OUTPUT_DIR, "lda_model.model"))
    dictionary.save(os.path.join(OUTPUT_DIR, "lda_dictionary.dict"))

    print(f"\nSaved LDA topics to {OUTPUT_DIR}/lda_topics.csv")