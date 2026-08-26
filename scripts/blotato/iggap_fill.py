import json,os,sys,time,urllib.request,urllib.error,re
SP=os.path.dirname(os.path.abspath(__file__))
PLAN="iggap_plan.json"; STATEF="iggap_state.json"
ROOT="/Users/danielrose/Documents/Claude/Projects/Abs By AI"
BASE="https://backend.blotato.com/v2"
KEY=open(os.path.join(ROOT,"Business","blotato-api-key.txt")).read().strip()
STATE=os.path.join(SP,STATEF)
state=json.load(open(STATE)) if os.path.exists(STATE) else {}

def call(method,path,body=None,retries=5):
    data=json.dumps(body).encode() if body is not None else None
    for _ in range(retries):
        h={"blotato-api-key":KEY}
        if data is not None: h["Content-Type"]="application/json"
        req=urllib.request.Request(BASE+path,data=data,method=method,headers=h)
        try:
            with urllib.request.urlopen(req) as r:
                raw=r.read(); return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as e:
            p=e.read().decode(errors="replace")
            if e.code==429:
                w=30; m=re.search(r"retry in (\d+)",p)
                if m: w=int(m.group(1))+2
                print("  429, waiting",w,flush=True); time.sleep(w); continue
            raise SystemExit(f"{method} {path} -> {e.code} {p}")
    raise SystemExit("gave up "+path)

plan=json.load(open(os.path.join(SP,PLAN)))
apply="--apply" in sys.argv
for i,p in enumerate(plan):
    key=f"{p['account']}|{p['day']}|{p['slug']}"
    if key in state: continue
    if i==0:
        state[key]={"response":{"note":"created via MCP","postSubmissionId":"93965937-7958-45a3-a1c1-e6c9f963ccf0"},"scheduledTime":p['day']+"T22:00:00.000Z"}
        json.dump(state,open(STATE,"w"),indent=1); continue
    body={"post":{"accountId":p['account'],
                  "target":{"targetType":"instagram","firstComment":p['fc']},
                  "content":{"platform":"instagram","text":p['text'],"mediaUrls":[p['url']]}},
          "scheduledTime":p['day']+"T22:00:00.000Z"}
    if not apply:
        print("DRY",key); continue
    res=call("POST","/posts",body)
    state[key]={"response":res,"scheduledTime":body["scheduledTime"]}
    json.dump(state,open(STATE,"w"),indent=1)
    print(f"[{i+1}/{len(plan)}] {p['handle']} {p['day']} {p['slug']} -> {res.get('postSubmissionId','?')}",flush=True)
    time.sleep(1.0)
print("done. created:",len(state))
