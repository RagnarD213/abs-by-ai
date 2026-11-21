# Ad 15 final: patching two spans of an editor's finished export (2026-09-21)

Recipe for changing a few seconds of an editor's finalized HD export while every other frame stays bit-identical.

- **GOP splice, not a re-encode.** Muhammad's Mainconcept exports are IDR every 30 frames, no B-frames, refs 1, SPS/PPS
  and an AUD in every access unit. `build.py` re-encodes only the 30-frame GOPs that contain a change (x264 main 4.1,
  keyint 30, bf 0, ref 1, aud, repeat-headers), splits both Annex B streams at AUDs and swaps those access units in, then
  remuxes with his AAC stream-copied. Proof: framemd5 differs only inside the re-encoded GOPs, untouched frames there
  sit at 48.6 dB PSNR or better, decoded PCM hashes identical.
- **Recovering a camera shot under an insert:** audio xcorr of his mix against the raw lav (`xc.py`, right channel on
  C1604) gives the audio offset; his picture ran one frame after it (ECC alignment on his neighbouring shot), so picture
  = ad frame + 2860.
- **Grade:** a global LUT or curves plateau at about 6.5/255 on his indoor ads; a pixel regression with multi-scale
  local-luminance terms (`ms.py`) matches visually. A per-pixel correction field fits better on paper (2.5/255) but is
  shaped like Dan, so it smears when he moves. Do not use it.
- **Transitions:** never rebuild an editor's flash from his own frames minus the old insert; the insert ghosts through.
  Screen-blend his white flash frame, blurred to light only, ramped to his measured brightness (`flashfix.py`).
- **Tag on an app screen:** lift his exact pill pixels from a frame where he used it, keep even x/y offsets so chroma
  copies cleanly, track the screen's scroll (`dy.py`), and fade it only while the picture fades up.
