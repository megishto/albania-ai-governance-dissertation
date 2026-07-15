import json
import time
from deep_translator import GoogleTranslator
from transformers import pipeline

INPUT_FILE = "../data/processed/feasibility_sample.json"
OUTPUT_FILE = "../data/processed/feasibility_results_translated.json"

SIEBERT_MODEL = "siebert/sentiment-roberta-large-english"

if __name__ == "__main__":
    print("Loading SiEBERT model...")
    classifier = pipeline("sentiment-analysis", model=SIEBERT_MODEL)

    translator = GoogleTranslator(source="sq", target="en")

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        sample = json.load(f)

    correct = 0
    total = 0
    disagreements = []

    for item in sample:
        try:
            translated = translator.translate(item["text"])
        except Exception as e:
            print(f"Translation failed for: {item['text'][:50]}... ({e})")
            continue

        result = classifier(translated, truncation=True)[0]
        predicted = result["label"].lower()  # SiEBERT outputs POSITIVE/NEGATIVE only, no neutral

        item["translated_text"] = translated
        item["siebert_label"] = predicted
        item["siebert_confidence"] = round(result["score"], 3)

        total += 1
        # Note: SiEBERT is binary (positive/negative), so we can only fairly
        # compare against manual labels that are also positive/negative.
        # Neutral manual labels are excluded from the accuracy count below,
        # but still saved in the output for review.
        if item["manual_label"] in ("positive", "negative"):
            if item["manual_label"] == predicted:
                correct += 1
            else:
                disagreements.append({
                    "speaker": item["speaker"],
                    "original": item["text"],
                    "translated": translated,
                    "manual": item["manual_label"],
                    "model": predicted,
                    "confidence": item["siebert_confidence"]
                })

        time.sleep(0.5)  # be polite to the free translation endpoint

    binary_total = sum(1 for i in sample if i.get("manual_label") in ("positive", "negative"))
    agreement = correct / binary_total * 100 if binary_total else 0

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(sample, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*50}")
    print(f"Agreement (positive/negative only, n={binary_total}): {correct}/{binary_total} = {agreement:.1f}%")
    print(f"{'='*50}")
    print(f"\nDisagreements ({len(disagreements)}):")
    for d in disagreements:
        print(f"  [{d['speaker']}] manual={d['manual']} vs siebert={d['model']} (conf={d['confidence']})")
        print(f"    Original: \"{d['original'][:70]}...\"")
        print(f"    Translated: \"{d['translated'][:70]}...\"")

    print(f"\nFull results saved to {OUTPUT_FILE}")