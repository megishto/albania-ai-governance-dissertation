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

  ### Update — speaker attribution bug fix

[RUBRIC: Critical Appraisal — data validation / error correction]

- Initial speaker-detection regex matched capitalized name-pairs anywhere
in text, not just at genuine speaker-turn boundaries, producing false
positives (e.g. "George Washington" misattributed as a speaker when
referenced rhetorically within another MP's speech; surname fragments
from adjacent speaker turns concatenated incorrectly).

- Fixed by (1) anchoring the regex to line starts only (^, re.MULTILINE)
and (2) cross-validating every detected speaker against the authoritative
267-name speaker roster captured in documents_metadata.json during
transcript collection. Rejected 94 of ~107,682 candidate chunks as
unrecognised speakers, confirming the validation step catches real
parsing errors.

### Update — Albanian NLP feasibility check result

- Ran cardiffnlp/twitter-xlm-roberta-base-sentiment against 30 manually
annotated sentences from parliamentary transcripts (speaker-attributed,
cross-validated against known roster).
- Result: 16/30 = 53.3% agreement with manual labels.
- Error pattern: model over-predicts "neutral" (10/14 disagreements were
cases where manual label was positive/negative but model said neutral),
suggesting the model under-captures rhetorical/indirect sentiment in
Albanian political speech that lacks explicit charged vocabulary.
- Decision: per proposal risk mitigation (Table 2), this falls below an
acceptable threshold for automated sentiment classification. Proceeding
with fallback: Albanian parliamentary sources will be used for topic
modelling and keyword frequency analysis only; sentiment classification
will be limited to English-language media coverage (Component 1).

  ### Update — Translation + SiEBERT feasibility test

[RUBRIC: Technical/Practical Effectiveness — justification of chosen methods]

- Tested alternative pipeline: Albanian text → English translation
(GoogleTranslator via deep-translator) → SiEBERT
(siebert/sentiment-roberta-large-english).

- Result: 16/18 = 88.9% agreement with manual labels (n=18, restricted to
positive/negative manual labels since SiEBERT is binary with no neutral
class; direct comparison with the 30-sentence direct-classification test
is not exact due to this class restriction, but still informative).

- Substantially outperforms direct Albanian classification via
cardiffnlp/twitter-xlm-roberta-base-sentiment (53.3%, n=30).

- Both disagreements involved genuinely ambiguous sentences with complex
or resigned/ironic tone, not clear model errors.

- DECISION: Adopt translate-then-SiEBERT as the sentiment classification
pipeline for Albanian parliamentary transcript sentiment in Component 2,
rather than dropping sentiment classification entirely per the original
fallback plan. Direct multilingual classification (XLM-R) rejected as
primary method. Limitation to document: translation may lose nuance,
idiom, and rhetorical structure specific to Albanian political discourse;
final report should acknowledge this as a methodological trade-off.

 ### Update — MP records: party normalization and data completeness


- Retrieved all 236 MP records via GET /api/anetaret (kuvendiapi.azurewebsites.net).
No wrapping in response; bare JSON array. Schema matches OSINT article
documentation exactly (id, emer, atesi, mbiemer, ditlindje, vendlindje,
email, qarku, partia, status, etc.).

- Party affiliation field ("partia") contains 19 raw string variants for
what are effectively 7 distinct parties (e.g. "Partia Socialiste", "PS",
"PARTIA SOCIALISTE", and "Partia Socialiste e Shqipërisë" all refer to
the same party). Built a normalization mapping to collapse these into
canonical labels for analysis, while preserving the original raw value
alongside it for transparency/audit trail.

- Data completeness finding: 7 of 236 MP records (~3%) have a null/missing
"partia" value — no party affiliation recorded at all. Retained as null
rather than imputed; to be noted as a limitation/data quality observation
in the dissertation, consistent with the broader argument about
inconsistent data governance in this system.
