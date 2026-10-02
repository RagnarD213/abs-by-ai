import json,subprocess,sys,re,urllib.request
DOC="13uu4k9y2ttOWD9sp3KU-OLAeCNO74-3pWeIrBjcgVhk"
md=open(sys.argv[1]).read().strip("\n").split("\n")
text="";paras=[]  # (start,end,kind,level)
bolds=[]
for ln in md:
    if not ln.strip(): continue
    kind="p";lvl=0
    if ln.startswith("## "): kind="h2"; ln=ln[3:]
    m=re.match(r'^( *)- (.*)$',ln)
    if m: kind="b"; lvl=len(m.group(1))//4; ln=m.group(2)
    ln=ln.replace("\\*","\x00")
    start=1+len(text)
    pre="\t"*lvl if kind=="b" else ""
    text+=pre
    parts=re.split(r'\*\*',ln)
    for i,p in enumerate(parts):
        p=p.replace("\x00","*")
        s=1+len(text); text+=p
        if i%2==1 and p: bolds.append((s,1+len(text)))
    text+="\n"
    paras.append((start,1+len(text),kind,lvl))
end=1+len(text)
reqs=[{"insertText":{"location":{"index":1},"text":text}},
 {"updateParagraphStyle":{"range":{"startIndex":1,"endIndex":end},"paragraphStyle":{"namedStyleType":"NORMAL_TEXT"},"fields":"namedStyleType"}},
 {"updateTextStyle":{"range":{"startIndex":1,"endIndex":end},"textStyle":{"bold":False},"fields":"bold"}}]
for s,e,k,l in paras:
    if k=="h2": reqs.append({"updateParagraphStyle":{"range":{"startIndex":s,"endIndex":e},"paragraphStyle":{"namedStyleType":"HEADING_2"},"fields":"namedStyleType"}})
for s,e in bolds: reqs.append({"updateTextStyle":{"range":{"startIndex":s,"endIndex":e},"textStyle":{"bold":True},"fields":"bold"}})
# bullet runs, bottom to top
runs=[];cur=None
for s,e,k,l in paras:
    if k=="b":
        if cur: cur[1]=e
        else: cur=[s,e]
    else:
        if cur: runs.append(cur); cur=None
if cur: runs.append(cur)
for s,e in reversed(runs): reqs.append({"createParagraphBullets":{"range":{"startIndex":s,"endIndex":e-1},"bulletPreset":"BULLET_DISC_CIRCLE_SQUARE"}})
print(json.dumps(reqs,ensure_ascii=False))
