"""tokens.json for Day 14 ("sell websites to local businesses"): the cut's words (edit/trials/<n>/words.json, Parakeet
timings mapped through the cut) + mishear fixes checked against Whisper medium.en and the audio ("quick cash": one fricative,
no k-closure, so not "tasks").
Usage: python3 -I edit/mktokens.py <n>"""
import json, re, sys
n = sys.argv[1]
words = [{"text": x["text"], "start": x["start"]} for x in json.load(open(f"edit/trials/{n}/words.json"))["words"]]


def core(s):
    return re.sub(r"[^a-z0-9']", "", s.lower())


def tail(s):
    m = re.search(r"[,.!?;:]+$", s)
    return m.group(0) if m else ""


out = words


def fix(seq, rep):
    """Replace the word run `seq` (compared without case/punctuation) with `rep`; None drops a word. Punctuation carries
    over unless the replacement brings its own."""
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
                kept[0]["start"] = t0
            out = out[:k] + kept + out[k + L:]
        k += 1


fix(["if", "you're", "good", "at", "seals"], ["If", "you're", "good", "at", "sales"])
fix(["quick", "cough"], ["quick", "cash,"])
fix(["today", "i'm", "gonna", "show"], ["Today", "I'm", "gonna", "show"])
fix(["charisma"], ["Karizma"])
fix(["no", "what", "we're"], ["Now", "what", "we're"])
fix(["have", "uh", "fresh", "link"], ["have", "a", "Fresha", "link"])
fix(["new", "chart"], ["new", "chat,"])
fix(["it", "it's", "perfect"], [None, "it's", "perfect."])
fix(["adminnovasagencycom"], ["admin.novasagency.com."])
fix(["redundant"], ["redundant."])
for k in range(len(out) - 3):  # the cut keeps his "Then" (66.72 s in the take; Parakeet put it in the silence before)
    if [core(x["text"]) for x in out[k:k + 4]] == ["what", "you're", "gonna", "do"] and core(out[k + 4]["text"]) == "is" and core(out[k + 7]["text"]) == "go":
        out.insert(k, {"text": "Then", "start": round(out[k]["start"] - 0.14, 3)})
        break
fix(["you're", "gonna", "set"], ["You're", "gonna", "set"])
fix(["then", "head", "over", "to", "google"], ["Then", "head", "over", "to", "Google"])
fix(["this", "is", "gonna", "be", "a", "really"], ["This", "is", "gonna", "be", "a", "really"])
fix(["if", "you", "don't", "know"], ["If", "you", "don't", "know"])
fix(["maybe", "five", "more"], ["Maybe", "five", "more"])
fix(["it", "tells", "them"], ["It", "tells", "them"])
fix(["fully", "made", "site"], ["fully", "made", "site."])
fix(["but", "no", "they"], ["But", "no,", "they"])
fix(["anywhere", "else"], ["anywhere", "else,"])
fix(["actually", "going", "to", "be", "active", "businesses"], ["actually", "going", "to", "be", "active", "businesses."] if n == "2" else ["actually", "going", "to", "be", "active", "businesses"])
json.dump(out, open(f"edit/trials/{n}/tokens.json", "w"), indent=0)
print(" ".join(x["text"] for x in out))
