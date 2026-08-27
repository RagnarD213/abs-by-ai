#!/usr/bin/env python3
"""Whisper with word timestamps and condition_on_previous_text=False.

The default (True) feeds the previous window's text back as a prompt, and on a roll with
repeated takes that makes the decoder skip a whole retake as "already said". On C1592 it
silently discarded a COMPLETE SECOND HOOK TAKE (32.2-46.9 s) and emitted one word in its
place. Always transcribe ad rolls with this off, then verify with orphan_scan.py.
"""
import sys, json, time, whisper
src, out = sys.argv[1], sys.argv[2]
model = sys.argv[3] if len(sys.argv) > 3 else "small"
t0=time.time(); m=whisper.load_model(model)
r=m.transcribe(src, word_timestamps=True, language="en", verbose=False,
               condition_on_previous_text=False)
json.dump(r, open(out,"w"))
print("done %.0fs segments=%d words=%d" % (time.time()-t0, len(r["segments"]),
      sum(len(s.get("words",[])) for s in r["segments"])))
