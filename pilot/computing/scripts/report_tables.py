"""Print the markdown tables for report.md: top 20 and the 30-judgment hand-check."""
import json
import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
L = lambda f: [json.loads(x) for x in open(HERE / f)]
claims = {c["id"]: c for c in L("claims.jsonl")}
concepts = {c["concept_id"]: c for c in L("concepts.jsonl")}
ms = {(m["concept_id"], m["kind"]): m for m in L("milestones.jsonl")}
js = L("judgments.jsonl")
esc = lambda s: s.replace("|", "\\|").replace("\n", " ")


def pts(j):
    return j["score"] * math.log2(1 + min(j["lead_years"], 500)) if j["lead_years"] > 0 else 0


def short(q, n=220):
    return q if len(q) <= n else q[:n].rsplit(" ", 1)[0] + " …"


print("| # | Year | Quote | Concept | Milestone | Lead | Score | Points |")
print("|---|---|---|---|---|---|---|---|")
seen, k = set(), 0
for j in sorted(js, key=lambda j: -pts(j)):
    if j["id"] in seen or pts(j) == 0:
        continue
    seen.add(j["id"])
    k += 1
    m = ms[(j["concept_id"], j["milestone_kind"])]
    what = m["what"]
    print(f'| {k} | {claims[j["id"]]["year"]} | "{esc(short(claims[j["id"]]["quote"]))}" | '
          f'{concepts[j["concept_id"]]["name"]} | {m["date"][:7]}: {esc(short(what, 110))} '
          f'({j["milestone_kind"].replace("_", " ")}) | {j["lead_years"]} | {j["score"]} | {pts(j):.2f} |')
    if k == 20:
        break
print()
hc = {r["pair"]: r for r in L("raw/handcheck.jsonl")}
pool = [j for j in js if j["judged_by"] == "sonnet"]
random.seed(20261102)
print("| Pair | Year | Concept | Judge | Mine | Note |")
print("|---|---|---|---|---|---|")
for j in random.sample(pool, 30):
    h = hc[j["pair"]]
    print(f'| {j["pair"]} | {claims[j["id"]]["year"]} | `{j["concept_id"]}` | {j["score"]} | '
          f'{"**" + str(h["mine"]) + "**" if h["mine"] != j["score"] else h["mine"]} | {esc(h["note"])} |')
