## 2026-07-17 — Topic modelling, keyword analysis, and salary/MP analysis

### Update — Transcript archive time coverage confirmed

- Verified via full document date sort: bisedimet.parlament.al archive
contains 20 transcripts spanning 2022–2024 only (documentDate field is
year-only granularity, not precise session date). No documents exist
covering September 2025 onward (Diella's appointment) as of this check.

- Keyword scan (AKSHI, kibernetik, inteligjenc, artificial) found 665 hits
across all 20 transcripts — substantial pre-existing discourse on
cybersecurity/AKSHI/AI topics predating Diella. Extracted context windows
for manual review (ai_keyword_contexts.txt).

- SCOPE DECISION: Component 2 (parliamentary discourse) serves as a
pre-Diella baseline; Component 1 (media sentiment, GDELT/Guardian)
covers the actual Diella-era timeline from Sept 2025 onward. The two
components are complementary in time coverage rather than overlapping,
which strengthens the before/after narrative structure of the dissertation.


### Update — Salary data collection: 2020–2021 archive gap

- Verified via full document catalog metadata (62,283 documents): no
  salary spreadsheet files exist for 2020 or 2021 in the Parliament's
  document archive, despite full coverage for 2018-2019 and 2022-2026.
- This is a genuine gap in the published archive, not a pipeline filtering
  error — confirmed by searching raw catalog metadata directly for these
  year strings before any parsing logic was applied.
- To be noted as a data completeness limitation in the salary/parliamentary
  dataset section of the report.

  ### Update — Salary data collection and parsing complete

[RUBRIC: Technical/Practical Effectiveness — constraints and limitations]

- Pulled full document catalog (62,283 documents, paginated) from
kuvendiapi.azurewebsites.net/api/dokumentet; filtered client-side for
.xlsx files with "paga" in filename (server-side OData $filter failed
due to incorrect assumed field name). Matched 95 salary spreadsheet files
spanning 2018-2026.

- Data completeness finding: no salary files exist for 2020 or 2021 in the
archive (confirmed via direct metadata search against the full catalog,
not a pipeline filtering artefact). Genuine gap in the published record,
to be noted as a data completeness limitation in the report.

- Built a unified parser handling three distinct spreadsheet structural
eras (2018-2019 simple format, 2022 detailed 29-column format with
itemized bonuses/deductions, 2024+ consolidated 14-column format
reflecting apparent salary law simplification). Header row position and
column names vary by file; parser uses content-based header detection
(searching for "emer") and fuzzy substring column matching rather than
fixed positions/exact names.

- Debugged three real parsing bugs during development: (1) duplicate-named
downloaded files silently overwriting each other, fixed by prefixing
filenames with document ID; (2) a formula-annotation row (e.g. "a, b, 1,
2, 3=1.7%*1") present in some but not all files, initially leaking
through as fake data; (3) duplicate column names within a single source
spreadsheet (one file has "Ndalese per mungesa te paperligjura" listed
twice), causing column selection to return multiple columns instead of
one. All three fixed and verified.

- Final dataset (pre-deduplication pass, see below): 12,551 salary records,
364 unique MP names, 2018-2026 (excluding 2020-2021 gap).


  ### Update — Salary/MP record merge: match rate ceiling identified

- Merged salary dataset against current MP records (236, representing
Legjislatura e 10-të only) via normalized name matching.

- Match rate: 79.6% (9,993/12,551 pre-dedup). Verified the ~20% unmatched
are NOT a matching bug: spot-checked several prominent unmatched names
directly against MP records — zero matches found under any name variant,
confirming these are genuinely former MPs from earlier legislatures not
present in the current /anetaret endpoint snapshot.

- INTERPRETATION: the Parliament API's MP endpoint reflects only the
current legislature's membership, not a historical register. Salary
records extend back to 2018, spanning MP turnover across legislature
changes; party/district-level analysis using the merged dataset is
therefore most reliable for the current legislature's tenure period,
with earlier years having partial MP-attribute coverage.


  ### Update — Salary dataset deduplication fixed, final clean dataset

[RUBRIC: Technical/Practical Effectiveness — development process / error correction]

- Root-caused duplicate salary records to re-uploaded source files (same
month's data uploaded under multiple document IDs — e.g. one month's
data existed under 7 separate document IDs in the catalog).

- Fixed deduplication logic (previously misplaced outside the main
execution block, causing a silent no-op). Final deduplicated dataset:
8,521 salary records (down from 12,551 raw), 79.3% matched to current
MP roster (6,753 records) — match rate stable pre/post dedup, confirming
it reflects genuine historical-MP turnover, not duplicate inflation.

- Yearly trend confirmed: mean gross pay rose from ~158K ALL (2022) to
~311K ALL (2024), consistent with a legal amendment referenced in
spreadsheet metadata (ligji nr.9584, as amended) — worth identifying
the specific amendment for the report.

- Deduction outlier analysis reproduces and extends the OSINT article's
published finding (Bardhi, 41% deduction, Jan 2026): found one MP (F.H) record
with a 71.4% deduction on a full 310,250 ALL gross salary (Feb 2024), a
more extreme case than the OSINT baseline, from independently parsed
data. [Individual MP name withheld per ethics commitment (Proposal,
Section 3.3: "individual sensitive information such as salaries will
not be published"); identifying detail retained in the raw dataset only,
which is excluded from version control via .gitignore, not in this
logbook or the final report.]


### Update — AI governance keyword frequency analysis (2022-2024 transcripts)

- Cybersecurity mentions spike sharply in 2022 (223 hits) vs 2023 (49) and
2024 (96) — consistent with parliamentary response to the July 2022
Iranian HomeLand Justice attack on AKSHI (CISA/FBI AA22-264A, Sept 2022).

- AI/artificial intelligence mentions rise steadily pre-Diella: 32 (2022)
-> 66 (2023) -> 148 (2024), indicating AI was an increasingly live topic
in parliamentary discourse well before the Sept 2025 appointment.
[CORRECTED BELOW — see "AI vs intelligence-services keyword conflation"
entry: these AI mention counts were conflating AI with intelligence-
services usage of "inteligjencë". Genuine AI-specific count is 12,
not 148.]

- Outlier: 2024_nr_4.txt contains 87 AI mentions (vs. next-highest 27) —
flagged for manual reading to identify the specific session/topic driving
this concentration.

- Data protection/privacy terminology appears only once across the entire
20-transcript corpus (~2022-2024) — notable near-total absence given the
scale of personal data later exposed via the same institutions' APIs.


### Update — 2024_nr_4.txt outlier investigated

- Manual review of context around AI mentions in 2024_nr_4.txt (87 hits,
outlier vs. corpus average) shows AI referenced within a broader
rhetorical framing about public administration modernization and EU
alignment (e.g. "carbon-neutral economy, innovation, competition, and
artificial intelligence happening across the world") — aspirational
language listing AI as one item among global trends, not substantive
policy discussion of AI governance or deployment.

- Tentative interpretation: pre-Diella AI discourse in parliament may be
predominantly rhetorical/aspirational rather than policy-substantive —
worth confirming via topic modelling and additional manual spot-checks
before treating as a firm finding.


### Update — BERTopic modelling on 2022-2024 transcripts, and a keyword conflation correction

[RUBRIC: Critical Appraisal — methodological self-correction, triangulation of methods]


Initial run. Ran BERTopic on 138,164 sentence-chunk documents split from
the 20 transcripts (multilingual sentence embeddings, min_topic_size=15).
Produced 18 substantive topics plus a large outlier cluster (topic -1,
73,970 chunks / ~54% of corpus — normal for parliamentary transcripts full
of procedural filler). Topics are coherent and cover expected parliamentary
domains: education, healthcare, PM/ministerial accountability, pensions,
agriculture, Kosovo/Serbia relations, EU integration, energy, corruption,
local governance, tourism, water infrastructure, and several
procedural/speaker-turn clusters. On first pass, scanning only the largest
~19 topics by size, none appeared to be specifically about AI, cybersecurity,
or AKSHI, despite 665 keyword hits found in the earlier frequency analysis —
initial (and, as below, incorrect) interpretation was that AI/cyber
terminology was scattered rhetorically across other topics rather than
forming a distinct cluster.

Correction 1 — topic clusters do exist, just outside the initial top-20
view. Cross-checked which topics the 640 AI/cyber-keyword-matching chunks
actually fell into. Found genuine, coherent clusters further down the
topic list:


Topic 76 (164 chunks): "kibernetike, kibernetik, sistemet, sulmet" —
direct cyberattack/cybersecurity incident discussion.
Topic 179 (62 chunks): "kibernetike, sulmet, hakerat, iranianë, sigurisë"
— explicitly references Iranian hackers, almost certainly discussion of
the 2022 HomeLand Justice attack on AKSHI (CISA/FBI AA22-264A).
Topic 277 (37 chunks): "akshi, informacionit, sistemeve, agjenci,
teknologjisë" — AKSHI discussed in an institutional/technology-agency
governance context.
Topic 42 (339 chunks): "armatosura, ushtarake, forcave, mbrojtjes,
sigurisë, inteligjencës" — armed forces/defense/intelligence-services
context.
Topic 63 (203 chunks): "albania, online, digjitale, shërbimeve,
elektronike, akep" — broader digital services/e-government discourse.


Correction 2 — AI vs. intelligence-services keyword conflation
(important). Topic 42's presence prompted a check of whether the
original "inteligjenc*" keyword count was conflating artificial
intelligence with intelligence services (SHISH, military/defense
intelligence). Verified directly: of 177 total "inteligjenc*" occurrences
across the corpus, only 12 are the specific phrase "inteligjencë
artificiale" (AI). The remaining 165 (93%) refer to intelligence services
in a defense/security sense, unrelated to AI. The original keyword
frequency analysis (246 "artificial_intelligence" hits) substantially
overcounted true AI references as a result.

Revised finding. Genuine AI-specific discourse in the 2022-2024
parliamentary transcripts is minimal (12 mentions total across 20
transcripts), while cybersecurity discourse is substantial and well-defined
(226 chunks across two BERTopic clusters, one explicitly referencing
Iranian hackers). This sharpens the dissertation's core contrast:
parliament engaged substantively with cybersecurity/infrastructure security
following the 2022 attack, but essentially not with artificial intelligence
as a governance topic, prior to Diella's September 2025 appointment.

Methodological note. This sequence — an initial keyword-only finding,
refined by cross-checking against topic modelling, then further corrected
by a targeted phrase-level check — demonstrates the value of triangulating
methods rather than trusting a single automated count. A keyword-only
analysis without the topic-modelling cross-check would have significantly
overstated pre-Diella AI discourse. The keyword frequency script
(analyze_ai_keywords.py) has been updated to search the precise phrase
"inteligjencë artificiale" rather than the bare stem "inteligjenc", and to
track intelligence-services mentions as a separate category rather than
folding them into the AI count.



### Update — LDA topic modelling and BERTopic vs. LDA comparison

[RUBRIC: Critical Appraisal — comparative method evaluation]


- Ran LDA (gensim, 15 topics, custom Albanian stopword list, no_below=10/
no_above=0.5 vocabulary filtering) on the same 138,164 document chunks
used for BERTopic. Topics are broader and less semantically coherent
than BERTopic's — several (e.g. Topic 9: "këtë, sot, gjithë, vetëm, unë,
duke") are dominated by generic/procedural language rather than
identifiable subject matter, versus BERTopic's cleanly interpretable
domain-specific clusters (education, healthcare, cybersecurity, etc.).

- Directly tested whether LDA captured the cybersecurity/AKSHI signal that
BERTopic identified (Topics 76, 179, 277). Checked topic-term
associations for "kibernetik", "kibernetike", "akshi", "sulmet",
"hakerat" directly in the trained LDA model. Result: essentially no
meaningful association — "kibernetik", "sulmet", "hakerat" show zero
topic probability in any topic; "kibernetike" and "akshi" show only
trace association (0.5% and 0.2% respectively) with a single generic
topic. LDA completely failed to surface this discourse cluster.

- METHODOLOGICAL FINDING (directly serving proposal's stated comparison
objective): BERTopic's embedding-based approach successfully identified
a real, coherent, substantively important discourse cluster
(cybersecurity/AKSHI, ~226 of 138,164 chunks, 0.16% of corpus) that
LDA's pure word-co-occurrence approach missed entirely, likely because
the topic's raw frequency was too low relative to LDA's statistical
requirements, despite being semantically coherent and substantively
significant. This supports the methodological choice of BERTopic as
primary, with LDA valuable specifically as a demonstration of
embedding-based methods' advantage for identifying low-frequency but
semantically distinct topics in heterogeneous parliamentary corpora.


  ### Update — Sentiment analysis on AI/cyber-relevant transcript sentences

- Applied validated translate+SiEBERT pipeline to 287 sentences from the
20 transcripts matching AI/cyber keywords (kibernetik, akshi,
inteligjencë artificiale, hakerat, sulm kibernetik). Mean classification
confidence 0.991.

- Overall: 158 positive (55%) vs 129 negative (45%) — near-even split,
counter to initial expectation of a negative skew.

- Breaking down by keyword category reveals a more precise pattern:
  - AKSHI-institutional mentions (n=79): 62% negative — consistent with
    AKSHI's later corruption scandal; institutional discussion already
    trends critical pre-arrest.
  - Attack-specific mentions (hakerat/sulm/sulmet, n=56): near-even split
    (30 negative/26 positive) — worth further investigation; may reflect
    government-defensive vs opposition-critical framing of the same
    incident (untested — would require speaker-party cross-reference).
  - General cybersecurity discourse (n=149, largest category): 66%
    positive — consistent with aspirational/modernization framing observed
    in manual review of the 2024_nr_4.txt outlier.
  - AI-specific (n=3): sample too small for meaningful interpretation
    (only 3 of 12 total genuine AI mentions met the 8-45 word length
    filter for sentiment classification).
- REVISED INTERPRETATION: pre-Diella parliamentary discourse on cyber/AI
topics is not uniformly negative or positive but category-dependent —
institutional accountability (AKSHI) skews critical, general policy
rhetoric skews aspirational, and specific incident discussion is
genuinely contested. This nuance would be lost in an aggregate-only
reporting of the 158/129 split.
