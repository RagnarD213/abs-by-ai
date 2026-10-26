"""After verified delivery/queue update, reconcile only the Dad Bod records."""
from pathlib import Path
import json,hashlib,re,shutil
W=Path(__file__).resolve().parents[1];R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');T=Path('/Users/danielrose/.codex/worktrees/dad-bod-r3-recipes/Abs By AI');JOB='DS-35';J='Handoffs/video-editing/DS-35-women-say-they-love-the-dad-bod-they-dont.md'
release=json.loads((W/'review/release-receipt.json').read_text());delivery=json.loads((W/'delivery-receipt.json').read_text());assert release['browser_verified'] and delivery['status']=='delivered_for_Dan_review'
for x in delivery['files']:
 for k in ['path','vlc_path']:assert hashlib.sha256(Path(x[k]).read_bytes()).hexdigest()==x['sha256']
source=json.loads((R/'Handoffs/video-editing/jobs.json').read_text());job=next(x for x in source['jobs'] if x['id']==JOB);assert job['state']=='delivered'
board='**Dad Bod SFC R3 - REVIEW 2026-10-25, Codex.** Both complete revisions await Dan at http://127.0.0.1:9241/. Full VLC copies are in Videos to Review. Next: Dan’s review choice in Docs/DAN_DECISIONS.md. Edit slot released for review.'
decision='- **Dad Bod SFC R3 (2026-10-25; Decision since: 2026-10-25):** [Review both complete takes](http://127.0.0.1:9241/). Check 0:09–0:17 in both and 0:31–0:36 in Scripted, then choose Scripted or Off The Cuff and give any remaining notes. Both are independently checked; full-quality VLC copies are in Videos to Review.'
def own_replace(path,pattern,value):
 s=path.read_text();s,n=re.subn(pattern,lambda m:value,s,count=1,flags=re.M);assert n==1,(path,pattern);path.write_text(s)
# Primary job brief is owned here; preserve its original first-cut context below the preface.
s=(R/J).read_text();body=s[s.index('# DS-35:'):]
head='''**CONTENT SFC.** Task name: `Dad Bod SFC R3`.

**Round 3 review delivered 2026-10-25, Codex.** [Paired review](http://127.0.0.1:9241/), Scripted 57.5s and Off The Cuff 61.1s. Check both 0:09–0:17 for larger Craig photo, exact label/arrow and repaired watching camera edge; Scripted 0:31–0:36 for the stronger real studio photo. Both exact full files have fresh independent reviews and maintained PASS delivery gates, with selected audio and diagnostic limits retained. Await Dan’s take choice and notes. Full copies are in `Short-form video content/Dad Bod - DS-35/` and `Videos to Review/`. Receipt: `/Volumes/Expansion/_edit_work/DS-35/round3/delivery-receipt.json`. Nothing is approved, uploaded or scheduled. Original first-cut context follows.

'''
(R/J).write_text(head+body)
for root in [R,T]:
 own_replace(root/'AI_COORDINATION.md',r'^\*\*Dad Bod SFC R[23] - [^\n]+',board)
 own_replace(root/'Docs/DAN_DECISIONS.md',r'^- \*\*Dad Bod SFC R[23] \([^\n]+',decision)
shutil.copy2(R/J,T/J)
# Copy just DS-35, never another session’s dirty status records or master rows.
p=T/'Handoffs/video-editing/jobs.json';x=json.loads(p.read_text());i=next(i for i,a in enumerate(x['jobs']) if a['id']==JOB);x['jobs'][i]=job;p.write_text(json.dumps(x,indent=1,ensure_ascii=False)+'\n')
row=next(s for s in (R/'Handoffs/video-editing/00-MASTER.md').read_text().splitlines() if '| [DS-35](' in s)
p=T/'Handoffs/video-editing/00-MASTER.md';s=p.read_text();s,n=re.subn(r'^\| \[DS-35\]\([^\n]+',lambda m:row,s,count=1,flags=re.M);assert n==1;p.write_text(s)
print('ONLY_DAD_BOD_METADATA_RECONCILED')
