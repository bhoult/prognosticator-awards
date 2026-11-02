"""Extraction through the Message Batches API: the passages, rules and verifier of extract.py,
paid from API credits instead of the Claude plan.

    python -I pipeline/batch_api.py gold <run>                          a run over the 37 gold-set chunks
    python -I pipeline/batch_api.py count <run> [n]                     check the key; input tokens of n pending passages (free)
    python -I pipeline/batch_api.py submit <run> [max=N] [thinking=off|low|medium|high]
    python -I pipeline/batch_api.py collect <run>                       fetch ended batches into out/, then verify
    python -I pipeline/batch_api.py cancel <run>                        pause: cancel batches still running
    python -I pipeline/batch_api.py status <run>                        batches, tokens and cost
    python -I pipeline/batch_api.py auto <run> <budget $> [first=1000]  send, wait, collect, repeat within the budget

<run> is an extract.py run directory. The key is read from ANTHROPIC_API_KEY or KEY_FILE and is
never printed.

One request per passage, its id as custom_id. The request carries prompts/extract_api.md (the
subagent prompt without the file and tool instructions) as the system prompt, and the passage
file without its id line ("First published: <year>", then the passage). The reply is the claims
JSON; collect adds the passage id as "chunk" and writes out/<id>.json, so verification is the
same as for subagent results. api/meta/<id>.json records how each passage was extracted, and
extract.py's verify copies that into the verified record.

Stopping and restarting: api/batches.jsonl lists every batch sent and its passages,
api/collected.jsonl every batch whose results are on disk. submit skips verified passages and
passages in batches not yet collected, so it can be run again at any time; cancel stops the
running batches, and collect still saves what they finished (stop `auto` first if it is running).
A passage the model has answered
ATTEMPTS times without a usable result (refusal, cut off, unreadable JSON) is not sent again.
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract import ROOT, GOLD, load, pending, repair_json, sha, verify, write_atomic  # noqa: E402

KEY_FILE = os.path.expanduser('~/.config/prognosticator/anthropic-key')
PROMPT = os.path.join(ROOT, 'prompts', 'extract_api.md')
MODEL = 'claude-sonnet-5-5'
MAX_TOKENS = 32000      # a long passage yields about 8K tokens of claims; a cut-off reply is lost
PER_BATCH = 1000        # requests per batch, well under the 256 MB limit
ATTEMPTS = 2
# Batch prices, $ per million tokens (platform.claude.com/docs/en/about-claude/pricing, 2026-11-02):
# half the standard rates; cache writes are 5-minute ones.
PRICES = {'claude-sonnet-5-5': {'input_tokens': 1.0, 'cache_creation_input_tokens': 1.25,
                                'cache_read_input_tokens': 0.05, 'output_tokens': 5.0}}


def client():
    import anthropic
    key = os.environ.get('ANTHROPIC_API_KEY') or open(KEY_FILE, encoding='utf-8').read().strip()
    return anthropic.Anthropic(api_key=key)


def api_dir(run, *parts):
    return os.path.join(run, 'api', *parts)


def jsonl(path):
    return [json.loads(l) for l in open(path, encoding='utf-8')] if os.path.exists(path) else []


def append(path, rec):
    with open(path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(rec, ensure_ascii=False) + '\n')


def passage_message(run, cid):
    raw = open(os.path.join(run, 'passages', cid + '.txt'), encoding='utf-8').read()
    return raw.split('\n', 1)[1] if raw.startswith('Passage id:') else raw


def settings(thinking):
    s = {'model': MODEL, 'max_tokens': MAX_TOKENS, 'prompt_sha256': sha(open(PROMPT, 'rb').read())}
    if thinking == 'off':
        s['thinking'] = {'type': 'between_tools'}   # Sonnet 5.5's no-thinking setting
    else:
        s['thinking'], s['output_config'] = {'type': 'adaptive'}, {'effort': thinking}
    return s


def request(run, cid, s, system):
    params = {'model': s['model'], 'max_tokens': s['max_tokens'], 'thinking': s['thinking'],
              'system': [{'type': 'text', 'text': system, 'cache_control': {'type': 'ephemeral'}}],
              'messages': [{'role': 'user', 'content': passage_message(run, cid)}]}
    if 'output_config' in s:
        params['output_config'] = s['output_config']
    return {'custom_id': cid, 'params': params}


def gold(run):
    """A run directory over the gold-set chunks, so submit/collect/verify work on it unchanged."""
    if os.path.exists(os.path.join(run, 'config.json')):
        raise SystemExit(f'{run} already exists')
    for d in ('passages', 'prompts', 'out', 'verified'):
        os.makedirs(os.path.join(run, d), exist_ok=True)
    rows = []
    for c in map(json.loads, open(os.path.join(GOLD, 'chunks.jsonl'), encoding='utf-8')):
        raw = open(os.path.join(GOLD, 'chunks', c['id'] + '.txt'), encoding='utf-8').read()
        write_atomic(os.path.join(run, 'passages', c['id'] + '.txt'), raw)
        rows.append({'id': c['id'], 'book': c['path'], 'start': c['start'], 'end': c['end'], 'words': c['words'],
                     'year': c['year'], 'sha256': sha(raw.split('Passage:\n\n', 1)[1])})
    write_atomic(os.path.join(run, 'chunks.jsonl'), ''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows))
    write_atomic(os.path.join(run, 'batches.json'), open(os.path.join(GOLD, 'batches.json')).read())
    write_atomic(os.path.join(run, 'config.json'), json.dumps({
        'model': MODEL, 'prompt_sha256': sha(open(PROMPT, 'rb').read()), 'gold': True, 'books': len({r['book'] for r in rows}),
        'passages': len(rows), 'words': sum(r['words'] for r in rows), 'planned_at': time.strftime('%Y-%m-%d %H:%M:%S')}, indent=1))
    print(f'{run}: {len(rows)} gold chunks, {sum(r["words"] for r in rows):,} words')


def in_flight(run):
    done = {b['id'] for b in jsonl(api_dir(run, 'collected.jsonl'))}
    return {cid for b in jsonl(api_dir(run, 'batches.jsonl')) if b['id'] not in done for cid in b['passages']}


def meta(run, cid):
    path = api_dir(run, 'meta', cid + '.json')
    return json.load(open(path, encoding='utf-8')) if os.path.exists(path) else None


def todo(run):
    """Unverified passages in batch order, minus those being processed and those given up on."""
    busy = in_flight(run)
    out = []
    for ids in pending(run):
        for cid in ids:
            m = meta(run, cid)
            if cid not in busy and not (m and len(m['batches']) >= ATTEMPTS):
                out.append(cid)
    return out


def count(run, n='20'):
    s = settings('off')
    system = open(PROMPT, encoding='utf-8').read()
    words = {c['id']: c['words'] for c in map(json.loads, open(os.path.join(run, 'chunks.jsonl'), encoding='utf-8'))}
    ids, c = todo(run), client()
    sample = ids[:int(n)]
    tok = 0
    for cid in sample:
        r = c.messages.count_tokens(model=s['model'], system=system,
                                    messages=[{'role': 'user', 'content': passage_message(run, cid)}])
        tok += r.input_tokens
    w = sum(words[i] for i in sample)
    all_w = sum(words[i] for i in ids)
    print(f'key works. {len(sample)} passages, {w:,} words: {tok:,} input tokens ({tok / w:.3f} per word, '
          f'prompt included). All {len(ids):,} pending passages, {all_w:,} words: about {tok / w * all_w / 1e6:,.1f}M input tokens')


def submit(run, *opts):
    o = dict(a.split('=', 1) for a in opts)
    s = settings(o.get('thinking', 'off'))
    os.makedirs(api_dir(run, 'meta'), exist_ok=True)
    cfg_path = api_dir(run, 'config.json')
    if os.path.exists(cfg_path) and json.load(open(cfg_path)) != s:
        raise SystemExit(f'{run} was started with other API settings: {json.load(open(cfg_path))}; use a new run')
    claims = [n for n in os.listdir(os.path.join(run, 'prompts')) if n.endswith('.claimed')]
    if claims:
        raise SystemExit(f'{len(claims)} subagent batch(es) claimed; let them finish or `extract.py release` first')
    write_atomic(cfg_path, json.dumps(s, indent=1))
    verify(run)
    ids = todo(run)[:int(o['max'])] if 'max' in o else todo(run)
    if not ids:
        print('nothing to send')
        return
    send(run, ids, s)


def send(run, ids, s, c=None):
    system = open(PROMPT, encoding='utf-8').read()
    c = c or client()
    for i in range(0, len(ids), PER_BATCH):
        part = ids[i:i + PER_BATCH]
        b = c.messages.batches.create(requests=[request(run, cid, s, system) for cid in part])
        append(api_dir(run, 'batches.jsonl'), {'id': b.id, 'passages': part, 'settings': s,
                                                'submitted_at': time.strftime('%Y-%m-%d %H:%M:%S')})
        print(f'{b.id}: {len(part)} passages')


def parse(text):
    """The claims object in a reply. A reply now and then holds a first answer, a line such as
    "Correction: ...", and a second answer; the last readable one wins."""
    dec, found, i = json.JSONDecoder(), None, text.find('{')
    while i >= 0:
        try:
            obj, end = dec.raw_decode(text, i)
            if isinstance(obj, dict) and 'claims' in obj:
                found, i = obj, text.find('{', end)
                continue
        except ValueError:
            pass
        i = text.find('{', i + 1)
    if found is not None:
        return found, False
    a, z = text.find('{'), text.rfind('}')
    if a < 0 or z < a:
        raise ValueError('no JSON object')
    return repair_json(text[a:z + 1]), True


def collect(run):
    c = client()
    done = {b['id'] for b in jsonl(api_dir(run, 'collected.jsonl'))}
    os.makedirs(api_dir(run, 'raw'), exist_ok=True)
    for b in jsonl(api_dir(run, 'batches.jsonl')):
        if b['id'] in done:
            continue
        info = c.messages.batches.retrieve(b['id'])
        rc = info.request_counts
        if info.processing_status != 'ended':
            print(f"{b['id']}: {info.processing_status}, {rc.processing} processing, {rc.succeeded} succeeded, "
                  f"{rc.errored} errored")
            continue
        tally = {}
        for r in c.messages.batches.results(b['id']):
            cid, kind = r.custom_id, r.result.type
            tally[kind] = tally.get(kind, 0) + 1
            if kind != 'succeeded':   # errored, canceled or expired: sent again by the next submit
                append(api_dir(run, 'errors.jsonl'), {'batch': b['id'], 'chunk': cid, 'type': kind,
                                                      'error': str(getattr(r.result, 'error', ''))[:500]})
                continue
            msg = r.result.message
            usage = {k: getattr(msg.usage, k, 0) or 0 for k in PRICES[MODEL]}
            append(api_dir(run, 'usage.jsonl'), {'batch': b['id'], 'chunk': cid, 'model': msg.model,
                                                 'stop_reason': msg.stop_reason, **usage})
            text = ''.join(x.text for x in msg.content if x.type == 'text')
            m = meta(run, cid) or {'batches': []}
            m.update({'method': 'batch-api', 'model': msg.model, 'prompt_sha256': b['settings']['prompt_sha256'],
                      'settings': b['settings'], 'batches': sorted(set(m['batches']) | {b['id']}),
                      'stop_reason': msg.stop_reason, 'usage': usage, 'json_repaired': False, 'problem': None})
            try:
                if msg.stop_reason != 'end_turn':
                    raise ValueError(f'stop_reason {msg.stop_reason}')
                result, m['json_repaired'] = parse(text)
                if not isinstance(result.get('claims'), list):
                    raise ValueError('no claims list')
            except (ValueError, AttributeError) as e:
                m['problem'] = str(e)
                write_atomic(api_dir(run, 'raw', cid + '.txt'), text)
                write_atomic(api_dir(run, 'meta', cid + '.json'), json.dumps(m, indent=1))
                continue
            write_atomic(api_dir(run, 'meta', cid + '.json'), json.dumps(m, indent=1))
            write_atomic(os.path.join(run, 'out', cid + '.json'),
                         json.dumps({'chunk': cid, 'claims': result['claims']}, ensure_ascii=False, indent=1))
        append(api_dir(run, 'collected.jsonl'), {'id': b['id'], 'at': time.strftime('%Y-%m-%d %H:%M:%S'), **tally})
        print(f"{b['id']}: collected {tally}")
    verify(run)


def cancel(run):
    c = client()
    done = {b['id'] for b in jsonl(api_dir(run, 'collected.jsonl'))}
    for b in jsonl(api_dir(run, 'batches.jsonl')):
        if b['id'] not in done and c.messages.batches.retrieve(b['id']).processing_status == 'in_progress':
            print(f"{b['id']}: {c.messages.batches.cancel(b['id']).processing_status}")
    print('run `collect` once they have ended to keep what they finished')


def spend(run):
    """Replies so far (one per batch and passage), their cost in $, and the words they covered."""
    seen = {}
    for u in jsonl(api_dir(run, 'usage.jsonl')):
        seen[(u['batch'], u['chunk'])] = u
    usage = list(seen.values())
    cost = sum(u[k] * p / 1e6 for u in usage for k, p in PRICES.get(u['model'], PRICES[MODEL]).items())
    words = {c['id']: c['words'] for c in map(json.loads, open(os.path.join(run, 'chunks.jsonl'), encoding='utf-8'))}
    return usage, cost, sum(words[u['chunk']] for u in usage), words


def status(run):
    batches, collected = jsonl(api_dir(run, 'batches.jsonl')), jsonl(api_dir(run, 'collected.jsonl'))
    usage, cost, w, words = spend(run)
    left = sum(words[cid] for ids in pending(run) for cid in ids)
    print(f'{len(batches)} batch(es) sent, {len(collected)} collected, {len(in_flight(run))} passages in flight')
    if usage:
        tot = {k: sum(u[k] for u in usage) for k in PRICES[MODEL]}
        print(f"{len(usage)} replies for {w:,} words: input {tot['input_tokens']:,}, cache writes "
              f"{tot['cache_creation_input_tokens']:,}, cache reads {tot['cache_read_input_tokens']:,}, output "
              f"{tot['output_tokens']:,} ({tot['output_tokens'] / len(usage):,.0f} per passage); ${cost:,.2f}, "
              f"${10000 * cost / w:.3f} per 10K words")
        print(f'unverified words left: {left:,}; at this rate about ${cost / w * left:,.2f}')
    probs = [m for m in (meta(run, f[:-5]) for f in os.listdir(api_dir(run, 'meta'))) if m and m['problem']] \
        if os.path.isdir(api_dir(run, 'meta')) else []
    if probs:
        print(f'{len(probs)} passage(s) without a usable reply (see api/raw/): '
              + ', '.join(sorted({m["problem"] for m in probs})))


def auto(run, budget, *opts):
    """Rounds of send, wait, collect until the passages or the budget run out.

    The budget is in dollars, counted from the replies' usage at PRICES. The first round sends
    `first` passages to measure the cost per word on this run; each later round sends as many
    passages as that rate, plus 5%, says fit in what is left. Stops early on a credit or billing
    error; whatever was not done stays pending."""
    import anthropic
    o = dict(a.split('=', 1) for a in opts)
    budget, first, c = float(budget), int(o.get('first', 1000)), client()
    s = settings(o.get('thinking', 'off'))
    cfg_path = api_dir(run, 'config.json')
    if os.path.exists(cfg_path) and json.load(open(cfg_path)) != s:
        raise SystemExit(f'{run} was started with other API settings; use a new run')
    if any(n.endswith('.claimed') for n in os.listdir(os.path.join(run, 'prompts'))):
        raise SystemExit('subagent batches are claimed; let them finish or `extract.py release` first')
    os.makedirs(api_dir(run, 'meta'), exist_ok=True)
    write_atomic(cfg_path, json.dumps(s, indent=1))

    def say(msg):
        print(time.strftime('%Y-%m-%d %H:%M:%S'), msg, flush=True)

    def billing_errors():
        return sum(any(w in e.get('error', '').lower() for w in ('credit', 'billing', 'balance'))
                   for e in jsonl(api_dir(run, 'errors.jsonl')))

    while True:
        while True:   # wait for everything in flight
            done = {b['id'] for b in jsonl(api_dir(run, 'collected.jsonl'))}
            open_ = [b['id'] for b in jsonl(api_dir(run, 'batches.jsonl')) if b['id'] not in done]
            if not open_ or all(c.messages.batches.retrieve(i).processing_status == 'ended' for i in open_):
                break
            time.sleep(60)
        before = billing_errors()
        collect(run)
        usage, cost, words_paid, words = spend(run)
        say(f'spent ${cost:,.2f} of ${budget:,.2f} on {len(usage)} replies')
        if billing_errors() > before:
            say('credit or billing errors in the last results; stopping')
            break
        ids = todo(run)
        if not ids:
            say('no passages left to send')
            break
        if words_paid:
            rate, room, pick, est = 1.05 * cost / words_paid, budget - cost, [], 0.0
            for cid in ids:
                if est + rate * words[cid] > room:
                    break
                pick.append(cid)
                est += rate * words[cid]
        else:
            pick, est = ids[:first], 0.0
        if len(pick) < min(20, len(ids)):
            say(f'budget left (${budget - cost:,.2f}) covers fewer than 20 passages; stopping')
            break
        say(f'sending {len(pick)} passages' + (f', estimated ${est:,.2f}' if est else ' to measure the rate'))
        try:
            send(run, pick, s, c)
        except anthropic.RateLimitError as e:
            say(f'rate limited ({e}); trying again in 10 minutes')
            time.sleep(600)
        except anthropic.APIStatusError as e:
            say(f'API error {e.status_code}: {str(e)[:300]}; stopping')
            break
    status(run)


if __name__ == '__main__':
    cmd, args = sys.argv[1], sys.argv[2:]
    {'gold': gold, 'count': count, 'submit': submit, 'collect': collect, 'cancel': cancel,
     'status': status, 'auto': auto}[cmd](*args)
