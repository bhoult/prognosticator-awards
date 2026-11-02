# Extraction prompt: extract_v0 (draft)

Model: varies by test (`claude-haiku-5-5` low/medium effort, `claude-sonnet-5-5`, `claude-opus-5-5` low effort).
Input per request: one chunk of a book and the year it was first published. **No author, no title.**

## System

You read passages of fiction and list everything in them that imagines a future, or an
alternative to the world as it was when the passage was written: technologies,
inventions, scientific discoveries, ways of living, political or economic arrangements,
and events. Include ideas that are impossible or never happened; they are recorded too.

Work only from the passage. Do not add things you know the book or its author is famous
for. Every item must rest on a quotation copied exactly from the passage: same words,
same order, no ellipses, at most 60 words. If an idea is spread across sentences, quote
the single sentence that states it most clearly.

Leave out ordinary things that already existed when the passage was written (trains in
1890, radio in 1935), unless the passage gives them a capability they didn't have yet.

Some passages are scripture or other ancient writing, often in translation. There, also
list statements about future events and about the natural world (the heavens, the body,
the earth) that go beyond what was known when it was written. Read the words literally:
do not supply meanings from commentary, allegory, numerology or later tradition, and do
not include a claim that only works under such a reading.

## User

```
First published: {year}          (ancient texts: "Written no later than: {year}")
Passage:
<<<
{chunk_text}
>>>
```

## Structured output (`output_config.format`, JSON schema)

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["claims"],
  "properties": {
    "claims": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["quote", "description", "category", "specificity", "speculative_at_time",
                     "stated_time", "polarity", "confidence", "valence", "voice", "domain", "second_order"],
        "properties": {
          "quote":       {"type": "string", "description": "Exact words from the passage, at most 60 words."},
          "description": {"type": "string", "description": "One plain sentence: what is imagined, in modern terms if possible."},
          "category":    {"type": "string", "enum": ["technology", "science", "social", "political", "event", "other"]},
          "specificity": {"type": "integer", "minimum": 1, "maximum": 5,
                          "description": "1 = vague gesture, 5 = concrete mechanism and use."},
          "speculative_at_time": {"type": "boolean",
                          "description": "True if this did not yet exist in practice in the year of first publication."},
          "stated_time": {"type": ["string", "null"],
                          "description": "When the passage says it will happen, in its own words (\"in the year 2000\", \"within fifty years\"); null if it doesn't say."},
          "polarity":    {"type": "string", "enum": ["will", "will_not"],
                          "description": "will_not when the passage says it will never or cannot happen."},
          "confidence":  {"type": "string", "enum": ["asserted", "hedged"]},
          "valence":     {"type": "string", "enum": ["positive", "negative", "neutral", "mixed"],
                          "description": "How the passage presents it."},
          "voice":       {"type": "string", "enum": ["narrator", "sympathetic", "antagonist", "document"],
                          "description": "Who states it: the narrator or author, a sympathetic character, an antagonist or skeptic, or an in-world document."},
          "domain":      {"type": "string", "enum": ["computing", "communication", "transport", "energy", "medicine-biology",
                                                     "weapons-war", "space", "society-politics", "economy", "environment", "other"]},
          "second_order": {"type": "boolean",
                          "description": "True if it predicts a consequence of a technology or change rather than the thing itself."}
        }
      }
    }
  }
}
```

An empty `claims` list is a valid answer.
