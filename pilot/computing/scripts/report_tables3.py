"""Step 8 of RUN3: tables for report3.md -> raw/report3_tables.md, and raw/top100_3.tsv.

1. The network check, and the hosts the verified sources come from.
2. The 33 target concepts: the ranking's milestone (first_practical_use, else
   first_demonstration) in the second and third pass, with event, source kinds,
   confidence and fit; decisions from raw/review3.jsonl and the earliest-event check marked.
3. Source kinds, second pass against third, for the target concepts.
4. Judge agreement (step 7), if the second judge has run.
5. The top 20 (each book once per concept) with the second-pass rank; the top 100 in
   raw/top100_3.tsv (quotes cut to 25 words).
Sections whose inputs don't exist yet are left out. Usage: python3 -I scripts/report_tables3.py
"""
import json
import sys
import urllib.parse
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rank3  # noqa: E402

HERE = rank3.HERE
L = lambda f: [json.loads(l) for l in open(HERE / f) if l.strip()] if (HERE / f).exists() else []  # noqa: E731
claims = rank3.claims()
names = {c["concept_id"]: c["name"] for c in L("concepts2.jsonl")}
targets = [r["concept_id"] for r in L("raw/targets3.jsonl")]
KS = {"first_demonstration": "demonstration", "first_practical_use": "practical use"}
cell = lambda s: str(s or "").replace("|", "/").replace("\n", " ")  # noqa: E731
out = []


def by_concept(rows):
    d = {}
    for m in rows:
        d.setdefault(m["concept_id"], {})[m["kind"]] = m
    return d


def pick(d):
    return d.get("first_practical_use") or d.get("first_demonstration")


m2, m3 = by_concept(L("milestones2.jsonl")), by_concept(L("milestones3.jsonl"))
checked3 = {tuple(r["key"]): r["result"] for r in L("raw/check3_applied.jsonl")}
review = {}
for r in L("raw/review3.jsonl"):
    review.setdefault(r["concept_id"], []).append(r["op"])

# 1. network
net = L("raw/netcheck3.jsonl")
if net:
    out += ["## Network check", "", "| Host | Status | Seconds |", "|---|---|---|"]
    out += [f"| {r['host']} | {r['status']} | {r.get('seconds', '')} |" for r in net]
    hosts = Counter(urllib.parse.urlparse(s["url"]).netloc.removeprefix("www.")
                    for c in targets for m in m3.get(c, {}).values() if m.get("target3") for s in m["sources"])
    out += ["", "Hosts of the verified sources of the target milestones (all kinds):", "",
            "| Host | Sources |", "|---|---|"] + [f"| {h} | {n} |" for h, n in hosts.most_common()]

# 2. the 33 targets
out += ["", "## The 33 target concepts: the ranking's milestone", "",
        "R = decided in raw/review3.jsonl; C = confirmed and X = replaced by the earliest-event check.", "",
        "| Concept | Kind | Second pass | Third pass | Event | Sources | Confidence | Fit |", "|---|---|---|---|---|---|---|---|"]
for c in targets:
    a, b = pick(m2.get(c, {})), pick(m3.get(c, {}))
    if not b:
        out.append(f"| {names[c]} | | {a['date'] if a else 'none'} | none | | | | |")
        continue
    mark = ("R" if c in review else "") + {"confirmed": "C", "replaced": "X"}.get(checked3.get((c, b["kind"])), "")
    kinds = ", ".join(f"{n} {k}" for k, n in sorted(Counter(s["kind"] for s in b["sources"]).items()))
    old = f"{a['date']} ({KS[a['kind']][:4]}.)" if a else "none"
    out.append(f"| {names[c]} | {KS[b['kind']]} | {old} | **{b['date']}** {mark} | {cell(b['what'])} | {kinds} | "
               f"{b['confidence']} | {cell(b.get('fit'))} |")

# 3. source kinds
def kinds(ms):
    rows = [m for c in targets for m in ms.get(c, {}).values() if m.get("kind") in KS]
    return len(rows), sum(any(s["kind"] == "contemporary" for s in m["sources"]) for m in rows), \
        Counter(s["kind"] for m in rows for s in m["sources"])


