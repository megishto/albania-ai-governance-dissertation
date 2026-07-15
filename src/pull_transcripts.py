import requests
import json
import os
import time

BASE_URL = "https://bisedimet.parlament.al/api"
OUTPUT_DIR = "../data/raw/transcripts"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_document_list():
    """Fetch the list of available transcripts."""
    resp = requests.get(f"{BASE_URL}/documents", timeout=30)
    resp.raise_for_status()
    payload = resp.json()
    if not payload.get("success"):
        raise RuntimeError("API returned success=false")
    return payload["data"]["documents"]

def download_document(doc_id, filename):
    """Download a single transcript PDF."""
    url = f"{BASE_URL}/documents/{doc_id}/view"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(resp.content)
    return filepath

if __name__ == "__main__":
    print("Fetching document list...")
    documents = get_document_list()

    # Save the full metadata list for reference (includes speakers, dates, ocrStatus etc.)
    with open(os.path.join(OUTPUT_DIR, "documents_metadata.json"), "w", encoding="utf-8") as f:
        json.dump(documents, f, ensure_ascii=False, indent=2)

    print(f"Found {len(documents)} documents. Downloading...")

    for i, doc in enumerate(documents):
        doc_id = doc.get("id")
        title = doc.get("title", f"doc_{doc_id}")
        safe_title = "".join(c if c.isalnum() or c in " -_" else "_" for c in title)[:80].strip()
        filename = f"{doc_id}_{safe_title}.pdf"

        print(f"[{i+1}/{len(documents)}] {title} (ocrStatus={doc.get('ocrStatus')})")
        try:
            download_document(doc_id, filename)
        except Exception as e:
            print(f"  Failed: {e}")

        time.sleep(1)  # polite delay, no need to hammer the server

    print("Done.")