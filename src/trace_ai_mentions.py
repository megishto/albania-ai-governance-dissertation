import os
import re
import csv

"""
Traces every raw occurrence of the "inteligjencë artificiale" phrase family
(the count behind the dissertation's "12 genuine AI mentions" figure,
src/check_ai_vs_intelligence.py) through the sentence-selection and
categorization pipeline (src/sentiment_transcripts.py,
src/categorize_sentiment.py) to explain why only 3 of those mentions ended
up in the ai_specific sentiment category.

Read-only against existing transcripts and the existing cached
outputs/ai_cyber_sentiment.csv. Does not re-translate, re-classify, or
modify any existing file. All logic below is copied verbatim from the
three scripts named above, not imported, so this script has no effect on
them and their own outputs are unchanged.
"""

TEXT_DIR = "../data/processed/transcript_text"
CACHED_SENTIMENT_CSV = "../outputs/ai_cyber_sentiment.csv"
OUTPUT_CSV = "../outputs/ai_mentions_trace.csv"

# --- Exact copy: check_ai_vs_intelligence.py's phrase forms (the "12" count) ---
AI_PHRASE_FORMS_RAW = ["inteligjencë artificiale", "inteligjencën artificiale", "inteligjenca artificiale"]

# --- Exact copy: sentiment_transcripts.py ---
AI_CYBER_KEYWORDS = ["kibernetik", "akshi", "inteligjencë artificiale",
                       "inteligjencën artificiale", "hakerat", "sulm kibernetik"]

def split_sentences(text):
    text = re.sub(r'\s+', ' ', text)
    return re.split(r'(?<=[.!?])\s+', text)

def is_usable_sentence(s, min_words=8, max_words=45):
    s = s.strip()
    word_count = len(s.split())
    if word_count < min_words or word_count > max_words:
        return False, word_count, None
    letters = sum(c.isalpha() for c in s)
    alpha_frac = letters / len(s) if len(s) else 0
    if letters < len(s) * 0.6:
        return False, word_count, alpha_frac
    return True, word_count, alpha_frac

# --- Exact copy: categorize_sentiment.py ---
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


def find_raw_occurrences(text_lower, forms):
    """Reproduce str.count() per form but return (form, char_offset) pairs
    instead of just a count, using the same non-overlapping left-to-right
    semantics as str.count."""
    occurrences = []
    for form in forms:
        start = 0
        while True:
            idx = text_lower.find(form, start)
            if idx == -1:
                break
            occurrences.append((form, idx))
            start = idx + len(form)
    occurrences.sort(key=lambda x: x[1])
    return occurrences


if __name__ == "__main__":
    # Load the cached sentiment set for cross-reference (no re-translation)
    cached_rows = []
    with open(CACHED_SENTIMENT_CSV, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cached_rows.append(row)
    cached_by_file = {}
    for row in cached_rows:
        cached_by_file.setdefault(row["source_file"], []).append(row)

    trace_rows = []
    total_raw_mentions = 0

    for fname in sorted(os.listdir(TEXT_DIR)):
        if not fname.endswith(".txt"):
            continue
        raw_text = open(os.path.join(TEXT_DIR, fname), encoding="utf-8").read()
        raw_text_lower = raw_text.lower()

        # Step 1: raw mentions, exactly mirroring check_ai_vs_intelligence.py
        raw_occs = find_raw_occurrences(raw_text_lower, AI_PHRASE_FORMS_RAW)
        total_raw_mentions += len(raw_occs)

        if not raw_occs:
            continue

        # Step 2: sentence chunks, exactly mirroring sentiment_transcripts.py
        sentences = split_sentences(raw_text)

        for form, offset in raw_occs:
            snippet = raw_text[max(0, offset - 40): offset + len(form) + 40].replace("\n", " ")
            exact_form_as_written = raw_text[offset: offset + len(form)]

            # find which split_sentences() chunk contains this phrase
            matching_sentence = None
            for s in sentences:
                if form in s.lower():
                    # guard against picking the wrong chunk when the same
                    # phrase form appears more than once in this file
                    matching_sentence = s
                    if sentences.count(s) == 1:
                        break
            usable, word_count, alpha_frac = (False, None, None)
            in_keyword_list = form in AI_CYBER_KEYWORDS
            in_cached_287 = False
            assigned_category = None
            fate = None

            if matching_sentence is not None:
                usable, word_count, alpha_frac = is_usable_sentence(matching_sentence)

                if not in_keyword_list:
                    fate = "form not in AI_CYBER_KEYWORDS selection list"
                elif not usable:
                    if word_count is not None and (word_count < 8 or word_count > 45):
                        fate = f"removed by length filter (word_count={word_count})"
                    else:
                        fate = f"removed by alphabetic-ratio filter (alpha_frac={alpha_frac:.2f})" if alpha_frac is not None else "removed by usability filter"
                else:
                    # would have been selected -- check if it's actually in the cache
                    candidates = cached_by_file.get(fname, [])
                    hit = None
                    for c in candidates:
                        if c["original_text"].strip() == matching_sentence.strip():
                            hit = c
                            break
                    if hit is not None:
                        in_cached_287 = True
                        assigned_category = categorize(hit["original_text"])
                        if assigned_category == "ai_specific":
                            fate = "in 287-set, correctly categorized ai_specific"
                        else:
                            fate = f"in 287-set, but reassigned to '{assigned_category}' (priority order matched another category's keyword first)"
                    else:
                        fate = "passed keyword+usability filters but not found in cached CSV (unexplained gap)"
            else:
                fate = "could not locate containing sentence via split_sentences() (possible whitespace/line-break split)"

            sentence_preview = (matching_sentence.strip()[:60] + "...") if matching_sentence else ""

            trace_rows.append({
                "transcript_file": fname,
                "phrase_form_as_written": exact_form_as_written,
                "context_snippet": snippet.strip(),
                "sentence_word_count": word_count,
                "alpha_fraction": round(alpha_frac, 3) if alpha_frac is not None else "",
                "in_ai_cyber_keywords_list": in_keyword_list,
                "in_287_sentence_set": in_cached_287,
                "assigned_category": assigned_category or "",
                "fate": fate,
                "sentence_preview": sentence_preview,
            })

    print(f"Total raw phrase mentions found (3-form count, mirrors check_ai_vs_intelligence.py): {total_raw_mentions}")
    print()
    for r in trace_rows:
        print(r["transcript_file"], "|", repr(r["phrase_form_as_written"]), "|", r["fate"])

    # Summary tally
    print("\n--- Summary tally ---")
    tally = {}
    for r in trace_rows:
        key = r["fate"]
        tally[key] = tally.get(key, 0) + 1
    running_total = 0
    for k, v in tally.items():
        print(f"{v:>3}  {k}")
        running_total += v
    print(f"{running_total:>3}  TOTAL")

    os.makedirs("../outputs", exist_ok=True)
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["transcript_file", "phrase_form_as_written", "context_snippet",
                      "sentence_word_count", "alpha_fraction", "in_ai_cyber_keywords_list",
                      "in_287_sentence_set", "assigned_category", "fate", "sentence_preview"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(trace_rows)
    print(f"\nSaved per-mention trace to {OUTPUT_CSV}")
