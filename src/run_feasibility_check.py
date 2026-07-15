import json
from transformers import pipeline

INPUT_FILE = "../data/processed/feasibility_sample.json"
OUTPUT_FILE = "../data/processed/feasibility_results.json"

MODEL_NAME = "cardiffnlp/twitter-xlm-roberta-base-sentiment"

LABEL_MAP = {
    "negative": "negative",
    "neutral": "neutral",
    "positive": "positive",
    "label_0": "negative",
    "label_1": "neutral",
    "label_2": "positive",
}

def normalize_label(raw_label):
    return LABEL_MAP.get(raw_label.lower(), raw_label.lower())

if __name__ == "__main__":
    print(f"Loading model: {MODEL_NAME} (this may take a minute on first run)")
    classifier = pipeline("sentiment-analysis", model=MODEL_NAME)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        sample = json.load(f)

    correct = 0
    total = 0
    disagreements = []

    for item in sample:
        text = item["text"]
        result = classifier(text, truncation=True)[0]
        predicted = normalize_label(result["label"])
        item["model_label"] = predicted
        item["model_confidence"] = round(result["score"], 3)

        total += 1
        if item["manual_label"] == predicted:
            correct += 1
        else:
            disagreements.append({
                "speaker": item["speaker"],
                "text": item["text"],
                "manual": item["manual_label"],
                "model": predicted,
                "confidence": item["model_confidence"]
            })

    agreement = correct / total * 100

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(sample, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*50}")
    print(f"Agreement: {correct}/{total} = {agreement:.1f}%")
    print(f"{'='*50}")
    print(f"\nDisagreements ({len(disagreements)}):")
    for d in disagreements:
        print(f"  [{d['speaker']}] manual={d['manual']} vs model={d['model']} (conf={d['confidence']})")
        print(f"    \"{d['text'][:80]}...\"")

    print(f"\nFull results saved to {OUTPUT_FILE}")