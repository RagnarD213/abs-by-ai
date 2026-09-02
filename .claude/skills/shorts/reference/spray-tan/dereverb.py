"""Moved to .claude/skills/_shared/audio/dereverb.py (2026-09-02), unchanged. Shim so
dereverb_sweep.py and any `from dereverb import dereverb` keep working."""
import sys
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio")
from dereverb import *          # noqa: F401,F403
if __name__ == "__main__":
    import runpy; runpy.run_path("/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/dereverb.py", run_name="__main__")
