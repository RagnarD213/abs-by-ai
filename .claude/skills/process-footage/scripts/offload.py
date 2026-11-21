#!/usr/bin/env python3
"""Offload one camera card: copy every clip to the Extreme shoot folder and the Seagate archive in a
single read of the card, then prove every copy with SHA-256.

Run it on the Mac the drives are plugged into (the M2 since 2026-11-14; from the M6 use `ssh m2`).

    offload.py scan                                   # list cards, clips, sizes, camera dates, free space
    offload.py copy --shoot "11:13 dan rose fitness shoot - green screen" [--card /Volumes/Untitled]
                    [--stray-before 2026-11-12] [--extreme-later] [--dry-run]
    offload.py fill-extreme --shoot "..."             # later: bring Seagate-only clips onto the Extreme
    offload.py verify --shoot "..."                   # re-hash every clip on both drives against the manifest

How a copy works (learned on the 11/13 shoot):
* The card is read ONCE per clip; that stream is hashed and written to the Extreme and the Seagate at the
  same time (`tee`). Both copies are then re-read and must match the card hash. A clip is never marked OK
  on a size match alone: the Seagate silently corrupted copies on 2026-11-01 to 11-03, and on 2026-11-14 a
  card that had been put back in the reader misreported a 60 GB clip as 4 GB.
* If the Extreme lacks room (clip + 8 GB margin), the clip goes to the Seagate only and is listed as
  `extreme_pending`; free space (jobarchive, see SKILL.md) and run `fill-extreme`. With --extreme-later every
  clip goes Seagate-first (fastest when the Extreme is busy or full).
* Clips whose camera date is before --stray-before are filed on the Seagate under
  `not this shoot - <clip> <date>/` and never on the Extreme.
* Everything is recorded in `<Extreme shoot folder>/.offload-manifest.json` (and a copy beside the Seagate
  folder): card hash, size, both verified hashes, timestamps. Re-running skips verified clips, so a second
  card for the same shoot just runs `copy` again.
* The card is never written to, renamed or formatted.
"""
import argparse, datetime, hashlib, json, os, re, shutil, subprocess, sys, xml.etree.ElementTree as ET

EXTREME = os.environ.get("PF_EXTREME", "/Volumes/Extreme")          # env overrides: tests only
SEAGATE_ROOT = os.environ.get("PF_SEAGATE", "/Volumes/Expansion/Abs By AI Raw Footage")
MARGIN = 8 * 10**9
CHUNK = 8 * 1024 * 1024
VIDEO_EXT = (".mp4", ".mov", ".mxf", ".insv", ".360")


def log(*a):
    print(*a, flush=True)


def cards():
    """Mounted removable camera cards: Sony (PRIVATE/M4ROOT/CLIP) or DCIM-style (GoPro, phones)."""
    found = []
    for v in sorted(os.listdir("/Volumes")):
        p = os.path.join("/Volumes", v)
        if v in ("Extreme", "Expansion", "Macintosh HD"):
            continue
        sony = os.path.join(p, "PRIVATE", "M4ROOT", "CLIP")
        if os.path.isdir(sony):
            found.append((p, sony))
        elif os.path.isdir(os.path.join(p, "DCIM")):
            found.append((p, os.path.join(p, "DCIM")))
    return found


def clips_on(clipdir):
    out = []
    for root, _, files in os.walk(clipdir):
        for f in sorted(files):
            if f.startswith("._") or not f.lower().endswith(VIDEO_EXT) or f.lower().endswith(".lrv"):
                continue
            path = os.path.join(root, f)
            stem = os.path.splitext(f)[0]
            side = [os.path.join(root, x) for x in os.listdir(root)
                    if x.startswith(stem) and x != f and not x.startswith("._") and x.lower().endswith((".xml", ".thm"))]
            out.append({"name": f, "stem": stem, "path": path, "size": os.path.getsize(path),
                        "sidecars": side, "date": camera_date(path, side)})
    return out


def camera_date(path, sidecars):
    """Camera CreationDate from the Sony XML when present, else the file's modified time."""
    for s in sidecars:
        if s.lower().endswith(".xml"):
            try:
                for el in ET.parse(s).iter():
                    if el.tag.endswith("CreationDate"):
                        return el.attrib.get("value", "")[:19]
            except Exception:
                pass
    return datetime.datetime.fromtimestamp(os.path.getmtime(path)).isoformat()[:19]


