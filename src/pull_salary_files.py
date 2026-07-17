import requests
import json
import os
import time

BASE_URL = "https://kuvendiapi.azurewebsites.net/api"
OUTPUT_DIR = "../data/raw/salary"
os.makedirs(OUTPUT_DIR, exist_ok=True)

PAGE_SIZE = 1000

def fetch_all_documents():
    """Paginate through the full /dokumentet catalog."""
    all_docs = []
    skip = 0
    while True:
        url = f"{BASE_URL}/dokumentet?$top={PAGE_SIZE}&$skip={skip}"
        resp = requests.get(url, timeout=60)
        resp.raise_for_status()
        batch = resp.json()

        if isinstance(batch, dict) and "value" in batch:
            batch = batch["value"]

        if not batch:
            break

        all_docs.extend(batch)
        print(f"Fetched {len(all_docs)} documents so far...")
        skip += PAGE_SIZE

        if len(batch) < PAGE_SIZE:
            break

        time.sleep(0.5)

    return all_docs

def is_salary_file(doc):
    name = (doc.get("fileName") or "").lower()
    is_xlsx = name.endswith(".xlsx")
    mentions_salary = "paga" in name
    return is_xlsx and mentions_salary

if __name__ == "__main__":
    cache_path = os.path.join(OUTPUT_DIR, "full_catalog_cache.json")

    if os.path.exists(cache_path):
        print("Loading cached catalog...")
        with open(cache_path, "r", encoding="utf-8") as f:
            all_docs = json.load(f)
    else:
        print("Fetching full document catalog (this may take a while)...")
        all_docs = fetch_all_documents()
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(all_docs, f, ensure_ascii=False, indent=2)

    print(f"Total documents in catalog: {len(all_docs)}")

    salary_docs = [d for d in all_docs if is_salary_file(d)]
    print(f"Matched {len(salary_docs)} salary spreadsheet files.")

    with open(os.path.join(OUTPUT_DIR, "salary_files_metadata.json"), "w", encoding="utf-8") as f:
        json.dump(salary_docs, f, ensure_ascii=False, indent=2)

    print(f"\nDownloading {len(salary_docs)} files...")
    for i, doc in enumerate(salary_docs):
        url = doc.get("url")
        filename = doc.get("fileName")
        doc_id = doc.get("id", "unknown")[:8]
        safe_filename = "".join(c if c.isalnum() or c in " .-_" else "_" for c in filename)[:140]
        unique_filename = f"{doc_id}_{safe_filename}"

        try:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            filepath = os.path.join(OUTPUT_DIR, unique_filename)
            with open(filepath, "wb") as f:
                f.write(resp.content)
            print(f"[{i+1}/{len(salary_docs)}] Downloaded: {unique_filename}")
        except Exception as e:
            print(f"[{i+1}/{len(salary_docs)}] FAILED: {filename} ({e})")

        time.sleep(0.3)
