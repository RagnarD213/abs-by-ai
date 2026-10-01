# Split a long page into canvas boards (a Design canvas board is capped at 8000 px tall).
# Usage: python3 split_boards.py <config.json>
# config: {"heights": {"phone": "m/h_phone.json", "desk": "m/h_desk.json"},
#          "breaks": ["revolution", "fiveways", "hack5"],          # first section key of parts 2..n
#          "files":  {"phone": ["P-1.dc.html", ...], "desk": [...]},
#          "titles": {"phone": ["Phone 1 of 4 · ...", ...], "desk": [...]},
#          "out": {"phone": "split_phone.json", "desk": "split_desk.json"}}
# Each part's board height = content x 1.025 + 40, rounded up to 20 px. The last section of every part
# gets flex-grow in the board, so the spare height extends that section's background instead of clipping.
import json, math, sys

cfg = json.load(open(sys.argv[1]))
for dev, path in cfg['heights'].items():
    rows = json.load(open(path))
    parts, cur = [], []
    for key, h in rows:
        if key in cfg['breaks'] and cur:
            parts.append(cur); cur = []
        cur.append((key, h))
    parts.append(cur)
    assert len(parts) == len(cfg['files'][dev]), f'{dev}: {len(parts)} parts but {len(cfg["files"][dev])} file names'
    out = {'parts': []}
    for n, pt in enumerate(parts):
        tot = sum(h for _, h in pt)
        H = int(math.ceil((tot * 1.025 + 40) / 20) * 20)
        if H > 8000:
            sys.exit(f'{dev} part {n + 1} is {H} px: move a break earlier or add a part')
        out['parts'].append({'file': cfg['files'][dev][n], 'title': cfg['titles'][dev][n],
                             'keys': [k for k, _ in pt], 'h': H, 'content': tot})
        print(f'{dev} {n + 1}: {tot} px content, board {H} px, {pt[0][0]} to {pt[-1][0]}')
    json.dump(out, open(cfg['out'][dev], 'w'), indent=1)
