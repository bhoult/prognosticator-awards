You are helping build a research database of predictions found in old texts. You will read passages and record every speculative claim in each one. Work only from the passages you are given.

Files to read, one passage each (use the Read tool on each, in full):
{files}

Work through them one at a time: read one passage, write its result file, then go on to the next. Write each result file as soon as you finish its passage, not at the end.

For each passage file, write a result file with the Write tool at:
{outdir}/<passage id>.json   (the passage id is on the file's first line, "Passage id: <id>", and is also the file name without .txt)

Rules:
- Read only the files listed above. Do not open, list or search any other file or directory, and do not use the web. Do not try to work out which book or author a passage comes from; names have been blanked out as […] on purpose.
- Each file starts with a short header: its passage id, then "First published: <year>". Judge what was speculative relative to that year.

What to record. List everything in the passage that imagines a future, or an alternative to the world as it was when the passage was written: technologies, inventions, scientific discoveries, ways of living, political or economic arrangements, and events. Include ideas that are impossible or never happened. Some passages are non-fiction forecasts, scripture or other old writing: there, also list statements about future events and about the natural world that go beyond what was known when it was written. Read the words literally; do not supply meanings from commentary, allegory or later tradition.

Every item must rest on a quotation copied exactly from the passage: same words, same order, no ellipses, at most 60 words. If an idea is spread across sentences, quote the single sentence that states it most clearly. Do not add things you know a book or author is famous for.

Leave out ordinary things that already existed when the passage was written, unless the passage gives them a capability they didn't have yet. If a passage is a later introduction or commentary describing what an earlier work predicted, the claims in it are not speculative: set speculative_at_time to false.

Result file format, exactly this JSON, with "chunk" set to the passage id (an empty "claims" list is a valid answer):
{
  "chunk": "<passage id>",
  "claims": [
    {
      "quote": "exact words from the passage, at most 60 words",
      "description": "one plain sentence: what is imagined, in modern terms if possible",
      "category": "technology | science | social | political | event | other",
      "specificity": 1-5 (1 = vague gesture, 5 = concrete mechanism and use),
      "speculative_at_time": true or false (true if it did not yet exist in practice in the year of first publication),
      "stated_time": "when the passage says it will happen, in its own words, e.g. \"within fifty years\"" or null,
      "polarity": "will | will_not" (will_not when the passage says it will never or cannot happen),
      "confidence": "asserted | hedged",
      "valence": "positive | negative | neutral | mixed" (how the passage presents it),
      "voice": "narrator | sympathetic | antagonist | document" (who states it: narrator or author, a sympathetic character, an antagonist or skeptic, or an in-world document),
      "domain": "computing | communication | transport | energy | medicine-biology | weapons-war | space | society-politics | economy | environment | other",
      "second_order": true or false (true if it predicts a consequence of a technology or change rather than the thing itself)
    }
  ]
}
Write valid JSON only in the result files: double quotes, no comments, no trailing commas.

When every file is written, reply with one line per passage: its id and how many claims you recorded. Nothing else.
