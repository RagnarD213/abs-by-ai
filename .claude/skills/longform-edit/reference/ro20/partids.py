"""ids of one plan part by its letter. usage: partids.py <letter> lt|all|ltA|ltB   (ltA / ltB = the part's lower thirds split in two for two render workers)"""
import json, sys
R = json.load(open("/Volumes/Extreme/_edit_work/ro20/plan_resolved.json")); L, k = sys.argv[1], sys.argv[2]
sp = {"a": ["O1", "A1"], "c": ["A2"], "d": ["A3"], "g": ["A4"], "h": ["P01"]}
x = [r["id"] for r in R if (len(r["id"]) == 4 and r["id"][0] in "GC" and r["id"][1] == L) or r["id"] in sp.get(L, [])]
lt = [i for i in x if i[0] == "G"]
print({"all": " ".join(x), "lt": ",".join(lt), "ltA": ",".join(lt[0::2]), "ltB": ",".join(lt[1::2])}[k])
