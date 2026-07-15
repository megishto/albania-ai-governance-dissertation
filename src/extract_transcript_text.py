import os
import json
from pypdf import PdfReader

TRANSCRIPT_DIR = "../data/raw/transcripts"
OUTPUT_DIR = "../data/processed/transcript_text"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def fix_mojibake(text):
    """Repair common UTF-8-decoded-as-Latin-1 double encoding."""
    try:
        return text.encode('latin-1').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text  # leave as-is if repair fails on this chunk

def extract_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += fix_mojibake(page_text) + "\n"
    return text

if __name__ == "__main__":
    pdf_files = [f for f in os.listdir(TRANSCRIPT_DIR) if f.endswith(".pdf")]
    print(f"Found {len(pdf_files)} PDFs to process.")

    summary = []

    for i, filename in enumerate(pdf_files):
        pdf_path = os.path.join(TRANSCRIPT_DIR, filename)
        print(f"[{i+1}/{len(pdf_files)}] Extracting: {filename}")

        try:
            text = extract_text(pdf_path)
            out_filename = filename.replace(".pdf", ".txt")
            out_path = os.path.join(OUTPUT_DIR, out_filename)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(text)
            summary.append({"file": filename, "chars": len(text), "status": "ok"})
        except Exception as e:
            print(f"  Failed: {e}")
            summary.append({"file": filename, "chars": 0, "status": f"failed: {e}"})

    with open(os.path.join(OUTPUT_DIR, "extraction_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print("Done. See extraction_summary.json for per-file results.")