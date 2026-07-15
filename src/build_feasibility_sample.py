import os
import re
import random
import json

TEXT_DIR = "../data/processed/transcript_text"
OUTPUT_FILE = "../data/processed/feasibility_sample.json"

N_SAMPLES = 30
random.seed(7)  # new seed since previous sample was contaminated

MIN_WORDS = 8
MAX_WORDS = 40

# Anchored to the START of a line only (re.MULTILINE), so we don't match
# capitalized names that appear mid-sentence (e.g. "George Washington" quoted
# inside a speech). Requires the name+dash to be the first thing on its line.
SPEAKER_PATTERN = re.compile(
    r'^([A-ZÇËÀ-Ÿ][a-zçëà-ÿ\'\.]+(?:\s+[A-ZÇËÀ-Ÿ][a-zçëà-ÿ\'\.]+){1,3})\s*[–\-]\s*',
    re.MULTILINE
)

def split_by_speaker(text):
    """Split transcript text into (speaker, speech_text) chunks.
    Operates on the RAW text (line breaks preserved) so the ^ anchor works."""
    matches = list(SPEAKER_PATTERN.finditer(text))
    chunks = []
    for i, m in enumerate(matches):
        speaker = m.group(1).strip()
        # sanity filter: reject names containing a stray period followed by
        # a newline artifact, or that are implausibly long
        if "\n" in speaker or len(speaker) > 40:
            continue
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
    text = re.sub(r'[ \t]+', ' ', text)  # collapse spaces/tabs but KEEP newlines out of this step
    text = re.sub(r'\n+', ' ', text)     # now flatten newlines within a speech, safe to do here
    return re.split(r'(?<=[.!?])\s+', text)

# Known real MP surnames pattern check isn't reliable without a reference list,
# so instead we validate against the speakers list already in
# documents_metadata.json — built earlier during transcript collection.
def load_known_speakers():
    meta_path = "../data/raw/transcripts/documents_metadata.json"
    known = set()
    if os.path.exists(meta_path):
        with open(meta_path, "r", encoding="utf-8") as f:
            docs = json.load(f)
        for doc in docs:
            for sp in doc.get("speakers", []):
                known.add(sp.strip())
    return known

if __name__ == "__main__":
    known_speakers = load_known_speakers()
    print(f"Loaded {len(known_speakers)} known speaker names from metadata for validation.")

    txt_files = [f for f in os.listdir(TEXT_DIR) if f.endswith(".txt")]
    all_candidates = []
    rejected_unknown_speaker = 0

    for filename in txt_files:
        path = os.path.join(TEXT_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        speaker_chunks = split_by_speaker(text)

        for speaker, speech in speaker_chunks:
            # Validate speaker against the known list from the API metadata.
            # This catches false-positive matches like "George Washington".
            if known_speakers and speaker not in known_speakers:
                rejected_unknown_speaker += 1
                continue

            sentences = split_sentences(speech)
            for s in sentences:
                if is_usable_sentence(s):
                    all_candidates.append({
                        "source_file": filename,
                        "speaker": speaker,
                        "text": s.strip()
                    })

    print(f"Rejected {rejected_unknown_speaker} chunks with unrecognised speaker names.")
    print(f"Total usable, speaker-validated candidate sentences: {len(all_candidates)}")

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