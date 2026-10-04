#!/usr/bin/env python3
"""The square's captions: the vertical's words, groups and timings, drawn for a 1080x1080 frame at CAP_Y 880 -> cap_sq/."""
import sys
sys.path.insert(0, '.')
import g5; g5.VH = 1080; g5.CAP_Y = 880
import captions as C
C.VH = 1080; C.CAP_Y = 880
ws = C.load_words(); gs = C.groups(ws, C.suppressed()); C.render(gs, capdir=sys.argv[1] if len(sys.argv) > 1 else 'cap_sq')
