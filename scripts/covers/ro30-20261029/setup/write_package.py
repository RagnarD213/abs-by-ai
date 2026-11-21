from pathlib import Path
import subprocess,os,concurrent.futures,json
P=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');D=Path('/Volumes/Extreme/_edit_work/RO-30/setup/install')
def run(spec):
 k,fmt,n,pos,kind=spec
 cmd=['python3',str(P/'scripts/voice/write.py'),'--type','content','--format',fmt,'--plan',str(D/f'{k}-plan.md'),'--his-words',str(D/'his-words.txt'),'--words',str(n),'--position',pos,'--seed','RO30-'+k,'--kind',kind,'--out',str(D/f'{k}-draft.txt')]
 with open(D/f'{k}-writer.log','w') as log:rc=subprocess.run(cmd,cwd=P,env=dict(os.environ,VOICE_BENCH_BACKEND='cli',CLAUDE_CODE_EFFORT_LEVEL='high'),stdout=log,stderr=subprocess.STDOUT).returncode
 print(k,rc,flush=True);return dict(part=k,exit_code=rc)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:res=list(ex.map(run,[('metadata','short',260,'whole','a JSON package of YouTube description opening, social caption, question comment and search excerpt'),('article-a','video',470,'opening','the opening half of a first-person website article based on his own finished video'),('article-b','video',470,'close','the closing half of the same first-person website article')]))
(D/'writing-complete.json').write_text(json.dumps(res,indent=2)+'\n')
