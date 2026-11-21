#!/usr/bin/env python3
"""QC for the DS-05 covers: the Muhammad batch checks, pointed at this review folder."""
from pathlib import Path
import runpy,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'muhammad-batch-20261013'))
src=(Path(__file__).resolve().parents[1]/'muhammad-batch-20261013/qc.py').read_text().replace("'Short-form video content/covers/review/muhammad-batch-20261013'","'Short-form video content/covers/review/ds05-20261014'")
exec(compile(src,'qc.py','exec'),{'__file__':str(Path(__file__).resolve()),'__name__':'__main__'})
