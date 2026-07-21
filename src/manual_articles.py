"""
manual_articles.py

Structured record of manually-sourced supplementary media articles for
Component 1 (media sentiment analysis).

CONTEXT: Automated collection via GDELT and Guardian APIs was tested
exhaustively across two sessions (11+ Guardian query variations, 8+ GDELT
query variations, systematic manual verification of every returned
result). Both platforms' relevance/phrase matching proved unreliable at
this topic's scale (see logbook 2026-07-20 and 2026-07-21 entries) —
returning large volumes of unrelated results even with quoted exact-phrase
syntax. Confirmed automated corpus: 5 genuinely relevant articles.

This file supplements that automated corpus with manually-searched and
individually verified articles, using the same relevance standard applied
throughout the project (read/verify before including, not just keyword
matched). This is a deliberate, documented methodological step taken in
response to a demonstrated data availability limitation, not an ad hoc
substitute for the planned pipeline.

INCLUSION CRITERIA:
- Must substantively discuss Diella specifically, OR the AKSHI
  corruption/arrest story, OR the parliamentary API/data exposure
  (Ringmast4r/OSINT) story - i.e. directly connected to the dissertation's
  core case study, not just general Albania political coverage.
- English or Albanian language (Albanian articles will be run through the
  same translate+SiEBERT pipeline validated in Component 2).
- Publication date within scope: September 2025 (Diella's appointment)
  onward.

SOURCE TYPES (source_type field):
- "news": straight news reporting, primary corpus for sentiment analysis
  and the media sentiment timeline (Component 1 core objective).
- "opinion_analysis": think-pieces, blog commentary, academic-adjacent
  policy commentary. NOT run through the sentiment timeline alongside
  news - reported/discussed separately as evidence of how the policy/
  expert community interpreted the story, since these pieces have a
  fundamentally different rhetorical register (evaluative/argumentative
  by design) than news reporting (aims for neutral framing).
- "official_source": primary government/institutional sources (e.g. the
  PM office's own Diella page). Used as background/context evidence in
  the report, NOT included in the media sentiment corpus at all.

HOW TO ADD AN ARTICLE:
Append a new dict to MANUAL_ARTICLES below, following the existing
structure. Fill in every field. Leave 'notes' with a brief justification
of relevance/inclusion. Do not duplicate articles already present in the
automated GDELT/Guardian corpus (data/raw/media/*.json).
"""

