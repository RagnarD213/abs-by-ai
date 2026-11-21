"""Moved to .claude/skills/_shared/motionlib.py (2026-08-24).

/longform-edit needs the same animated-graphics pack /ad-edit has been using since
August. Keeping one copy per skill is how the longform edits ended up shipping static
PNG chips while the ad edits had animation. Import from the shared location; this shim
exists so nothing that already points here breaks.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_shared"))
from motionlib import *          # noqa: F401,F403
