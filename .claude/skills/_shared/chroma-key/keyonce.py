"""Key a piece exactly once: skip it when its .done stamp matches, re-key only a piece whose inputs changed.

    python3 keyonce.py DONE_FILE --inputs FILE [FILE ...] [--params "T0 DUR ..."] -- COMMAND ...

The rule (Dan's house key, 2026-10-21, every recipe, Claude and Codex): each keyed piece of a green-screen video has a
.done stamp beside its cache. A round never re-keys a piece whose stamp matches. The stamp holds a fingerprint of
everything that decides the matte: the recipe code (stage scripts, keylib), the plate, the watch/glasses boxes and
the piece's times. Change one of them for one piece and only that piece is keyed again; the others are skipped.

    exit 0, "skipped"   the stamp matches: the cache is the approved key for these inputs
    exit 0, "keyed"     no stamp (or a stale one): COMMAND ran and succeeded, the stamp is written
    exit != 0           COMMAND failed: no stamp is written, the next run tries again

Calibrate first (calibrate.py, 2-3 s excerpts in the quick lane), then run the full key through this once.
"""
import hashlib, json, os, subprocess, sys, time
from pathlib import Path


def fingerprint(inputs, params):
    h = hashlib.sha256(params.encode())
    for f in sorted(inputs):
        p = Path(f)
        h.update(str(p.name).encode())
        with open(p, "rb") as fh:
            for block in iter(lambda: fh.read(1 << 20), b""):
                h.update(block)
    return h.hexdigest()


def main(argv):
    if "--" not in argv or len(argv) < 2:
        sys.exit(__doc__)
    cut = argv.index("--"); head, cmd = argv[:cut], argv[cut + 1:]
    done = Path(head[0]); inputs, params, k = [], "", 1
    while k < len(head):
        if head[k] == "--inputs":
            k += 1
            while k < len(head) and not head[k].startswith("--"):
                inputs.append(head[k]); k += 1
        elif head[k] == "--params":
            params = head[k + 1]; k += 2
        else:
            sys.exit(f"keyonce: unknown option {head[k]}")
    fp = fingerprint(inputs, params)
    if done.exists():
        try:
            old = json.loads(done.read_text())
        except ValueError:
            old = {"fingerprint": done.read_text().strip()}     # older plain stamps ("T0 N"): treated as stale
        if old.get("fingerprint") == fp:
            print(f"keyonce: {done.stem} skipped: already keyed with these inputs ({old.get('keyed', '?')})")
            return 0
        print(f"keyonce: {done.stem}: inputs changed since {old.get('keyed', 'an older stamp')}: keying this piece again", flush=True)
    t = time.time()
    rc = subprocess.call(cmd)
    if rc:
        print(f"keyonce: {done.stem} FAILED (exit {rc}); no stamp written")
        return rc
    tmp = done.with_name("." + done.name + ".tmp")
    tmp.write_text(json.dumps(dict(fingerprint=fp, params=params, inputs=sorted(inputs), command=cmd,
                                   keyed=time.strftime("%Y-%m-%d %H:%M"), minutes=round((time.time() - t) / 60, 1)), indent=1))
    os.replace(tmp, done)
    print(f"keyonce: {done.stem} keyed in {(time.time() - t) / 60:.1f} min; stamp {done}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
