#!/usr/bin/env python3
"""SL-07 review: one sheet (REVIEW_all.jpg) and one page (index.html) with all 25 cover choices, both layouts, one row per short.
Uses the Muhammad batch review layout."""
from pathlib import Path
import importlib.util
here=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('build',here/'build.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
src=(here.parent/'muhammad-batch-20261013/review.py').read_text()
src=src.replace('sys.path.insert(0,str(Path(__file__).parent));from build import COPY,ORDER,R,POOL,STUDIO','')
src=src.replace("COPY[k][2]","COPY[k][1]").replace("COPY[k][3]","COPY[k][2]").replace("COPY[k][0]+' / '","").replace('{html.escape(COPY[k][0])} / {html.escape(" ".join(COPY[k][1]))}','Lose Your Belly Fat / {html.escape(" ".join(COPY[k][0]))}')
src=src.replace('MUHAMMAD DEDICATED SHORTS: FIVE COVER CHOICES PER SHORT','IF I HAD BELLY FAT SHORTS: FIVE COVER CHOICES PER SHORT').replace('Muhammad dedicated Shorts: cover choices','If I Had Belly Fat Shorts: cover choices').replace('Muhammad Shorts Covers','Belly Fat Shorts Covers')
src=src.replace("'C':'C: AI design 1','D':'D: AI design 2','E':'E: AI design 3'","'C':'C: AI image of you','D':'D: Codex choice 1','E':'E: Codex choice 2'")
src=src.replace("{r+1}. {html.escape(COPY[k][2])} <span style=\"color:#8fa1b1;font-size:15px\">({k.upper()})</span>","Short {r+1}: {html.escape(COPY[k][2])}").replace("f'{r+1}. {COPY[k][2]}  ({k.upper()})'","f'Short {r+1}: {COPY[k][2]}'")
src=src.replace('Real studio photo ({STUDIO[k]}) on an AI scene','Real studio photo ({STUDIO[k]}) on an AI scene, white outline').replace('Reply with one letter per short, for example \\"1 C, 2 A, 3 B\\".','Reply with one letter per short, for example \\"1 C, 2 A, 3 B, 4 D, 5 E\\".')
g={'__name__':'__main__','__file__':str(here/'review.py'),'COPY':b.COPY,'ORDER':b.ORDER,'R':b.R,'POOL':b.POOL,'STUDIO':b.STUDIO}
exec(compile(src,'review.py','exec'),g)
