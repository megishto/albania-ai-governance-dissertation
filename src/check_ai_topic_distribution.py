import pandas as pd

doc_topics = pd.read_csv("../outputs/bertopic_document_topics.csv")

ai_keywords = ["inteligjenc", "artificial", "kibernetik", "akshi"]
doc_topics["mentions_ai_cyber"] = doc_topics["text"].str.lower().apply(
    lambda t: any(kw in t for kw in ai_keywords)
)

ai_chunks = doc_topics[doc_topics["mentions_ai_cyber"]]
print(f"Chunks mentioning AI/cyber terms: {len(ai_chunks)}")
print("\nTopic distribution of these chunks:")
print(ai_chunks["topic"].value_counts().head(15))