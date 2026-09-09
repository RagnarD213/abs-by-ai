#!/usr/bin/env python3
"""List the real contents of a link-shared Google Drive folder, without a browser.

Why this exists: Drive's search API cannot see a file dropped into a folder that was
shared with Dan earlier — it is indexed only once Dan opens it. That blind spot cost a
missed delivery on 2026-09-09 (a 545 MB MP4 invisible for 6 h; its .srt invisible all day).
The folder's own HTML page, fetched anonymously, lists every child. Pair each id with the
Drive MCP's get_file_metadata, which DOES work by id even when search returns nothing.

    python3 folder_scan.py                 # every folder in state.json
    python3 folder_scan.py <folder_id> ... # specific folders

Prints one TSV row per child: folder_title <tab> file_id <tab> filename
Feed the ids to get_file_metadata for size / createdTime before deciding anything.
"""
import json, os, re, sys, urllib.request

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
HERE = os.path.dirname(os.path.abspath(__file__))


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "replace")


def children(folder_id):
    """[(file_id, filename)] for a link-shared folder. Empty list = fetch worked but
    folder is empty; an exception means the fetch itself failed — never silently pass."""
    html = fetch(f"https://drive.google.com/drive/folders/{folder_id}")
    # Each child renders as: aria-label="<name> <Type> Shared" ... data-id="<id>"
    out, seen = [], set()
    for m in re.finditer(r'aria-label="([^"]+?)"[^>]*>.{0,600}?data-id="([A-Za-z0-9_\-]{20,50})"',
                         html, re.S):
        name, fid = m.group(1), m.group(2)
        if fid == folder_id or fid in seen:
            continue
        name = re.sub(r"\s+(Video|Audio|Image|PDF|Binary|Text|File|Folder)?\s*Shared$", "", name).strip()
        seen.add(fid)
        out.append((fid, name))
    if not out and "data-id=" not in html:
        raise RuntimeError(f"folder {folder_id}: no listing in HTML "
                           f"({len(html)} bytes) — not link-shared, or Drive changed its markup")
    return out


def folders_from_state():
    st = json.load(open(os.path.join(HERE, "state.json"), encoding="utf-8"))
    for name, e in st.get("editors", {}).items():
        for f in e.get("shared_folders", []):
            yield name, f["id"], f.get("title", f["id"])


def main():
    args = sys.argv[1:]
    targets = ([("(arg)", fid, fid) for fid in args] if args else list(folders_from_state()))
    if not targets:
        print("no shared_folders in state.json and no ids given", file=sys.stderr)
        return 2
    rc = 0
    for editor, fid, title in targets:
        try:
            kids = children(fid)
        except Exception as exc:                      # loud, never a silent empty
            print(f"!! {editor} / {title}: {exc}", file=sys.stderr)
            rc = 1
            continue
        for cid, cname in kids:
            print(f"{editor}\t{title}\t{cid}\t{cname}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