def free(path):
    return shutil.disk_usage(path).free


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(CHUNK)
            if not b:
                return h.hexdigest()
            h.update(b)


def tee_copy(src, dests):
    """Read src once; write every dest (as .partial, then rename); return the hash of the bytes read."""
    h = hashlib.sha256()
    outs = [open(d + ".partial", "wb") for d in dests]
    try:
        with open(src, "rb") as f:
            while True:
                b = f.read(CHUNK)
                if not b:
                    break
                h.update(b)
                for o in outs:
                    o.write(b)
    finally:
        for o in outs:
            o.close()
    for d in dests:
        os.replace(d + ".partial", d)
    return h.hexdigest()


def manifest_path(shoot):
    return os.path.join(EXTREME, shoot, ".offload-manifest.json")


def load_manifest(shoot):
    for p in (manifest_path(shoot), os.path.join(SEAGATE_ROOT, shoot, ".offload-manifest.json")):
        if os.path.exists(p):
            return json.load(open(p))
    return {"shoot": shoot, "clips": {}}


def save_manifest(shoot, m):
    for d in (os.path.join(EXTREME, shoot), os.path.join(SEAGATE_ROOT, shoot)):
        if os.path.isdir(d):
            tmp = os.path.join(d, ".offload-manifest.json.tmp")
            json.dump(m, open(tmp, "w"), indent=1)
            os.replace(tmp, os.path.join(d, ".offload-manifest.json"))


def cmd_scan(a):
    for vol, cdir in cards():
        cl = clips_on(cdir)
        log(f"CARD {vol}  ({len(cl)} clips, {sum(c['size'] for c in cl)/1e9:.1f} GB)")
        for c in cl:
            log(f"  {c['name']:<14} {c['size']/1e9:7.2f} GB  camera {c['date']}")
    for p in (EXTREME, os.path.dirname(SEAGATE_ROOT)):
        log(f"FREE {p}: {free(p)/1e9:.0f} GB" if os.path.isdir(p) else f"MISSING {p}")


def cmd_copy(a):
    found = [c for c in cards() if not a.card or c[0] == a.card.rstrip("/")]
    if a.card and not found and os.path.isdir(os.path.join(a.card, "PRIVATE", "M4ROOT", "CLIP")):
        found = [(a.card.rstrip("/"), os.path.join(a.card, "PRIVATE", "M4ROOT", "CLIP"))]
    if len(found) != 1:
        sys.exit(f"Need exactly one card (found {[c[0] for c in found]}); pass --card")
    vol, cdir = found[0]
    ext_dir, sea_dir = os.path.join(EXTREME, a.shoot), os.path.join(SEAGATE_ROOT, a.shoot)
    m = load_manifest(a.shoot)
    todo = clips_on(cdir)
    log(f"Card {vol}: {len(todo)} clips -> {ext_dir} + {sea_dir}")
    if a.dry_run:
        for c in todo:
            st = m["clips"].get(c["name"], {}).get("status", "new")
            log(f"  {c['name']} {c['size']/1e9:.2f} GB {c['date']} [{st}]")
        return
    os.makedirs(ext_dir, exist_ok=True)
    os.makedirs(sea_dir, exist_ok=True)
    for c in todo:
        rec = m["clips"].get(c["name"], {})
        if rec.get("status") in ("ok", "extreme_pending") and rec.get("size") == c["size"]:
            log(f"skip {c['name']} ({rec['status']})")
            continue
        if rec.get("size") and rec["size"] != c["size"]:
            log(f"WARN {c['name']}: card now reports {c['size']} bytes, manifest has {rec['size']}. "
                "Card may be damaged; the verified drive copies are kept and this clip is not recopied.")
            continue
        stray = bool(a.stray_before and c["date"][:10] < a.stray_before)
        sub = f"not this shoot - {c['stem']} {c['date'][:10]}" if stray else ""
        s_out = os.path.join(sea_dir, sub)
        os.makedirs(s_out, exist_ok=True)
        dests = [os.path.join(s_out, c["name"])]
        to_extreme = not stray and not a.extreme_later and free(EXTREME) > c["size"] + MARGIN
        if to_extreme:
            dests.append(os.path.join(ext_dir, c["name"]))
        log(f"copy {c['name']} {c['size']/1e9:.1f} GB -> {'Extreme+Seagate' if to_extreme else 'Seagate only'}"
            f"{' (stray, ' + c['date'][:10] + ')' if stray else ''} {datetime.datetime.now():%H:%M:%S}")
        for s in c["sidecars"]:
            for d in dests:
                shutil.copy2(s, os.path.dirname(d))
        card_hash = tee_copy(c["path"], dests)
        got = {d: sha(d) for d in dests}
        bad = [d for d, v in got.items() if v != card_hash]
        rec = {"size": c["size"], "camera_date": c["date"], "card_hash": card_hash, "stray": stray,
               "seagate": dests[0], "extreme": dests[1] if to_extreme else None,
               "verified": datetime.datetime.now().isoformat(timespec="seconds"),
               "status": "FAIL" if bad else ("ok" if to_extreme or stray else "extreme_pending")}
        m["clips"][c["name"]] = rec
        save_manifest(a.shoot, m)
        log(("FAIL " + ", ".join(bad)) if bad else f"OK {c['name']} {rec['status']} {card_hash[:12]}")
    summary(m)


