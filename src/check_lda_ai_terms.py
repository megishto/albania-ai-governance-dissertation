import pandas as pd
from gensim import corpora
from gensim.models import LdaModel

dictionary = corpora.Dictionary.load("../outputs/lda_dictionary.dict")
lda_model = LdaModel.load("../outputs/lda_model.model")

target_words = ["kibernetik", "kibernetike", "akshi", "sulmet", "hakerat"]

for word in target_words:
    if word in dictionary.token2id:
        word_id = dictionary.token2id[word]
        print(f"\n'{word}' found in vocabulary. Topic distribution:")
        term_topics = lda_model.get_term_topics(word_id, minimum_probability=0.0)
        term_topics_sorted = sorted(term_topics, key=lambda x: -x[1])
        for topic_id, prob in term_topics_sorted[:5]:
            print(f"  Topic {topic_id}: {prob:.4f}")
    else:
        print(f"\n'{word}' NOT in vocabulary (filtered out, likely too rare — "
              f"no_below=10 threshold may have excluded it)")