"""The shared HyperFrames 9:16 module loaded a second time at 1920x1080 (the way square.py makes the 1:1), for RA-06's 16:9 (copied from RA-15 round 3).
Lower thirds land on the approved 16:9 reference box (x 86..1828, bottom 1016: softblue.lower_third_default_box); captions sit
at 930-1040 (ra01lib.Aspect('16x9')), so a card ends at 900."""
import importlib.util, pathlib, sys
HF = pathlib.Path("/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes")
sys.path.insert(0, str(HF))
_spec = importlib.util.spec_from_file_location("vertical_h16", HF / "vertical.py")
V = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(V)
W, Hh = 1920, 1080
V.W, V.Hh, V.CANVAS = W, Hh, [W, Hh]
V.U = V.B.unit(W, Hh)              # 2.0
V.CAP_TOP = 930
V.CARD_END = 900
V.CAPTION_BAND = (910, 1060)