def cmd_fill(a):
    m = load_manifest(a.shoot)
    ext_dir = os.path.join(EXTREME, a.shoot)
    for name, rec in m["clips"].items():
        if rec.get("status") != "extreme_pending":
            continue
        if free(EXTREME) < rec["size"] + MARGIN:
            log(f"wait {name}: Extreme has {free(EXTREME)/1e9:.0f} GB free, needs {(rec['size']+MARGIN)/1e9:.0f}")
            continue
        src, dst = rec["seagate"], os.path.join(ext_dir, name)
        for x in os.listdir(os.path.dirname(src)):
            if x.startswith(os.path.splitext(name)[0]) and x.lower().endswith((".xml", ".thm")):
                shutil.copy2(os.path.join(os.path.dirname(src), x), ext_dir)
        tee_copy(src, [dst])
        if sha(dst) == rec["card_hash"]:
            rec.update(extreme=dst, status="ok", verified=datetime.datetime.now().isoformat(timespec="seconds"))
            log(f"OK {name} on Extreme")
        else:
            log(f"FAIL {name}: Extreme copy does not match the card hash")
        save_manifest(a.shoot, m)
    summary(m)


def cmd_verify(a):
    m = load_manifest(a.shoot)
    bad = 0
    for name, rec in sorted(m["clips"].items()):
        for k in ("extreme", "seagate"):
            p = rec.get(k)
            if not p:
                continue
            ok = os.path.exists(p) and sha(p) == rec["card_hash"]
            bad += not ok
            log(f"{'OK  ' if ok else 'FAIL'} {k:<8} {name}")
    log("ALL VERIFIED" if not bad else f"{bad} FAILURES")


def summary(m):
    st = {}
    for r in m["clips"].values():
        st[r["status"]] = st.get(r["status"], 0) + 1
    log("SUMMARY " + json.dumps(st))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("scan")
    c = sp.add_parser("copy")
    c.add_argument("--shoot", required=True, help='e.g. "11:13 dan rose fitness shoot - green screen"')
    c.add_argument("--card")
    c.add_argument("--stray-before", help="YYYY-MM-DD; clips filmed before this date are filed as strays")
    c.add_argument("--extreme-later", action="store_true", help="copy to the Seagate only now; fill-extreme later")
    c.add_argument("--dry-run", action="store_true")
    for n in ("fill-extreme", "verify"):
        s = sp.add_parser(n)
        s.add_argument("--shoot", required=True)
    a = ap.parse_args()
    if a.cmd != "scan" and not re.match(r"^\d{1,2}:\d{1,2} ", a.shoot):
        sys.exit('Shoot folder must start with the date as "M:DD " so the nightly backup finds it')
    {"scan": cmd_scan, "copy": cmd_copy, "fill-extreme": cmd_fill, "verify": cmd_verify}[a.cmd](a)
