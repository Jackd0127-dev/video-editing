"""Keep caption token indexes stable after re-cutting: give every old token its time in a new transcript.

Usage: python3 -I realign.py OLD_TOKENS.json NEW_TRANSCRIPT.json OUT_TOKENS.json
- Words are matched by text (difflib); 1:1 replacements ("hours" -> "ours") take the new time too.
- Anything left is interpolated between neighbours and printed so you can check it.
- Words that only exist in the new cut (a line you added back) are printed: append them to the end of
  the token list and reference the new indexes in the captions, so no existing index moves.
"""
import difflib
import json
import re
import sys

old = json.load(open(sys.argv[1]))
new = json.load(open(sys.argv[2]))
new = new if isinstance(new, list) else new["words"]
norm = lambda s: re.sub(r"[^a-z0-9']", "", s.lower())
sm = difflib.SequenceMatcher(a=[norm(w["text"]) for w in old], b=[norm(w["text"]) for w in new], autojunk=False)
out, done = [dict(w) for w in old], set()
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal" or (tag == "replace" and i2 - i1 == j2 - j1):
        for k in range(i2 - i1):
            out[i1 + k]["start"] = new[j1 + k]["start"]
            done.add(i1 + k)
    if tag in ("insert", "replace") and not (tag == "replace" and i2 - i1 == j2 - j1):
        print("new-only words:", [(w["text"], w["start"]) for w in new[j1:j2]])
for i in range(len(out)):
    if i not in done:
        p = max((k for k in range(i) if k in done), default=None)
        n = min((k for k in range(i + 1, len(out)) if k in done), default=None)
        if p is not None and n is not None:
            out[i]["start"] = round(out[p]["start"] + (out[n]["start"] - out[p]["start"]) * (i - p) / (n - p), 3)
        print("interpolated", i, out[i]["text"], out[i]["start"])
json.dump(out, open(sys.argv[3], "w"), indent=1)
print(f"{len(done)} of {len(old)} tokens matched exactly")
