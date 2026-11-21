"""Paths for the SL-18 cover scripts. Media lives in the main checkout (git-ignored), so a worktree resolves to it."""
from pathlib import Path
import subprocess
def _main():
 here=Path(__file__).resolve().parents[3]
 if (here/'photos/finalized social media photos').exists():return here
 g=subprocess.run(['git','-C',str(here),'rev-parse','--git-common-dir'],capture_output=True,text=True,check=True).stdout.strip()
 return (here/g).resolve().parent if not Path(g).is_absolute() else Path(g).resolve().parent
P=_main();R=P/'Short-form video content/covers/review/sl18-20261022';PH=P/'photos/finalized social media photos';CUT=PH/'_cutouts'
