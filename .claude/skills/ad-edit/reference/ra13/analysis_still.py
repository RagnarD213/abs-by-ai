import sys,json
from pathlib import Path
W=Path('/Volumes/Extreme/_edit_work/ra13');R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');SH=R/'.claude/skills/_shared'
sys.path[:0]=[str(SH),str(SH/'adkit')]
import softblue as B,analysis_card as AC,cardlib as L
AC.LIME=B.SPECULAR;AC.OLIVE=B.CYAN;AC.PLAN_GREEN=(22,70,124);L.OLIVE=B.GLASS_LINE;L.field=lambda A:B.field(0,*A.size).convert('RGBA')
# Sample the final settled frame from the canonical generator; do not retain a full animation in memory.
AC.range=lambda n:[n-1]
f,m=AC._frames(str(R/'Media/example pictures/dan by pool.png'),L.Aspect('9x16'),5.5,AC.ROWS,AC.FOOTER,'ai',str(W/'round1/stills'),'A1')
f[0].convert('RGB').save(W/'round1/stills/A1.jpg',quality=94)
json.dump(m,open(W/'round1/stills/A1.json','w'),indent=2)
print('ANALYSIS STILL READY')