MANUAL_ARTICLES = [
    {
        "title": "World's first AI minister will eliminate corruption, says Albania's PM",
        "url": "https://www.bbc.co.uk/news/articles/cm2znzgwj3xo",
        "outlet": "BBC",
        "date": "2025-09-12",
        "language": "English",
        "source_type": "news",
        "source_method": "manual_search_prior_bibliography",
        "notes": "Straight news reporting on Diella's appointment announcement. Already cited in proposal bibliography; formally added to media sentiment corpus here.",
    },
    {
        "title": "Albania: AI ChatBot Minister Joins Government",
        "url": "https://gfmag.com/economics-policy-regulation/albania-ai-chatbot-minister-joins-government/",
        "outlet": "Global Finance",
        "date": "2025-09-15",
        "language": "English",
        "source_type": "news",
        "source_method": "manual_search",
        "notes": "Straight news/business-press reporting on the appointment. New find, not previously in bibliography or automated corpus. NOTE: verify exact publication date on page.",
    },
    {
        "title": "Albania Created an 'A.I. Minister' to Curb Corruption. Then Its Developers Were Accused of Graft.",
        "url": "https://www.nytimes.com/2026/01/27/world/europe/albania-ai-corruption-graft.html",
        "outlet": "The New York Times",
        "date": "2026-01-27",
        "language": "English",
        "source_type": "news",
        "source_method": "manual_search",
        "notes": "Major outlet, directly covers the AKSHI Director-General arrest/graft accusation angle - the pivot point central to the dissertation's hypothesis about sentiment shift. Strong, high-value find; not surfaced by either automated API.",
    },
    {
        "title": "Albania puts AI-created 'minister' in charge of public procurement",
        "url": "https://www.theguardian.com/world/2025/sep/11/albania-diella-ai-minister-public-procurement",
        "outlet": "The Guardian",
        "date": "2025-09-11",
        "language": "English",
        "source_type": "news",
        "source_method": "already_in_automated_corpus",
        "notes": "DUPLICATE - already collected via Guardian API automated pipeline (data/raw/media/guardian_articles.json). Listed here for reference only; DO NOT double-count in final merged corpus.",
    },
    {
        "title": "AI can help tackle corruption in Europe - but only if politicians let it do its job",
        "url": "https://blogs.lse.ac.uk/europpblog/2026/05/19/ai-anti-corruption-europe-public-procurement/",
        "outlet": "LSE European Politics and Policy (EUROPP) blog",
        "date": "2026-05-19",
        "language": "English",
        "source_type": "opinion_analysis",
        "source_method": "manual_search",
        "notes": "Academic policy-blog commentary using Diella as a case study within a broader European AI-anticorruption argument. Not straight news; excluded from sentiment timeline, referenced separately as expert commentary.",
    },
    {
        "title": "Artificial intelligence, real politics: What Albania's AI Minister means for EU accession",
        "url": "https://www.iss.europa.eu/publications/commentary/artificial-intelligence-real-politics-what-albanias-ai-minister-means-eu",
        "outlet": "EU Institute for Security Studies (ISS)",
        "date": "2025-09-22",
        "language": "English",
        "source_type": "opinion_analysis",
        "source_method": "manual_search_prior_bibliography",
        "notes": "Institutional policy commentary, already cited in proposal bibliography. Excluded from sentiment timeline; used as expert/policy-analysis evidence in background/discussion sections. NOTE: verify exact publication date on page.",
    },
    {
        "title": "Albania's AI minister: 'avatar democracy' and the spectacle of accountability",
        "url": "https://theloop.ecpr.eu/albanias-ai-minister-avatar-democracy-and-the-spectacle-of-accountability/",
        "outlet": "The Loop (ECPR political science blog)",
        "date": "2025-10-01",
        "language": "English",
        "source_type": "opinion_analysis",
        "source_method": "manual_search",
        "notes": "Academic political-science commentary, coins/uses the framing 'avatar democracy'. Genuinely valuable conceptual framing for the discussion chapter; excluded from sentiment timeline as opinion, not news. NOTE: verify exact publication date on page.",
    },
    {
        "title": "Albania's AI-generated minister is impressive spectacle, questionable reform",
        "url": "https://www.lowyinstitute.org/the-interpreter/albania-s-ai-generated-minister-impressive-spectacle-questionable-reform",
        "outlet": "The Interpreter (Lowy Institute)",
        "date": "2025-09-25",
        "language": "English",
        "source_type": "opinion_analysis",
        "source_method": "manual_search",
        "notes": "Think-tank commentary/analysis. Excluded from sentiment timeline; useful for background/discussion sections on international expert reception. NOTE: verify exact publication date on page.",
    },
    {
        "title": "Copied identities: What went wrong with Albania's AI minister",
        "url": "https://www.dailysabah.com/opinion/op-ed/copied-identities-what-went-wrong-with-albanias-ai-minister",
        "outlet": "Daily Sabah",
        "date": "2026-03-11",
        "language": "English",
        "source_type": "opinion_analysis",
        "source_method": "manual_search",
        "notes": "Op-ed (URL confirms /opinion/op-ed/ section). Likely discusses the Anila Bisha likeness controversy given the 'copied identities' framing. Excluded from sentiment timeline as opinion; valuable for discussion section on the ethics/consent dimension of Diella's construction.",
    },
    {
        "title": "Albanian actor Anila Bisha sues government over use of image, voice for Diella virtual minister",
        "url": "https://www.dw.com/en/albanian-actor-anila-bisha-sues-government-over-use-of-image-voice-for-diella-virtual-minister/a-76090488",
        "outlet": "Deutsche Welle (DW)",
        "date": "2026-02-23",
        "language": "English",
        "source_type": "news",
        "source_method": "manual_search",
        "notes": "Major international broadcaster, straight news reporting. Introduces a distinct governance/ethics dimension not covered elsewhere in the corpus: alleged non-consensual use of a real person's likeness/voice to construct Diella. Directly relevant to the dissertation's governance-claims-vs-reality framing from an image rights/consent angle, separate from the AKSHI procurement corruption angle. High-value, genuinely novel find.",
    },
    {
        "title": "Albania appoints its first ever AI bot as minister in parliament to tackle corruption",
        "url": "https://www.digitaljournal.com/article/albania-appoints-its-first-ever-ai-bot-as-minister-in-parliament-to-tackle-corruption/",
        "outlet": "Digital Journal",
        "date": "2025-09-19",
        "language": "English",
        "source_type": "news",
        "source_method": "manual_search",
        "notes": "Appointment announcement coverage.",
    },
    {
        "title": "Diella / Albania AI Minister incident entry",
        "url": "https://oecd.ai/en/incidents/2026-05-26-d84d",
        "outlet": "OECD AI Incidents Monitor",
        "date": "2026-05-26",
        "language": "English",
        "source_type": "institutional_record",
        "source_method": "manual_search",
        "notes": "NOT a news article - formal entry in the OECD's official AI Incidents Monitor database, an independent institutional record of AI governance incidents. High-value citable evidence that Diella is formally recognised internationally as an AI governance incident. Excluded from sentiment timeline (not prose news content); cite directly as institutional evidence in background/discussion.",
    },
    {
        "title": "Albania government Diella AI minister Anila Bisha (lawsuit coverage)",
        "url": "https://www.politico.eu/article/albania-government-diella-ai-minister-anila-bisha/",
        "outlet": "POLITICO Europe",
        "date": "2026-02-11",
        "language": "English",
        "source_type": "news",
        "source_method": "manual_search",
        "notes": "Major outlet, Bisha likeness lawsuit coverage.",
    },
    {
        "title": "Albania artificial intelligence government minister Diella actor Bisha",
        "url": "https://www.nbcnews.com/world/europe/albania-artificial-intelligence-government-minister-diella-actor-bisha-rcna258727",
        "outlet": "NBC News",
        "date": "2026-02-12",
        "language": "English",
        "source_type": "news",
        "source_method": "manual_search",
        "notes": "Major US outlet, Bisha likeness lawsuit coverage.",
    },
    {
        "title": "Albania: Europe's laboratory where AI combats or hides corruption",
        "url": "https://english.elpais.com/international/2026-02-19/albania-europes-laboratory-where-ai-combats-or-hides-corruption.html",
        "outlet": "El Pais (English)",
        "date": "2026-02-19",
        "language": "English",
        "source_type": "news",
        "source_method": "manual_search",
        "notes": "Major international outlet, substantive framing directly addressing the governance-claims-vs-reality tension central to the dissertation.",
    },
    {
        "title": "Albania's AI turn: a surveillance state without oversight",
        "url": "https://tol.org/client/article/albanias-ai-turn-a-surveillance-state-without-oversight.html",
        "outlet": "Transitions Online (TOL)",
        "date": "2026-04-13",
        "language": "English",
        "source_type": "opinion_analysis",
        "source_method": "manual_search",
        "notes": "Regional (Eastern Europe/Balkans specialist) analysis outlet. Excluded from sentiment timeline as analysis; valuable regional-expert framing on surveillance/oversight angle.",
    },
    {
        "title": "Actress sues Albanian govt for using her image for AI minister",
        "url": "https://balkaninsight.com/2026/02/13/actress-sues-albanian-govt-for-using-her-image-for-ai-minister/bi/",
        "outlet": "Balkan Insight",
        "date": "2026-02-13",
        "language": "English",
        "source_type": "news",
        "source_method": "manual_search",
        "notes": "Different Balkan Insight article from the previously-added AKSHI graft piece - this one covers the Bisha lawsuit specifically. Balkan Insight is your key OSINT-adjacent regional source, already cited in proposal bibliography for the AKSHI arrest coverage.",
    },
    {
        "title": "From AI minister to virtual ombudsman: the Balkans enter era of AI-powered governance",
        "url": "https://www.bta.bg/en/news/balkans/1156491-from-ai-minister-to-virtual-ombudsman-the-balkans-enter-era-of-ai-powered-gover",
        "outlet": "BTA (Bulgarian News Agency)",
        "date": "2026-06-27",
        "language": "English",
        "source_type": "news",
        "source_method": "manual_search",
        "notes": "Regional news wire, broader Balkans AI-governance framing context.",
    },
    {
        "title": "Diella Albania artificial intelligence minister image rights theft",
        "url": "https://europeanconservative.com/articles/news-corner/diella-albania-artificiali-intelligence-minister-image-rights-theft/",
        "outlet": "The European Conservative",
        "date": "2026-02-14",
        "language": "English",
        "source_type": "opinion_analysis",
        "source_method": "manual_search",
        "notes": "Ideologically-branded commentary outlet, not neutral news wire. Excluded from sentiment timeline; if used at all, clearly labeled as partisan commentary, not treated as representative media coverage.",
    },
    {
        "title": "Transparent, incorruptible and unaccountable: inside Albania's AI minister",
        "url": "https://www.mironline.ca/transparent-incorruptible-and-unaccountable-inside-albanias-ai-minister/",
        "outlet": "Montreal Institute for Genocide and Human Rights Studies / MIR Online",
        "date": "2026-02-20",
        "language": "English",
        "source_type": "opinion_analysis",
        "source_method": "manual_search",
        "notes": "Academic-affiliated analysis publication. Title's framing ('transparent, incorruptible and unaccountable') is directly relevant conceptual language for the discussion section.",
    },
    {
        "title": "Albania Diella artificial intelligence corruption (analysis)",
        "url": "https://www.worldpoliticsreview.com/albania-diella-artificial-intelligence-corruption/",
        "outlet": "World Politics Review",
        "date": "2026-01-27",
        "language": "English",
        "source_type": "opinion_analysis",
        "source_method": "manual_search",
        "notes": "Respected foreign-affairs analysis publication (subscription-based). Excluded from sentiment timeline as analysis.",
    },
    {
        "title": "Machinery of government: Albania's new AI-powered minister",
        "url": "https://www.publicfinance.co.uk/analysis/2026/01/machinery-government-albanias-new-ai-powered-minister",
        "outlet": "Public Finance (CIPFA)",
        "date": "2026-01-26",
        "language": "English",
        "source_type": "opinion_analysis",
        "source_method": "manual_search",
        "notes": "UK public-sector finance/governance trade publication. Excluded from sentiment timeline as analysis; valuable for public-administration/governance-professional perspective.",
    },
    {
        "title": "Albania lays groundwork for AI-powered procurement system",
        "url": "https://seenews.com/news/albania-lays-groundwork-for-ai-powered-procurement-system-1294500",
        "outlet": "SeeNews",
        "date": "2026-05-11",
        "language": "English",
        "source_type": "news",
        "source_method": "manual_search",
        "notes": "Southeast Europe business/news wire, straight news coverage of the procurement-AI rollout.",
    },
    {
        "title": "Albania officials house arrest bribery govt contracts",
        "url": "https://www.bhaskarenglish.in/international/news/albania-officials-house-arrest-bribery-govt-contracts-137068653.html",
        "outlet": "Dainik Bhaskar (English)",
        "date": "2026-01-29",
        "language": "English",
        "source_type": "news",
        "source_method": "manual_search",
        "notes": "Indian outlet covering the AKSHI arrest story - useful evidence of the story's international reach beyond Western/European media.",
    },
    {
        "title": "ChatGPT, fix my government?",
        "url": "https://brownpoliticalreview.org/chatgpt-fix-my-government/",
        "outlet": "Brown Political Review",
        "date": "2026-01-28",
        "language": "English",
        "source_type": "opinion_analysis",
        "source_method": "manual_search",
        "notes": "Student political review publication. Excluded from sentiment timeline as opinion/analysis.",
    },
]

if __name__ == "__main__":
    news = [a for a in MANUAL_ARTICLES if a["source_type"] == "news" and a["source_method"] != "already_in_automated_corpus"]
    opinion = [a for a in MANUAL_ARTICLES if a["source_type"] == "opinion_analysis"]
    official = [a for a in MANUAL_ARTICLES if a["source_type"] == "official_source"]
    duplicates = [a for a in MANUAL_ARTICLES if a["source_method"] == "already_in_automated_corpus"]

    print(f"NEW news articles for sentiment corpus: {len(news)}")
    for a in news:
        print(f"  - [{a['date']}] ({a['outlet']}) {a['title']}")

    print(f"\nOpinion/analysis pieces (excluded from sentiment timeline): {len(opinion)}")
    for a in opinion:
        print(f"  - [{a['date']}] ({a['outlet']}) {a['title']}")

    print(f"\nOfficial sources (background use only): {len(official)}")
    for a in official:
        print(f"  - ({a['outlet']}) {a['title']}")

    print(f"\nDuplicates already in automated corpus (excluded here): {len(duplicates)}")
    for a in duplicates:
        print(f"  - {a['title']}")