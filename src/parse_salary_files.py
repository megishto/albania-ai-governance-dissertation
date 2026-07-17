import os
import re
import pandas as pd
import glob

INPUT_DIR = "../data/raw/salary"
OUTPUT_FILE = "../data/processed/salary_unified.csv"
LOG_FILE = "../data/processed/salary_parse_log.json"

MONTH_MAP = {
    "janar": 1, "shkurt": 2, "mars": 3, "prill": 4, "maj": 5, "qershor": 6,
    "korrik": 7, "gusht": 8, "shtator": 9, "tetor": 10, "nentor": 11,
    "nëntor": 11, "dhjetor": 12,
}

def find_header_row(raw_df, max_scan=15):
    """Scan the first N rows for the real header — identified by containing
    a name-related column label (present in every observed format)."""
    for i in range(min(max_scan, len(raw_df))):
        row_values = raw_df.iloc[i].astype(str).str.lower()
        if row_values.str.contains("emer").any():
            return i
    return None

def is_formula_row(raw_df, row_idx):
    """Detect the 'a, b, 1, 2, 3=1.7%*1...' style annotation row."""
    row = raw_df.iloc[row_idx]
    non_null = row.dropna()
    if len(non_null) == 0:
        return False

    non_null_str = non_null.astype(str).str.strip()
    non_null_str = non_null_str[non_null_str != "nan"]
    if len(non_null_str) == 0:
        return False

    formula_pattern = re.compile(r'^[a-z0-9\.\+\-\*/=%\s]{1,20}$', re.IGNORECASE)
    matches = non_null_str.apply(lambda x: bool(formula_pattern.match(x)))
    return matches.mean() > 0.6

COLUMN_ALIASES = {
    "mp_name": ["emer mbiemer", "emër mbiemer", "emer", "emri"],
    "position": ["emertesa e pozicionit", "pozicioni"],
    "gross_pay": ["paga bruto", "paga  bruto"],
    "net_pay": ["paga neto", "paga  neto", "pagё neto"],
    "deductions_total": ["shuma e ndalesave"],
    "absence_penalty": ["ndalese", "penalitet"],
}

def map_columns(columns):
    mapped = {}
    for target, aliases in COLUMN_ALIASES.items():
        for col in columns:
            col_norm = str(col).lower().strip()
            if any(alias in col_norm for alias in aliases):
                mapped[target] = col
                break
    return mapped

def extract_month_year_from_filename(filename):
    fname_lower = filename.lower()
    year_match = re.search(r"(20\d{2})", fname_lower)
    year = int(year_match.group(1)) if year_match else None

    month = None
    for name, num in MONTH_MAP.items():
        if name in fname_lower:
            month = num
            break

    return month, year

def deduplicate_columns(columns):
    seen = {}
    result = []
    for col in columns:
        col_str = str(col)
        if col_str in seen:
            seen[col_str] += 1
            result.append(f"{col_str}__{seen[col_str]}")
        else:
            seen[col_str] = 0
            result.append(col_str)
    return result

def parse_salary_file(filepath):
    raw = pd.read_excel(filepath, header=None)
    header_idx = find_header_row(raw)

    if header_idx is None:
        return None, "no_header_found"

    data_start = header_idx + 1
    if is_formula_row(raw, data_start):
        data_start += 1

    headers = deduplicate_columns(raw.iloc[header_idx])
    data = raw.iloc[data_start:].copy()
    data.columns = headers
    data = data.dropna(how="all")

    col_map = map_columns(data.columns)

    if "mp_name" not in col_map:
        return None, "no_name_column_matched"

    result = pd.DataFrame()
    result["mp_name_raw"] = data[col_map["mp_name"]]
    for target in ["position", "gross_pay", "net_pay", "deductions_total", "absence_penalty"]:
        if target in col_map:
            result[target] = data[col_map[target]]
        else:
            result[target] = None

    result = result[result["mp_name_raw"].notna()]
    result = result[~result["mp_name_raw"].astype(str).str.lower().isin(["nan", "emer mbiemer"])]

    month, year = extract_month_year_from_filename(os.path.basename(filepath))
    result["month"] = month
    result["year"] = year
    result["source_file"] = os.path.basename(filepath)

    return result, "ok"

if __name__ == "__main__":
    files = glob.glob(os.path.join(INPUT_DIR, "*.xlsx"))
    print(f"Found {len(files)} salary files to parse.")

    all_results = []
    log = []

    for f in files:
        try:
            df, status = parse_salary_file(f)
            log.append({"file": os.path.basename(f), "status": status,
                        "rows_extracted": len(df) if df is not None else 0})
            if df is not None:
                all_results.append(df)
        except Exception as e:
            log.append({"file": os.path.basename(f), "status": f"error: {e}", "rows_extracted": 0})

    if all_results:
        unified = pd.concat(all_results, ignore_index=True)
        unified.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
        print(f"\nWrote {len(unified)} salary records to {OUTPUT_FILE}")
    else:
        print("\nNo records extracted.")

    import json
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

    ok_count = sum(1 for l in log if l["status"] == "ok")
    print(f"\nParse summary: {ok_count}/{len(files)} files parsed successfully.")
    print("Failures:")
    for l in log:
        if l["status"] != "ok":
            print(f"  {l['file']}: {l['status']}")