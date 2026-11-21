"""print words in [a,b]: word@start-end (prob)"""
import json, sys
W=json.load(open("/Volumes/Extreme/_edit_work/RO-18/round1/words.json"))["words"]
for arg in sys.argv[1:]:
    a,b=map(float,arg.split("-")); print("==",arg)
    print(" ".join(f"{w['word'].strip()}@{w['start']:.2f}-{w['end']:.2f}" + ("" if w['p']>0.5 else f"({w['p']})") for w in W if a<=w["start"]<b))
