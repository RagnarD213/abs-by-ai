# RO-37 round 3 recipe: a cut-out long-form from real footage (pool, no green screen)

Provenance, not a launcher. Key order in `assemble.py` Presenter.read: refined matte (BiRefNet -> trimap -> ViTMatte small), `main_body`, `skinfill`, `gapmask`, `softmotion`, `decontaminate`, composite.

- `gapfix.py`: `gapmask` takes pool stone and tile back out of the cut-out by colour; `skinfill` puts moving warm skin back (both matte models thin a blurred finger into a claw); `softmotion` softens the matte edge where the picture moves fast. Tuning numbers come from measured wall colours: stone rg p99 0.066, tan stone p99 0.094. Too strict leaves chunks, too loose eats fingers.
- Audit on the delivered picture: `audit_key.py`, `audit_sheets.py`, then a moving-hand sheet (`hands3.py`), because the brightness audit misses finger faults. A fresh reviewer grades each pass.
- `sidehits.py` lists shots where an arm leaves the vertical camera frame. Right-placed shots can slide to the screen edge (`r2.DX`); left-side hits on right-placed shots cannot be fixed.
- Trim after picture lock: `r2.sh()` shifts every later time, `bg_plan3` and the manifest are rewritten once, only later chunks re-render.
- `review_server.py` serves a staged copy of the review folder: re-run it after changing the page or the page stays old.
