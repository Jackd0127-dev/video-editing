"""tokens.json for Day 13 (Jack's own pre-cut file, one take): Parakeet words + fixes; the 'database' sentence Parakeet
dropped comes from Whisper (medium.en) timings; Jess's (the AI receptionist's) lines are tagged spk=jess.
Usage: python3 -I edit/mktokens.py 1"""
import json, re, sys
n = sys.argv[1]
tx = json.load(open(f"edit/trials/{n}/tx-raw.json"))
tx = tx.get("words", tx) if isinstance(tx, dict) else tx
END = 135.3
words = [{"text": x["text"], "start": round(x["start"], 3)} for x in tx if x["start"] < END]
DB = [("I", 111.05), ("had", 111.2), ("to", 111.32), ("set", 111.48), ("up", 111.55), ("a", 111.62), ("bit", 111.68), ("of", 111.86),
      ("a", 111.98), ("database", 112.04), ("so", 112.6), ("it", 112.68), ("can", 112.8), ("take", 112.95), ("bookings", 113.18),
      ("and", 113.55), ("stuff", 113.7), ("like", 114.0), ("that.", 114.15)]
words += [{"text": a, "start": b} for a, b in DB]
words.sort(key=lambda x: x["start"])
def core(s):
    return re.sub(r"[^a-z0-9']", "", s.lower())
def tail(s):
    m = re.search(r"[,.!?;:]+$", s); return m.group(0) if m else ""
out = words
def fix(seq, rep):
    global out
    L = len(seq)
    k = 0
    while k <= len(out) - L:
        if [core(x["text"]) for x in out[k:k + L]] == seq:
            t0 = out[k]["start"]
            for j, r in enumerate(rep):
                out[k + j]["text"] = None if r is None else (r if tail(r) else r + tail(out[k + j]["text"]))
            kept = [x for x in out[k:k + L] if x["text"] is not None]
            if kept:
                kept[0]["start"] = t0  # a merged phrase lands at its first word
            out = out[:k] + kept + out[k + L:]
        k += 1
fix(["13"], ["thirteen"])
fix(["30"], ["thirty"])
fix(["wedding", "on", "event"], ["wedding", "and", "event"])
fix(["the", "seum"], ["the", "same"])
fix(["do", "you", "use", "weddings"], ["do", "you", "do", "weddings"])
fix(["guests", "should", "be"], ["guests", "would", "be"])
fix(["um", "do", "you"], [None, "Do", "you"])
fix(["vegans"], ["vegans?"])
fix(["any", "do", "you"], ["any.", "Do", "you"])
fix(["book", "a", "view", "on"], ["book", "a", "viewing", "or"])
fix(["the", "air", "reception"], ["the", "AI", "receptionist."])
fix(["twenty", "four", "seven"], [None, None, "24/7,"])
fix(["thanks", "jess"], ["Thanks,", "Jess."])
for k in range(len(out) - 1):  # "So 200 guests would be above…" is one sentence
    if out[k]["text"] == "guests." and out[k + 1]["text"] == "would":
        out[k]["text"] = "guests"
# Jess (the AI on speaker): her turns, by the first and last words of each
JESS = [("hey", 20.9, "help?"), ("we", 31.2, "that."), ("i'm", 53.1, "answer."), ("yes,", 78.1, "house."), ("no", 94.9, "day."), ("you're", 102.7, "bye.")]
for first, at, last in JESS:
    on = False
    for x in out:
        if not on and x["start"] >= at - 0.05 and core(x["text"]) == core(first):
            on = True
        if on:
            x["spk"] = "jess"
            if x["text"].lower() == last:
                break
json.dump(out, open(f"edit/trials/{n}/tokens.json", "w"), indent=0)
print(" ".join(("*" if x.get("spk") else "") + x["text"] for x in out))
