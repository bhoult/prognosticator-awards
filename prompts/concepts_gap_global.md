# Merge the gap concepts across domain groups (full matching run, tranche A, gap pass)

New concepts were proposed for the claims that matched nothing in the registry, and each
domain group's were consolidated on their own, so the same concept can appear in two groups
(a "giant serpent" under other and "giant snakes" under medicine-biology). A book counts once
per concept, so duplicates would count it twice. Your job is to find them.

Work in `{workdir}` and run commands from there. Keep every file you write (scripts, notes)
in `{tmpdir}`, never in any other temporary or scratchpad directory.

## Input

`{concepts}`: JSON lines `{"concept_id", "name", "definition", "domains", "est_claims"}`,
every new concept of every group. Read it with the Read tool in three calls (lines 1–300,
301–600, 601 to the end). Read every definition in full: don't print names only or shortened
definitions with a script. Duplicates are often worded differently, so compare definitions,
not just names.

## Task

Find concepts that are the same thing: the same function and mechanism, so that one real
event would date both. Similar but distinct concepts stay separate ("radar" and "sonar";
"heart transplant" and "artificial heart"). For each group of duplicates, choose the one to
keep (the clearest definition, usually the broader domain coverage).

## Output

Write with the Write tool to `{out}`: JSON lines only, one group per line, no prose:

{"keep": "giant-snakes", "drop": ["giant-serpent"], "reason": "both: snakes of enormous size threatening people"}

Only real duplicates; if there are none, write an empty file. Check that it parses
(`python3 -I -c "import json;print(len([json.loads(l) for l in open('{out}')]))"`).
Don't edit any other file, don't search the web, and don't run git. Reply with one line: how
many groups.
