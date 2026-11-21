"""Across the whole plan: any source used in more than one item (library ID or file), and counts by kind."""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plan import PLAN
use = collections.defaultdict(list)
for it in PLAN:
    for s in it.get("src", []): use[os.path.basename(s.split("@")[0])].append(it["id"])
d = {k: v for k, v in use.items() if len(v) > 1}
print(len(PLAN), "items:", sum(i["kind"] == "lt" for i in PLAN), "lower thirds,", sum(i["kind"] == "clip" for i in PLAN), "clips,", len(use), "sources")
print("used twice:", d or "none")
kinds = collections.Counter("pexels" if k.startswith("pexels") else ("library AI" if k[0] == "A" and k[1:5].isdigit() else ("library B" if k[0] == "B" and k[1:5].isdigit() else "other")) for k in use)
print(dict(kinds)); print("other:", [k for k in use if not (k.startswith("pexels") or (k[0] in "AB" and k[1:5].isdigit()))])
