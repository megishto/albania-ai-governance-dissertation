## 2026-07-15 — Parliamentary transcript collection

- Verified bisedimet.parlament.al/health: status "ok", production environment,
  memory at 95% (33421704/35155968) — consistent with OSINT baseline
  (Ringmast4r, 2026), confirming the endpoint remains unsecured and
  unmaintained since discovery in April 2026.
- Retrieved full document list via GET /api/documents: 20 transcripts
  confirmed, ocrStatus=COMPLETED for all, spanning 2022 (nr. 1,3,4,5,7,8),
  2023 (nr. 1-6), 2024 (nr. 2,3,4,6,7,8,9,10).
- Downloaded all 20 PDFs (~24MB total) plus full metadata JSON (includes
  per-document speaker lists, ~99KB) to data/raw/transcripts/ via
  src/pull_transcripts.py.
- No authentication bypassed; all requests were unauthenticated GET requests
  per documented methodology (Ringmast4r, 2026).
- Note: coverage has gaps (e.g. no 2022 nr. 2 or 6) — matches the "20 of
  presumably more" framing in the source article; treat as full available
  archive, not necessarily complete parliamentary record.

  ### Update — text extraction

- Extracted embedded OCR text layer from all 20 PDFs using pypdf
  (src/extract_transcript_text.py). Yield: ~800K–1.9M characters per
  transcript, all extractions status "ok".
- Identified and corrected a Latin-1/UTF-8 double-encoding bug (mojibake)
  in initial extraction — Albanian diacritics (ë, ç) were corrupted
  (e.g. "tÃ«" instead of "të"). Fixed by re-encoding extracted text as
  latin-1 then decoding as utf-8. Verified via direct Python read
  (encoding='utf-8') — confirmed clean text with correct diacritics.
  Note: PowerShell's terminal (Get-Content) still visually displays
  the corrected files incorrectly due to console encoding settings,
  unrelated to the underlying file content, which is correct UTF-8.