import requests
import json
import os

OUTPUT_DIR = "../data/raw/parliament"
os.makedirs(OUTPUT_DIR, exist_ok=True)

BASE_URL = "https://kuvendiapi.azurewebsites.net/api"

def fetch_mps():
    resp = requests.get(f"{BASE_URL}/anetaret", timeout=30)
    resp.raise_for_status()
    return resp.json()

if __name__ == "__main__":
    print("Fetching MP records...")
    mps = fetch_mps()

    # Handle either a bare list or a wrapped {"value": [...]} OData-style response
    if isinstance(mps, dict) and "value" in mps:
        records = mps["value"]
    else:
        records = mps

    print(f"Retrieved {len(records)} MP records.")

    out_path = os.path.join(OUTPUT_DIR, "mp_records.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    print(f"Saved to {out_path}")

    # quick preview
    if records:
        print("\nSample record:")
        print(json.dumps(records[0], ensure_ascii=False, indent=2))