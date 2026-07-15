import os
import re
import random
import json

TEXT_DIR = "../data/processed/transcript_text"
OUTPUT_FILE = "../data/processed/feasibility_sample.json"

N_SAMPLES = 30
random.seed(42)

MIN_WORDS = 8
MAX_WORDS = 40

# Matches: "Name Surname – " or "Name Surname - " at the start of a speaker turn
# Requires 2-4 capitalized words followed by an en-dash or hyphen
SPEAKER_PATTERN = re.compile(
    r'(?:^|\n)([A-ZÇËÀ-Ÿ][a-zçëà-ÿ\'\.]+(?:\s+[A-ZÇËÀ-Ÿ][a-zçëà-ÿ\'\.]+){1,3})\s*[–\-]\s*'
)

def split_by_speaker(text):
    """Split transcript text into (speaker, speech_text) chunks."""
    matches = list(SPEAKER_PATTERN.finditer(text))
    chunks = []
    for i, m in enumerate(matches):
        speaker = m.group(1).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        speech = text[start:end].strip()
        if speech:
            chunks.append((speaker, speech))
    return chunks

def is_usable_sentence(sentence):
    s = sentence.strip()
    if not s:
        return False
    word_count = len(s.split())
    if word_count < MIN_WORDS or word_count > MAX_WORDS:
        return False
    noise_markers = [
        "Rendi i ditës", "Legjislatura e", "Botim i Kuvendit",
        "REPUBLIKA", "Seanca e", "Drejton seancën", "neni ", "pika "
    ]
    if any(marker in s for marker in noise_markers):
        return False
    letters = sum(c.isalpha() for c in s)
    if letters < len(s) * 0.6:
        return False
    return True

def split_sentences(text):
    text = re.sub(r'\s+', ' ', text)
    return re.split(r'(?<=[.!?])\s+', text)

if __name__ == "__main__":
    txt_files = [f for f in os.listdir(TEXT_DIR) if f.endswith(".txt")]
    all_candidates = []

    for filename in txt_files:
        path = os.path.join(TEXT_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        speaker_chunks = split_by_speaker(text)

        for speaker, speech in speaker_chunks:
            sentences = split_sentences(speech)
            for s in sentences:
                if is_usable_sentence(s):
                    all_candidates.append({
                        "source_file": filename,
                        "speaker": speaker,
                        "text": s.strip()
                    })

    print(f"Total usable candidate sentences with speaker attribution: {len(all_candidates)}")

    sample = random.sample(all_candidates, min(N_SAMPLES, len(all_candidates)))

    for item in sample:
        item["manual_label"] = ""
        item["model_label"] = ""

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(sample, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(sample)} sample sentences to {OUTPUT_FILE}")
    print("\nPreview:")
    for item in sample[:5]:
        print(f"- [{item['speaker']}]: {item['text']}")