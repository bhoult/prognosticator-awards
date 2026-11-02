"""Pull a subagent's final report and usage out of its transcript.

Usage: python3 -I scripts/agent_out.py <transcript.jsonl> <out.jsonl> <usage-label> <step> <purpose>

Writes every line of the final report (or of the SubagentHandback message) that parses
as a JSON object to <out.jsonl>, and appends one row to usage.tsv:
agent, step, purpose, model, total_tokens (the last turn's input+cache+output, as the
harness reports it), tool_uses, seconds (first to last transcript timestamp).
"""
import json
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
src, out, label, step, purpose = sys.argv[1:6]
rows = []
for line in open(src):
    try:
        rows.append(json.loads(line))
    except json.JSONDecodeError:
        pass

texts, last_usage, tools, model = [], None, 0, ""
for r in rows:
    m = r.get("message")
    if not isinstance(m, dict):
        continue
    if m.get("usage"):
        last_usage = m["usage"]
        model = m.get("model", model)
    content = m.get("content")
    if m.get("role") == "assistant" and isinstance(content, list):
        for c in content:
            if c.get("type") == "tool_use":
                tools += 1
                inp = c.get("input", {})
                if "Handback" in c.get("name", "") or c.get("name") == "SendMessage":
                    texts.append(json.dumps(inp))  # handled below
            elif c.get("type") == "text":
                texts.append(c["text"])

# Gather candidate JSON lines from the final text and any handback payloads.
cand = []
for t in texts:
    try:
        obj = json.loads(t)
        if isinstance(obj, dict):
            t = "\n".join(str(v) for v in obj.values() if isinstance(v, str))
    except (json.JSONDecodeError, TypeError):
        pass
    for line in t.splitlines():
        line = line.strip().strip(",")
        if line.startswith("{") and line.endswith("}"):
            try:
                cand.append(json.loads(line))
            except json.JSONDecodeError:
                pass

# Keep the last complete block: de-duplicate identical objects, keep order.
seen, objs = set(), []
for o in cand:
    k = json.dumps(o, sort_keys=True)
    if k not in seen:
        seen.add(k)
        objs.append(o)
Path(out).write_text("".join(json.dumps(o, ensure_ascii=False) + "\n" for o in objs))

ts = [datetime.fromisoformat(r["timestamp"].replace("Z", "+00:00")) for r in rows if r.get("timestamp")]
secs = round((max(ts) - min(ts)).total_seconds()) if ts else 0
u = last_usage or {}
tot = sum(u.get(k, 0) for k in ["input_tokens", "cache_creation_input_tokens",
                                "cache_read_input_tokens", "output_tokens"])
with open(HERE / "usage.tsv", "a") as f:
    f.write(f"{label}\t{step}\t{purpose}\t{model}\t{tot}\t{tools}\t{secs}\n")
print(f"{len(objs)} objects -> {out}; tokens {tot}, tools {tools}, {secs}s")