out += ["", "## Source kinds (target concepts, demonstration and practical-use milestones)", "",
        "| Pass | Milestones | With a contemporary source | Sources by kind |", "|---|---|---|---|"]
for label, ms in (("second", m2), ("third", m3)):
    n, w, k = kinds(ms)
    out.append(f"| {label} | {n} | {w} | {', '.join(f'{x} {v}' for x, v in sorted(k.items()))} |")

# 4. judge agreement
J = L("judgments3.jsonl")
keys = {}
for p in sorted(HERE.glob("raw/judge3b_key_round*.jsonl")):
    rnd = int(p.stem.split("round")[1])
    s2 = {r["pair"]: r["score"] for r in L(f"raw/judge3b_round{rnd}.jsonl")}
    s3 = {r["pair"]: r["score"] for r in L(f"raw/judge3c_round{rnd}.jsonl")}
    for r in L(p.relative_to(HERE)):
        keys[(rnd, r["pair"])] = (r["group"], rnd, s2.get(r["pair"]), s3.get(r["pair"]))
if keys and J:
    first = {j["pair"]: j for j in L("raw/judgments3_step6.jsonl")}
    out += ["", "## Second judge: agreement with the first", "",
            "| Group | Pairs | Same score | One step apart | Two or more apart | Second judge lower | Second judge higher |",
            "|---|---|---|---|---|---|---|"]
    for g in ("top100", "score1", "top100_new", "random50"):
        rows = [(first[p]["score"], v[2]) for (_, p), v in keys.items() if v[0] == g and v[2] is not None]
        if rows:
            d = [abs(a - b) for a, b in rows]
            out.append(f"| {g} | {len(rows)} | {sum(x == 0 for x in d)} | {sum(x == 0.25 for x in d)} | "
                       f"{sum(x >= 0.5 for x in d)} | {sum(b < a for a, b in rows)} | {sum(b > a for a, b in rows)} |")
    act = Counter(j["action2"] for j in J if "action2" in j)
    moved = Counter((j["judges"][0], j["score"]) for j in J if "action2" in j and j["score"] != j["judges"][0])
    out += ["", "Outcome for the top-100 and 1.0 pairs: " + ", ".join(f"{k} {v}" for k, v in sorted(act.items())) + ".",
            "Scores changed (first judge -> final): " + (", ".join(f"{a} -> {b}: {n}" for (a, b), n in sorted(moved.items())) or "none") + "."]

# 5. top 20 and top 100
if J:
    r2 = {rank3.entry(j): i for i, (_, j) in enumerate(rank3.ranking(L("judgments2.jsonl")), 1)}
    top = rank3.ranking(J)
    out += ["", f"## Top 20 ({len(top)} book-concept entries with points)", "",
            "| # | Was | Year | Concept | Milestone | Lead | Judges | Score | Points | Quote |", "|---|---|---|---|---|---|---|---|---|---|"]
    tsv = ["rank\tsecond_pass_rank\tyear\tclaim\tconcept\tmilestone_kind\tmilestone_date\tlead_years\tjudges\tscore\tpoints\tquote"]
    for i, (p, j) in enumerate(top[:100], 1):
        c = claims[j["id"]]
        q = c["quote"].split()
        q = " ".join(q[:25]) + (" …" if len(q) > 25 else "")
        was = r2.get(rank3.entry(j), "")
        judges = "/".join(str(x) for x in j.get("judges", [j["score"]]))
        tsv.append("\t".join(str(x) for x in (i, was, c["year"], j["id"], j["concept_id"], j["milestone_kind"],
                                               j["milestone_date"], j["lead_years"], judges, j["score"], p, q)))
        if i <= 20:
            out.append(f"| {i} | {was or 'new'} | {c['year']} | {names[j['concept_id']]} | {j['milestone_date']} | "
                       f"{j['lead_years']} | {judges} | {j['score']} | {p:.2f} | {cell(q)} |")
    (HERE / "raw/top100_3.tsv").write_text("\n".join(tsv) + "\n")
(HERE / "raw/report3_tables.md").write_text("\n".join(out) + "\n")
print("wrote raw/report3_tables.md", "and raw/top100_3.tsv" if J else "")
