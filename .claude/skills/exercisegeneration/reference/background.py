#!/usr/bin/env python3
"""Check every exposed empty-gym pixel for temporal change, with per-frame foreground masks.

Masks are white ONLY on the person, held props and genuinely driven apparatus. They must be
independently reviewed; a whole equipment cabinet must not be hidden for an entire clip because
a bar crosses it briefly. The mask sequence repeats for a narrated loop. No audio is played.
"""
import argparse
import hashlib
import json
from pathlib import Path

import cv2
import numpy as np


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('video', type=Path)
    p.add_argument('--plate', required=True, type=Path)
    p.add_argument('--masks', required=True, type=Path)
    p.add_argument('--report', required=True, type=Path)
    a = p.parse_args()
    plate = cv2.imread(str(a.plate))
    paths = sorted(a.masks.glob('*.png'))
    if plate is None or not paths:
        p.error('A readable clean plate and per-frame masks are required')
    mask_hash = hashlib.sha256()
    masks = []
    for path in paths:
        mask = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
        if mask is None or mask.shape != plate.shape[:2]:
            p.error(f'Mask size mismatch: {path}')
        mask_hash.update(path.name.encode() + bytes.fromhex(sha(path)))
        # Four pixels cover matte feather and video compression at moving silhouettes.
        masks.append(cv2.dilate(mask, np.ones((9, 9), np.uint8)) > 0)
    cap = cv2.VideoCapture(str(a.video))
    if not cap.isOpened():
        p.error('Video could not be decoded')
    frame = 0
    failures = []
    worst = {'largest_changed_region_px': 0, 'changed_fraction': 0}
    min_exposed_fraction = 1.0
    evidence = None
    first_exposed = plate.copy()
    seen = np.zeros(plate.shape[:2], dtype=bool)
    while True:
        ok, picture = cap.read()
        if not ok:
            break
        if picture.shape != plate.shape:
            p.error('Plate and video must have identical native dimensions')
        exposed = ~masks[frame % len(masks)]
        fraction = float(exposed.mean())
        min_exposed_fraction = min(min_exposed_fraction, fraction)
        # Compare each pixel to its first genuinely unoccluded observation, not to
        # a bar that happened to cover that background pixel in frame zero.
        newly_seen = exposed & ~seen
        first_exposed[newly_seen] = picture[newly_seen]
        seen |= exposed
        delta = np.max(np.abs(picture.astype(np.int16) - first_exposed.astype(np.int16)), axis=2)
        changed = ((delta > 20) & exposed).astype(np.uint8)
        n, _, stats, _ = cv2.connectedComponentsWithStats(changed, connectivity=8)
        regions = stats[1:] if n > 1 else np.empty((0, 5), dtype=int)
        biggest = int(regions[:, cv2.CC_STAT_AREA].max()) if len(regions) else 0
        ratio = float(changed.sum() / max(1, exposed.sum()))
        row = {'frame': frame, 'largest_changed_region_px': biggest, 'changed_fraction': ratio}
        if biggest > worst['largest_changed_region_px']:
            worst = row
            evidence = picture.copy()
            for x, y, w, h, area in regions:
                if area >= 64:
                    cv2.rectangle(evidence, (int(x), int(y)), (int(x+w), int(y+h)), (0, 0, 255), 3)
        if biggest >= 64 or ratio > 0.001 or fraction < 0.50:
            failures.append(row)
        frame += 1
    cap.release()
    complete = frame > 0 and frame % len(masks) == 0
    report = {
        'version': 1, 'video': str(a.video.resolve()), 'video_sha256': sha(a.video),
        'plate': str(a.plate.resolve()), 'plate_sha256': sha(a.plate),
        'masks': str(a.masks.resolve()), 'mask_sequence_sha256': mask_hash.hexdigest(),
        'frames_checked': frame, 'mask_frames': len(masks), 'complete_mask_cycles': complete,
        'minimum_background_exposed_fraction': min_exposed_fraction,
        'background_reference': 'first unoccluded observation of each pixel; supplied plate is visual evidence',
        'limits': {'channel_difference': 20, 'largest_changed_region_px': 63,
                   'changed_fraction': 0.001, 'minimum_background_exposed_fraction': 0.50},
        'worst': worst, 'failed_frames': failures,
        'verdict': 'PASS' if complete and not failures else 'FAIL',
        'limitation': 'Masks require independent review. Occluded background cannot be measured until uncovered.'
    }
    a.report.parent.mkdir(parents=True, exist_ok=True)
    if evidence is not None:
        ev = a.report.with_suffix('.evidence.jpg')
        cv2.imwrite(str(ev), evidence)
        report['evidence'] = str(ev)
    a.report.write_text(json.dumps(report, indent=2) + '\n')
    print(f"EMPTY BACKGROUND {report['verdict']}: {frame} frames, "
          f"{len(failures)} failed; worst region {worst['largest_changed_region_px']} px")
    return 0 if report['verdict'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
