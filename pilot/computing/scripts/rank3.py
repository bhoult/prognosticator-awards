"""Ranking as in report2.md 6.2: points = score x log2(1 + min(lead, 500)); each book counted
once per concept (its best claim); ties broken by claim id. Shared by the RUN3 scripts."""
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
_claims = None


def claims():
    global _claims
    if _claims is None:
        _claims = {c["id"]: c for c in map(json.loads, open(HERE / "claims.jsonl"))}
    return _claims


def points(j):
    if j["score"] and j["lead_years"] and j["lead_years"] > 0:
        return round(j["score"] * math.log2(1 + min(j["lead_years"], 500)), 4)
    return 0


def ranking(judg):
    """List of (points, judgment) for every book-concept entry with points, best first."""
    best = {}
    for j in judg:
        p = points(j)
        if p:
            key = (claims()[j["id"]]["book"], j["concept_id"])
            if key not in best or p > best[key][0] or (p == best[key][0] and j["id"] < best[key][1]["id"]):
                best[key] = (p, j)
    return sorted(best.values(), key=lambda t: (-t[0], t[1]["id"]))


def entry(j):
    return (claims()[j["id"]]["book"], j["concept_id"])
