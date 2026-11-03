"""Step 6 of RUN2: tables for report2.md -> raw/report2_tables.md.

1. Milestone date changes, first pass -> second pass, per (concept, kind); the 30
   largest with old and new dates and the new source.
2. Top 20 by score x log2(1 + min(lead, 500)), counting each book once per concept (its
   best claim), for both passes, and how the ranking moved.
3. Score changes for re-judged pairs.
"""
import json
import math
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
L = lambda f: [json.loads(l) for l in open(HERE / f)]  # noqa: E731
claims = {c["id"]: c for c in L("claims.jsonl")}
names = {c["concept_id"]: c["name"] for c in L("concepts2.jsonl")}
m1 = {(m["concept_id"], m["kind"]): m for m in L("milestones.jsonl")}
m2 = {(m["concept_id"], m["kind"]): m for m in L("milestones2.jsonl")}
KS = {"first_demonstration": "demonstration", "first_practical_use": "practical use", "mass_adoption": "mass adoption"}
y = lambda d: int(str(d)[:4])  # noqa: E731
out = []

# 1. date changes
ch = Counter()
rows = []
for k in sorted(set(m1) | set(m2)):
    a, b = m1.get(k), m2.get(k)
    if a and b:
        d = y(b["date"]) - y(a["date"])
        ch["earlier" if d < 0 else "later" if d > 0 else ("same year, different date" if a["date"] != b["date"] else "unchanged")] += 1
        if d:
            rows.append((abs(d), d, k, a, b))
    elif a:
        ch["removed"] += 1
    else:
        ch["new"] += 1
out.append("### Milestone changes (first pass → second pass, per concept and kind)\n")
out.append("| Change | Milestones |\n|---|---|")
for k in ["earlier", "later", "same year, different date", "unchanged", "new", "removed"]:
    out.append(f"| {k} | {ch[k]} |")
out.append(f"\nYears moved, among the {len(rows)} that moved: median "
           f"{sorted(r[0] for r in rows)[len(rows) // 2]}, earlier {sum(r[1] < 0 for r in rows)}, later {sum(r[1] > 0 for r in rows)}.\n")
out.append("### The 30 largest date changes\n")
out.append("| # | Concept | Kind | Old | New | Change (years) | New event | Source |\n|---|---|---|---|---|---|---|---|")
for i, (_, d, k, a, b) in enumerate(sorted(rows, key=lambda r: -r[0])[:30], 1):
    s = b["sources"][0]
    out.append(f"| {i} | {k[0]} | {KS[k[1]]} | {a['date']} | {b['date']} | {d:+d} | {b['what'][:110]} | "
               f"[{s['title'] or s['publisher']}]({s['url']}) |")


# 2. rankings
def ranking(judg):
    best = {}
    for j in judg:
        if j["score"] and j["lead_years"] and j["lead_years"] > 0:
            p = j["score"] * math.log2(1 + min(j["lead_years"], 500))
            c = claims[j["id"]]
            key = (c["book"], j["concept_id"])
            if key not in best or p > best[key][0]:
                best[key] = (round(p, 4), j)
    return sorted(best.values(), key=lambda t: (-t[0], t[1]["id"]))


r1, r2 = ranking(L("judgments.jsonl")), ranking(L("judgments2.jsonl"))
pos1 = {(claims[j["id"]]["book"], j["concept_id"]): i for i, (_, j) in enumerate(r1, 1)}
pos2 = {(claims[j["id"]]["book"], j["concept_id"]): i for i, (_, j) in enumerate(r2, 1)}


def ms_text(cid, kind, which):
    m = which.get((cid, kind))
    return f"{m['date']}: {m['what'][:90]}" if m else ""


def table(r, which, other_pos, label):
    out.append(f"| # | Year | Quote | Concept | Milestone | Lead | Score | Points | {label} |\n|---|---|---|---|---|---|---|---|---|")
    for i, (p, j) in enumerate(r[:20], 1):
        c = claims[j["id"]]
        q = c["quote"].replace("|", "/").replace("\n", " ")
        q = q if len(q) <= 160 else q[:157] + "…"
        o = other_pos.get((c["book"], j["concept_id"]))
        out.append(f"| {i} | {c['year']} | \"{q}\" | {names[j['concept_id']]} | "
                   f"{ms_text(j['concept_id'], j['milestone_kind'], which)} ({KS[j['milestone_kind']]}) | "
                   f"{j['lead_years']} | {j['score']} | {p:.2f} | {o if o else '—'} |")


out.append("\n### New top 20 (each book counted once per concept)\n")
table(r2, m2, pos1, "First-pass rank")
out.append("\n### First-pass top 20, recomputed with each book counted once per concept\n")
table(r1, m1, pos2, "Second-pass rank")
both = len({k for k in list(pos1)[:0]})
top1 = {(claims[j["id"]]["book"], j["concept_id"]) for _, j in r1[:20]}
top2 = {(claims[j["id"]]["book"], j["concept_id"]) for _, j in r2[:20]}
out.append(f"\nIn both top 20s: {len(top1 & top2)}. Book-concept entries with points: first pass {len(r1)}, second {len(r2)}.")
mx = lambda r: (max(j["lead_years"] for _, j in r[:20]), min(j["lead_years"] for _, j in r[:20]))  # noqa: E731
out.append(f"Lead years in the top 20: first pass {mx(r1)[1]}–{mx(r1)[0]}, second pass {mx(r2)[1]}–{mx(r2)[0]}.")
sc = Counter(round(p, 2) for p, _ in r2[:20])

# 3. score changes
j2 = L("judgments2.jsonl")
re_ = [j for j in j2 if j["action"] == "rejudged" and "first_pass_score" in j]
delta = Counter(j["score"] - j["first_pass_score"] for j in re_)
out.append("\n### Re-judged pairs: score change against the first pass\n")
out.append("| Change | Pairs |\n|---|---|")
for d in sorted(delta):
    out.append(f"| {d:+.2f} | {delta[d]} |")
out.append(f"\nActions: {dict(Counter(j['action'] for j in j2))}. Score distribution (all pairs): "
           f"{dict(sorted(Counter(j['score'] for j in j2).items()))}.")
(HERE / "raw/report2_tables.md").write_text("\n".join(out) + "\n")
print("\n".join(out[:12]))
