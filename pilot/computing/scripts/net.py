"""Shared HTTP helper for run 2: descriptive User-Agent, retry with backoff on 429/5xx.

Uses curl (Python's urllib hangs behind this environment's proxy). Wikimedia
rate-limits the environment's shared egress IP, so 429s are common: we back off,
honouring Retry-After, and retry.
"""
import json
import subprocess
import time
import urllib.parse

UA = ("prognosticator-awards-pilot/0.2 "
      "(https://github.com/bhoult/prognosticator-awards; research on predictions in fiction)")


def get(url, params=None, accept="application/json", tries=8, timeout=60):
    """Return (status, body, final_url); status -1 on network failure."""
    if params:
        url = url + ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
    delay = 2.0
    last = (-1, "", url)
    for _ in range(tries):
        p = subprocess.run(
            ["curl", "-sSL", "-m", str(timeout), "-A", UA, "-H", f"Accept: {accept}",
             "-D", "/dev/stderr", "-w", "\n%{http_code} %{url_effective}", url],
            capture_output=True, text=True)
        out = p.stdout
        if "\n" in out:
            body, tail = out.rsplit("\n", 1)
        else:
            body, tail = "", out
        parts = tail.split(" ", 1)
        try:
            code = int(parts[0])
        except ValueError:
            code = -1
        final = parts[1] if len(parts) > 1 else url
        last = (code if code else -1, body, final)
        if code == 200:
            return last
        if code in (0, 429, 500, 502, 503, 504) or p.returncode != 0:
            ra = None
            for line in p.stderr.splitlines():
                if line.lower().startswith("retry-after:"):
                    ra = line.split(":", 1)[1].strip()
            time.sleep(max(delay, float(ra) if ra and ra.isdigit() else 0))
            delay = min(delay * 2, 60)
            continue
        return last
    return last


def get_json(url, params=None, **kw):
    code, body, _ = get(url, params, **kw)
    if code != 200:
        raise RuntimeError(f"HTTP {code} for {url}: {body[:200]}")
    return json.loads(body)


def sparql(query):
    return get_json("https://query.wikidata.org/sparql", {"query": query, "format": "json"},
                    accept="application/sparql-results+json")
