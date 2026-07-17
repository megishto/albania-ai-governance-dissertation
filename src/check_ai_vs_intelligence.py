import os

text_dir = "../data/processed/transcript_text"
count_ai_phrase = 0
count_bare_inteligjenc = 0

for f in os.listdir(text_dir):
    if not f.endswith(".txt"):
        continue
    text = open(os.path.join(text_dir, f), encoding="utf-8").read().lower()
    count_ai_phrase += text.count("inteligjencë artificiale") + text.count("inteligjencën artificiale") + text.count("inteligjenca artificiale")
    count_bare_inteligjenc += text.count("inteligjenc")

print(f"Bare 'inteligjenc*' count: {count_bare_inteligjenc}")
print(f"Specific 'inteligjenc* artificiale' (AI) count: {count_ai_phrase}")
print(f"Difference (likely intelligence-services or other usage): {count_bare_inteligjenc - count_ai_phrase}")