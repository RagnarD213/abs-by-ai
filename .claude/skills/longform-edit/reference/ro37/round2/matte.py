"""RO-37 round 2 mattes: BiRefNet (Replicate 851-labs/background-remover, about $0.002 a frame) on every cut-out presenter
frame of the film ranges asked for, exactly the approved test method: the colour-F graded frame at 1152x2048 JPEG in,
the alpha kept at 1152x2048 (the compositor scales it with the picture and takes a 3-frame median). Stored per roll frame
(round2/matte/<roll>/<frame>.png), so a later round or the full film never pays for a frame twice.

  python3 matte.py estimate RANGES          RANGES = "0:61.1,140:150"  (film seconds) or "first-minute" / "contexts"
  python3 matte.py run RANGES [--threads 12] [--cap-usd 15]
"""
import io, json, os, subprocess, sys, time, threading, urllib.request, concurrent.futures as cf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r2
sys.path.insert(0, f"{r2.P}/.claude/skills/background-removal/scripts")
import removebg as RB
from PIL import Image
USD = 0.002
LEDGER = f"{r2.W2}/matte/ledger.json"


def ranges(spec):
    if spec == "first-minute": return [(0.0, 61.0944)]
    if spec == "contexts":
        return json.load(open(f"{r2.W2}/context_ranges.json"))
    return [tuple(float(x) for x in r.split(":")) for r in spec.split(",")]


def todo(spec):
    shots = r2.shots2(); need = {}
    if spec == "geo":
        return {roll: sorted(k for k in ks if not os.path.exists(r2.mpath(roll, k))) for roll, ks in r2.geo_frames(shots).items()}
    for a, b in ranges(spec):
        for roll, ks in r2.needed_frames(r2.fr(a), r2.fr(b), shots).items(): need.setdefault(roll, set()).update(ks)
    return {roll: sorted(k for k in ks if not os.path.exists(r2.mpath(roll, k))) for roll, ks in need.items()}


def runs(ks):
    out, cur = [], []
    for k in ks:
        if cur and k != cur[-1] + 1: out.append(cur); cur = []
        cur.append(k)
    if cur: out.append(cur)
    return out


def main():
    cmd, spec = sys.argv[1], sys.argv[2]
    T = todo(spec); n = sum(len(v) for v in T.values())
    print(f"{n} frames to matte ({', '.join(f'{r}: {len(v)}' for r, v in T.items())}), estimate ${n * USD:.2f}", flush=True)
    if cmd == "estimate" or not n: return
    cap = float(sys.argv[sys.argv.index("--cap-usd") + 1]) if "--cap-usd" in sys.argv else 15.0
    assert n * USD <= cap, f"estimate ${n * USD:.2f} is over the ${cap:.2f} cap for one batch: ask Dan first"
    threads = int(sys.argv[sys.argv.index("--threads") + 1]) if "--threads" in sys.argv else 12
    tok = RB.token(); ver = RB.latest_version(tok); lock = threading.Lock(); done = [0]; t0 = time.time()

    def one(job):
        roll, k, jpeg = job
        out = r2.mpath(roll, k)
        for attempt in range(4):
            try:
                url = RB.upload(tok, jpeg, f"{roll}_{k}.jpg")
                png = urllib.request.urlopen(RB.predict(tok, ver, url)).read(); break
            except Exception as e:
                if attempt == 3: raise
                time.sleep(4 * (attempt + 1))
        a = Image.open(io.BytesIO(png)).split()[-1]
        if a.size != (r2.MW, r2.MH): a = a.resize((r2.MW, r2.MH), Image.LANCZOS)
        a.save(out + ".tmp.png"); os.replace(out + ".tmp.png", out)
        with lock:
            done[0] += 1
            if done[0] % 100 == 0: print(f"  {done[0]}/{n} matted, {done[0] / (time.time() - t0):.2f}/s", flush=True)

    def frames(roll, ks):
        """graded frames of one contiguous run, as 1152x2048 JPEGs (decode once per run)"""
        k0 = ks[0]
        p = subprocess.Popen([r2.FF, "-nostdin", "-v", "error", "-ss", f"{(k0 - 0.5) / r2.FPS:.6f}", "-i", r2.F.ROLLS[roll], "-frames:v",
                              str(len(ks)), "-vf", f"{r2.F.DEC},{r2.F.GRADES['F'][1]},scale={r2.MW}:{r2.MH}:flags=lanczos,format=rgb24",
                              "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
        for k in ks:
            raw = p.stdout.read(r2.MW * r2.MH * 3); assert len(raw) == r2.MW * r2.MH * 3, f"{roll} frame {k} short"
            buf = io.BytesIO(); Image.frombytes("RGB", (r2.MW, r2.MH), raw).save(buf, "JPEG", quality=94); yield roll, k, buf.getvalue()
        p.stdout.close(); p.wait()

    with cf.ThreadPoolExecutor(threads) as ex:
        futs = []
        for roll, ks in T.items():
            os.makedirs(f"{r2.W2}/matte/{roll}", exist_ok=True)
            for run in runs(ks):
                for job in frames(roll, run):
                    futs.append(ex.submit(one, job))
                    while sum(not f.done() for f in futs) > threads * 4: time.sleep(0.2)
        for f in futs: f.result()
    led = json.load(open(LEDGER)) if os.path.exists(LEDGER) else []
    led.append(dict(when=time.strftime("%Y-%m-%d %H:%M"), spec=spec, frames=n, usd=round(n * USD, 2)))
    json.dump(led, open(LEDGER, "w"), indent=1)
    print(f"MATTE DONE {n} frames ${n * USD:.2f} in {time.time() - t0:.0f} s; ledger total ${sum(x['usd'] for x in led):.2f}", flush=True)


if __name__ == "__main__":
    main()
