"""RUN3 step 1: fetch one ordinary page or API call from each newly allowed host.
Records HTTP status, seconds and bytes (never page text). Status -1: no HTTP answer
(curl_exit says why, e.g. 28 timeout, 56 proxy refused CONNECT) in raw/netcheck3.jsonl.
Usage: python3 -I scripts/netcheck3.py"""
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import net  # noqa: E402
import page_text3  # noqa: E402,F401  (sets the 0.3 User-Agent)

HERE = Path(__file__).resolve().parent.parent
URLS = [
    ("books.google.com", "https://books.google.com/books?id=rEgEAAAAMBAJ"),
    ("www.googleapis.com/books/v1", "https://www.googleapis.com/books/v1/volumes?q=%22robot%22+computerworld&maxResults=3"),
    ("www.worldradiohistory.com", "https://www.worldradiohistory.com/"),
    ("www.worldradiohistory.com (PDF)", "https://www.worldradiohistory.com/Archive-Radio-Electronics/50s/1957/Radio-Electronics-1957-01.pdf"),
    ("bitsavers.org", "http://bitsavers.org/pdf/"),
    ("bitsavers.org (PDF)", "http://bitsavers.org/pdf/dec/pdp1/F15D_PDP1_Handbook_Oct63.pdf"),
    ("archive.computerhistory.org", "https://archive.computerhistory.org/"),
    ("www.computerhistory.org", "https://www.computerhistory.org/timeline/"),
    ("ethw.org", "https://ethw.org/Milestones:List_of_IEEE_Milestones"),
    ("spectrum.ieee.org", "https://spectrum.ieee.org/"),
    ("ieeexplore.ieee.org", "https://ieeexplore.ieee.org/document/1457412"),
    ("*.si.edu (www.si.edu)", "https://www.si.edu/"),
    ("*.si.edu (airandspace.si.edu)", "https://airandspace.si.edu/"),
    ("*.nasa.gov", "https://www.nasa.gov/history/"),
    ("ntrs.nasa.gov", "https://ntrs.nasa.gov/api/citations/19660019472"),
    ("pmc.ncbi.nlm.nih.gov", "https://pmc.ncbi.nlm.nih.gov/"),
    ("pubmed.ncbi.nlm.nih.gov", "https://pubmed.ncbi.nlm.nih.gov/?term=brain-computer+interface"),
    ("www.nature.com", "https://www.nature.com/articles/s41586-019-1119-1"),
    ("api.crossref.org", "https://api.crossref.org/works/10.1038/s41586-019-1119-1"),
    ("api.semanticscholar.org", "https://api.semanticscholar.org/graph/v1/paper/DOI:10.1038/s41586-019-1119-1?fields=title,year,publicationDate"),
    ("babel.hathitrust.org", "https://babel.hathitrust.org/cgi/pt?id=mdp.39015011330424"),
    ("archive.org (OCR text)", "https://archive.org/download/computerworld1940unse/computerworld1940unse_djvu.txt"),
    ("archive.org", "https://archive.org/advancedsearch.php?q=computerworld&fl%5B%5D=identifier&rows=3&output=json"),
    ("archive.org full-text", "https://archive.org/services/search/beta/page_production/?user_query=%22security+robot%22&service_backend=fts&hits_per_page=3"),
    ("www.smithsonianmag.com", "https://www.smithsonianmag.com/innovation/"),
    ("www.aip.org", "https://www.aip.org/history-programs"),
    ("www.hagley.org", "https://www.hagley.org/"),
    ("www.thehenryford.org", "https://www.thehenryford.org/"),
    ("www.nobelprize.org", "https://www.nobelprize.org/prizes/physics/1971/summary/"),
    ("*.mit.edu", "https://news.mit.edu/"),
    ("www.britannica.com (expected 403)", "https://www.britannica.com/technology/computer"),
]
rows = []
for host, url in URLS:
    t = time.time()
    p = subprocess.run(["curl", "-sSL", "-m", "45", "-A", net.UA, "-o", "/dev/null", "-w",
                        "%{http_code} %{size_download} %{url_effective}", url], capture_output=True, text=True)
    code, size, final = (p.stdout.split(" ", 2) + ["", "", ""])[:3]
    rows.append({"host": host, "url": url, "status": int(code or 0) or -1, "seconds": round(time.time() - t, 1),
                 "bytes": int(size or 0), "final_url": final, "curl_exit": p.returncode,
                 "checked": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")})
    print(host, rows[-1]["status"], rows[-1]["seconds"], size)
(HERE / "raw/netcheck3.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
