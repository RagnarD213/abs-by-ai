# The container-vs-sample timeline trap (found 2026-08-28, supplements Shorts)

**A master built by concatenating AAC segments can carry MORE audio samples than its
container declares, distributed through the file — so `-ss T` and "sample T x rate" point at
different audio, and the gap between them GROWS through the video.**

## What it did

`CUT_v1_graded_NO-GRAPHICS.mp4` is 62 concatenated ranges. Its container declares
`duration_ts 67657104` = 1409.523 s, but its AAC stream holds 66108 frames x 1024 =
67,694,592 samples = 1410.30 s. Decoding to WAV yields all of them; seeking by timestamp
honours the container. The two timelines diverge at roughly **0.5 ms per second**.

| source time | WAV-vs-`-ss` lag |
|---|---|
| 60 s | −35 ms |
| 283 s | −130 ms |
| 420 s | −222 ms |
| 997 s | −559 ms |
| 1245 s | −669 ms |

The whole shorts pipeline analyses a decoded WAV (Whisper word timestamps, `vad.py`,
`silencedetect`) and then cuts with `-ss` on the MP4. So:

* **Captions ran 280–650 ms late**, worse the later the short sat in the source.
* **First words were clipped.** Short E was supposed to open on "So this is the biggest
  mistake"; the delivered audio opened on "This is the biggest mistake" — the in-point was
  asserted to be in measured silence, but that silence was on the *other* timeline.

## Why nothing caught it

Every gate passed. `qc.js` was 12/12 green, the splice-discontinuity test passed, loudness
and duration were on spec, and the crop/centring audit was clean. **No check compared the
delivered audio against the delivered captions.** It was found by transcribing a finished
short and diffing its word times against its own `.ass`.

## The fix

Extract analysis audio on the CONTAINER timeline:

```
ffmpeg -i SRC -vn -af "aresample=async=1:first_pts=0" -ac 1 -ar 48000 -c:a pcm_s16le out.wav
```

That WAV measures 1409.526 s against the container's 1409.523 s, and the lag against `-ss`
collapses to a constant **−20 to −42 ms** — inside one AAC frame (21.3 ms), i.e. seek
granularity, not drift.

## The check that must run from now on

`work/checksync.py`: transcribe the DELIVERED short, match each caption's first word to the
heard audio, report the median offset. It is the only test that measures what a viewer
experiences. Anything beyond ~±120 ms is a defect.

## When to suspect it

Any source that was itself assembled by concatenation — which is every master this project
renders. Cheap detector: compare `(wav bytes / 2 / rate)` against the container duration. A
difference of more than a few ms means the timelines disagree.
