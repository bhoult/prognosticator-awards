"""Write one filled-in extraction prompt per (model, batch), saved with the run.

    python -I pipeline/make_prompts.py <model> [<model> ...]

Creates runs/<model>/batch_<n>.md from prompts/extract_subagent.md and gold/batches.json.
Each subagent is told only to read its batch file and follow it, so every model gets
byte-identical instructions and the exact prompt is kept next to its results.
"""
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
template = open(os.path.join(ROOT, 'prompts', 'extract_subagent.md'), encoding='utf-8').read()
batches = json.load(open(os.path.join(ROOT, 'gold', 'batches.json')))
for model in sys.argv[1:]:
    outdir = os.path.join(ROOT, 'runs', model)
    os.makedirs(outdir, exist_ok=True)
    for n, ids in enumerate(batches, 1):
        files = '\n'.join(os.path.join(ROOT, 'gold', 'chunks', f'{i}.txt') for i in ids)
        prompt = template.replace('{files}', files).replace('{outdir}', outdir)
        with open(os.path.join(outdir, f'batch_{n}.md'), 'w', encoding='utf-8') as f:
            f.write(prompt)
    print(model, len(batches), 'batch prompts in', outdir)
