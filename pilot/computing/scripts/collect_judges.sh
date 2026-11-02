#!/bin/sh
# Collect finished judge agents (listed in scripts/agents.tsv) into raw/judge_NN.jsonl.
# Usage: sh scripts/collect_judges.sh <tasks-dir> <batch-dir> NN [NN...]
T=$1; B=$2; shift 2
for n in "$@"; do
  line=$(grep -P "\t$n\t" scripts/agents.tsv)
  id=$(echo "$line" | cut -f1); lab=$(echo "$line" | cut -f3)
  python3 -I scripts/agent_out.py "$T/$id.output" raw/judge_$n.jsonl $lab 4 "judge batch $n"
  python3 -c "
import json,sys
a=[json.loads(l)['pair'] for l in open('$B/judge_batch$n.jsonl')]
b=[json.loads(l) for l in open('raw/judge_$n.jsonl')]
bad=[r for r in b if r.get('score') not in (0,0.25,0.5,0.75,1)]
print('  in',len(a),'out',len(b),'missing',sorted(set(a)-{r['pair'] for r in b}),'bad',len(bad))"
done
