#!/bin/bash
# Proof of the frame gate on the RA-04 leg press pairs Dan and seven reviews judged on 2026-10-14.
# Must FAIL: F4c_a/F5c_b, F4d_b/F5e_b, F4h/F5h2, F4h/F5j, F4h/F5m.  Must PASS: F4h/F5p.
F=/Volumes/Extreme/_edit_work/ra04/round2/frames
G="$(cd "$(dirname "$0")/../.." && pwd)/gate.py"; P="$(cd "$(dirname "$0")" && pwd)"; O=${1:-/Volumes/Extreme/_edit_work/ra04/round2/framecheck_proof}
mkdir -p "$O"
run() { python3 "$G" "$F/$1.png" "$F/$2.png" --spec "$P/$3" --out "$O" --no-stamp --json "$O/$2.json" 2>/dev/null | grep -v '^I0000\|^W0000\|^INFO'
        echo "== $1 -> $2: expected $4"; echo; }
run F4c_a F5c_b spec_AI1-3_F4c_a.json FAIL
run F4d_b F5e_b spec_AI1-3_F4d_b.json FAIL
run F4h F5h2 spec_AI1-3_F4h.json FAIL
run F4h F5j  spec_AI1-3_F4h.json FAIL
run F4h F5m  spec_AI1-3_F4h.json FAIL
run F4h F5p  spec_AI1-3_F4h.json PASS
