"""RO-20C round 6: video 3's new intro picture (pickup P4). Frames 0..205 (to "You need", 6.874 s) are the levels-split plate
(_shared/hyperframes/levels-split, round6/graphic/plate/LS-ro20c-r6.mov, transparent holes) over the three AI clips, each laid
into its tile from the moment its hole opens; frames 206..532 are the approved round 3 P4 picture, unchanged. The voice is the
locked P4 voice (round3b hashes) and is not touched here.
usage: p4_r6.py OUT.mp4            (reads the gated take ranges below)
Colour: every input is converted to RGB with its own matrix (Veo takes BT.709; HyperFrames renders BT.601, as composite.py
decodes them), the result is encoded BT.709 tagged, libx264 crf 14, 30000/1001, exactly 533 frames like round3/pickups/P4.mp4."""
import json, os, subprocess, sys
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
R6 = "/Volumes/Extreme/_edit_work/ro20/round6"
P4 = "/Volumes/Extreme/_edit_work/ro20/round3/pickups/P4.mp4"
PLATE = f"{R6}/graphic/plate/LS-ro20c-r6.mov"
CFG = json.load(open(f"{R6}/graphic/LS-ro20c.json"))
NCARD, NP4 = 206, 533                     # "You need" lands at P4 6.87 s; P4 is 533 frames
TILE, GAP, X0, TY = 560, 40, 80, 272       # levels-split/build.py geometry
# take, first frame of the gated range (24 fps), square crop [x, y, side] in the 1920x1080 take
# per tile: shots [(take, first frame, frame count)] at 24 fps, played in order with hard cuts, and the square crop [x, y, side]
# Middle Class: four 8 s takes failed review (hair and face redrawn whenever he looked down for long), so a 4 s take from the same
# approved START/END frames (I2f) leaves the model no time to drift; frames 14 to 95 (a single shot list still allows several).
TAKES = {0: ([(f"{R6}/veo/I1-api-t1.mp4", 96, 96)], (419, 0, 1080)),
         1: ([(f"{R6}/veo/I2f-api-t1.mp4", 14, 82)], (420, 0, 1080)),
         2: ([(f"{R6}/veo/I3-api-t1.mp4", 0, 53)], (420, 0, 1080))}

if __name__ == "__main__":
    out = sys.argv[1]
    dur = NCARD * 1001 / 30000
    args = [FF, "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=black:s=1920x1080:r=30000/1001:d={dur:.4f}"]
    fg = ["[0:v]format=rgb24[b0]"]
    last = "b0"
    k = 1
    for i, tl in enumerate(CFG["tiles"]):
        shots, (cx, cy, side) = TAKES[i]
        at = tl["at"]; x = X0 + i * (TILE + GAP); parts = []
        for j, (take, f0, nf) in enumerate(shots):
            args += ["-ss", f"{f0 / 24:.4f}", "-i", take]
            fg.append(f"[{k}:v]trim=end_frame={nf},setpts=PTS-STARTPTS,scale=in_color_matrix=bt709:in_range=tv,format=rgb24,"
                      f"crop={side}:{side}:{cx}:{cy},scale={TILE}:{TILE}:flags=lanczos[s{i}_{j}]"); parts.append(f"[s{i}_{j}]"); k += 1
        cat = f"{''.join(parts)}concat=n={len(parts)}:v=1:a=0," if len(parts) > 1 else f"{parts[0]}"
        fg.append(f"{cat}{'' if len(parts) > 1 else 'null,'}fps=30000/1001,trim=duration={dur - at + 0.1:.4f},setpts=PTS-STARTPTS+{at:.4f}/TB[c{i}]")
        fg.append(f"[{last}][c{i}]overlay={x}:{TY}:eof_action=pass:enable='gte(t,{at:.4f})'[b{i + 1}]"); last = f"b{i + 1}"
    args += ["-i", PLATE, "-i", P4]
    fg.append(f"[{k}:v]scale=in_color_matrix=bt601:in_range=tv,format=rgba,trim=end_frame={NCARD},setpts=PTS-STARTPTS[pl]")
    fg.append(f"[{last}][pl]overlay=0:0:format=auto,trim=end_frame={NCARD},setpts=PTS-STARTPTS[card]")
    fg.append(f"[{k + 1}:v]scale=in_color_matrix=bt709:in_range=tv,format=rgb24,trim=start_frame={NCARD}:end_frame={NP4},setpts=PTS-STARTPTS[rest]")
    fg.append("[card][rest]concat=n=2:v=1:a=0,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p[v]")
    args += ["-filter_complex", ";".join(fg), "-map", "[v]", "-an", "-r", "30000/1001", "-c:v", "libx264", "-crf", "14", "-preset", "slow",
             "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-frames:v", str(NP4), out]
    subprocess.run(args, check=True)
    print("P4 r6 ->", out)
