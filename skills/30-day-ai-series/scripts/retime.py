"""Move caption tokens from an old cut to a new cut via source time.
Usage: python3 -I edit/retime.py edit/words-v1.json edit/tokens-v1.json  (after rebuilding the cut)"""
import json
import sys

old = json.load(open(sys.argv[1]))["segments"]
toks = json.load(open(sys.argv[2]))
new = json.load(open("edit/words.json"))["segments"]
out = []
for tk in toks:
    s = next(s for s in reversed(old) if s["start"] <= tk["start"] + 1e-6)
    src = s["src_in"] + tk["start"] - s["start"]
    n = next((n for n in new if n["src_in"] - 0.15 <= src < n["src_out"]), None)
    if n is None:  # token timed just before its segment's new in-point: pin it to that in-point
        n = min(new, key=lambda n: abs(n["src_in"] - src))
        print("pinned", tk["text"], "to segment", n["index"])
    out.append(dict(tk, start=round(n["start"] + max(src, n["src_in"]) - n["src_in"], 3)))
json.dump(out, open("edit/tokens.json", "w"), indent=0)
print(len(out), "tokens retimed")
