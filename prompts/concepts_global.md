# Merge concepts across domains (full matching run, tranche A)

Each domain's concepts were consolidated on their own, so the same concept can appear in two
domains (a "space-station computer" under computing and under space; "radar" under
communication and under weapons-war). A book counts once per concept, so duplicates would
count it twice. Your job is to find them.

Work in `{workdir}` and run commands from there.

## Input

`{concepts}`: JSON lines `{"concept_id", "name", "definition", "domains", "est_claims"}`,
every concept of every domain. Read the whole file, in chunks, until the end.

## Task

Find concepts that are the same thing: the same function and mechanism, so that one real
event would date both. Similar but distinct concepts stay separate ("radar" and "sonar";
"heart transplant" and "artificial heart"). For each group of duplicates, choose the one to
keep (the clearest definition, usually the broader domain coverage).

## Output

Write with the Write tool to `{out}`: JSON lines only, one group per line, no prose:

{"keep": "radar", "drop": ["radar-detection"], "reason": "both: radio echoes locate distant objects"}

Only real duplicates; if there are none, write an empty file. Check that it parses
(`python3 -I -c "import json;print(len([json.loads(l) for l in open('{out}')]))"`).
Don't edit any other file, don't search the web, and don't run git. Reply with one line: how
many groups.
