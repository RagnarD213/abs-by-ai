# Muhammad HD exports — exact-match check

Checked 2026-09-16 against the review exports on record from Muhammad. Per Dan's direction, this is only a content-identity check. It does not reopen accepted flaws or require items from old revision lists.

## Result

| Ad | Finalized reference used | HD delivery | Exact higher-resolution copy? |
|---|---|---|---|
| 8 | `ad8_v3.mp4` | `Daniel HQ Ad 8 V4 HD.mp4` | **No** — same 6,320-frame timeline and equivalent audio, but the picture contains multiple edits. |
| 9 | `ad9_v3.mp4` | `Daniel HQ Ad 9 v3 HD.mp4` | **No** — same 5,803-frame timeline and equivalent audio, but the picture changes materially at about 0:12–0:18 and 1:56.8–1:58.6. |
| 13 | `ad13_v3.mp4` | `Daniel HQ Ad 13 V4 HD.mp4` | **No** — same 7,339-frame timeline and equivalent audio, but the picture contains multiple edits. |
| 14 | `ad14_v3.mp4` | `Daniel HQ Ad 14 V3 HD.mp4` | **Yes** — same 5,924 frames and duration, equivalent audio, and no sampled picture change beyond re-encode noise. |
| 15 | `ad15_v2.mp4` | `Daniel HQ Ad 15 V3 HD.mp4` | **No** — same 6,205-frame timeline and equivalent audio, but the picture contains multiple edits. |

## Interpretation

Ad 14 is the only file proved to be the same finalized cut at higher quality. Ads 8, 9, 13 and 15 are not resolution-only exports of the accepted references: their audio and complete timelines were preserved, but their visuals were edited. This finding does **not** say those edits are bad or that abandoned revision requests should be restored. It says only that the four HD files are not identical to the finalized review exports used for comparison.

Because exact identity was the upload condition, Ads 8, 9, 13 and 15 were not uploaded or added to Google Ads. Their HD files can still be used if Dan explicitly designates those changed HD versions as the new approved masters.

Ad 14 passed and was installed: [YouTube `SGJoPjnl6AU`](https://youtu.be/SGJoPjnl6AU), Unlisted and fully processed. New Google Ads `824922224568` (`/start`) and `824922224571` (homepage) are enabled and under review; the two ads using the superseded low-bitrate upload are paused.

## Evidence

- HD files and machine-readable comparisons: `/Volumes/Extreme/_edit_work/ad-setup-20260916-hd/`
- Finalized review references: `/Volumes/Extreme/_edit_work/revisions-0915m/dl/`
- Comparator: `.claude/skills/ad-setup/scripts/compare_hd_export.py`
