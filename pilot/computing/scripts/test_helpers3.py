"""RUN3 step 2: test page_text3.py's --check on one real example of each source type.
Writes raw/helper_tests3.jsonl (url, type, quote, found, record date or error; no page text).
Usage: python3 -I scripts/test_helpers3.py"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import page_text3  # noqa: E402

HERE = Path(__file__).resolve().parent.parent
TESTS = [
    ("html (Wikipedia, via API)", "https://en.wikipedia.org/wiki/Kiva_Systems", "Kiva Systems", None),
    ("html (ethw.org)", "https://ethw.org/Milestones:List_of_IEEE_Milestones", "IEEE Milestones", None),
    ("html (PubMed abstract page)", "https://pubmed.ncbi.nlm.nih.gov/31019317/",
     "Speech synthesis from neural decoding of spoken sentences", None),
    ("archive.org scanned magazine (OCR)", "https://archive.org/details/computerworld1940unse",
     "is being developed specifically for the security business. : The mobile robot, equipped with ultrasonic sensors", None),
    ("PDF (bitsavers)", "http://bitsavers.org/pdf/dec/pdp1/F15D_PDP1_Handbook_Oct63.pdf", "PROGRAMMED DATA PROCESSOR", None),
    ("PDF (worldradiohistory)", "https://www.worldradiohistory.com/Archive-Radio-Electronics/50s/1957/Radio-Electronics-1957-01.pdf",
     "Radio-Electronics", None),
    ("NASA NTRS record", "https://ntrs.nasa.gov/citations/19660019472", "Guidance computer design", None),
    ("Crossref metadata", "https://api.crossref.org/works/10.1038/s41586-019-1119-1",
     "Speech synthesis from neural decoding of spoken sentences", None),
    ("Semantic Scholar metadata", "https://api.semanticscholar.org/graph/v1/paper/DOI:10.1038/s41586-019-1119-1",
     "Speech synthesis from neural decoding of spoken sentences", None),
    ("Google Books API", "https://www.googleapis.com/books/v1/volumes?q=%22security+robot%22+computerworld", "robot", "any"),
]
rows = []
for typ, url, quote, vol in TESTS:
    try:
        t, d = page_text3.fetch(url, vol)
        rows.append({"type": typ, "url": url, "quote": quote, "found": page_text3.has_quote(t, quote), "record_date": d})
    except Exception as e:  # noqa: BLE001
        rows.append({"type": typ, "url": url, "quote": quote, "found": False, "error": str(e)[:160]})
    print(rows[-1])
(HERE / "raw/helper_tests3.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
