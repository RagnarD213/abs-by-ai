"""raw Codex PNG -> skin texture cleanup (deskin.py) -> 1080x1920 JPEG. finalize.py RAW OUT"""
import sys, subprocess, os, tempfile
from PIL import Image
raw, out = sys.argv[1], sys.argv[2]; here = os.path.dirname(os.path.abspath(__file__))
t = tempfile.mktemp(suffix=".png"); subprocess.run([sys.executable, f"{here}/deskin.py", raw, t, "0"], check=True)
Image.open(t).convert("RGB").resize((1080, 1920), Image.LANCZOS).save(out, quality=95); os.remove(t); os.remove(t[:-4] + "_mask.png")
