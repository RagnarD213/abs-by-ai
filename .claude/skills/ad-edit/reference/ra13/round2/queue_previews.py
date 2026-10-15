from pathlib import Path
import sys
sys.path.insert(0,'/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared')
import buildcap
buildcap.wait('RA-13 R2 previews')
p=Path('/Volumes/Extreme/_edit_work/ra13/round2/recipe/build_previews.py')
exec(compile(p.read_text(),str(p),'exec'),{'__file__':str(p),'__name__':'__main__'})
