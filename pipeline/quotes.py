"""Quote verification shared by the gold evaluation and the extraction driver. Deterministic.

A claim's quote must appear in its passage: exactly after normalizing, or at >= 90%
fuzzy similarity (rapidfuzz partial_ratio_alignment). Offsets map back to the original text.
"""
from rapidfuzz import fuzz

FOLD = str.maketrans({'‘': "'", '’': "'", '“': '"', '”': '"', '—': '-', '–': '-', ' ': ' '})


def normalize(s):
    """Fold quotes/dashes, drop markdown emphasis and escapes, collapse whitespace; keep a map to s."""
    out, pos = [], []
    prev_space = False
    for i, ch in enumerate(s.translate(FOLD)):
        if ch in '*_\\':
            continue
        if ch.isspace():
            if prev_space:
                continue
            ch, prev_space = ' ', True
        else:
            prev_space = False
        out.append(ch.lower())
        pos.append(i)
    return ''.join(out), pos


def verify(quote, _text, ntext, npos):
    """('exact' | 'fuzzy' | 'rejected', offset in the original text or None, similarity)."""
    q, _ = normalize(quote.strip().strip('"').strip())
    if len(q) < 8:
        return 'rejected', None, 0.0
    at = ntext.find(q)
    if at >= 0:
        return 'exact', npos[at], 100.0
    al = fuzz.partial_ratio_alignment(q, ntext, score_cutoff=90)
    if al:
        return 'fuzzy', npos[al.dest_start], al.score
    return 'rejected', None, 0.0
