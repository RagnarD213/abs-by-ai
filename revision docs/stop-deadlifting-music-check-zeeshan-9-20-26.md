# STOP Deadlifting - music check, 2026-09-20

Zeeshan's claim: the music in the video is the track he was asked to use.

## Measurement (Rev 3, "Video2 Rev 3.mp4", 660.1 s)

Envelope cross-correlation, 20 s and 40 s windows across the whole file, against both mp3s
now sitting in his delivery folder.

- **knox-gym "Energy Gym Thunder"** IS present, but only under the live round:
  cut 520 s r=+0.918 (track 18.7 s), 540 s r=+0.955 (38.7 s), 560 s r=+0.906 (58.7 s),
  580 s r=+0.397 (78.7 s). Offsets advance exactly with the windows, so the track starts at
  about 8:21 and runs to about 9:55. Null everywhere else in the file.
- **topsecretmusicnetwork trip hop 130 BPM** (byte identical to our own
  `Media/music beds/rhythmical-melodic-syncopation-triphop-130bpm-pixabay-10091.mp3`,
  md5 0f36416eb99e087aeafd025b3c1bafec) is **NOT in the mix anywhere.** 17 consecutive 40 s
  windows read r 0.09 to 0.28 with scattered, inconsistent offsets. Tempo sweep
  (atempo 0.90 / 0.95 / 1.05 / 1.10) found nothing either.
- **Positive control, because this track's envelope is flat and r alone is weak:** the same
  trip hop file mixed into cut 20-100 s at -15, -20 and -25 dB returned the true offset
  40.0 s every time (r +0.412, +0.260, +0.155). A present track pins the offset; the real
  windows do not.
- **A bed IS running under the whole video.** Gap floor p5 -36.6 to -41.2 dB against our raw
  floor of about -53 dB, with 80-500 Hz energy in the quietest 10 percent of frames at every
  window sampled (20, 150, 300, 420, 530, 620 s).

**Verdict: a third, unnamed track runs 0:00 - 8:19 and 9:55 to the end.** The round 2 item
stands as written.

## Paste-ready message to Zeeshan

Hey Zeeshan,

Thanks for sending the music file over. I checked it again carefully, and I think there is a
simple mix up here, so let me explain it clearly.

There are TWO different music tracks in this video, not one.

The first one is "Energy Gym Thunder". That one IS in the video, and you are right about it.
It plays under the live workout round, from about 8:21 to 9:55. That is the track I asked you
to use, it is correct, and I want you to keep it exactly as it is.

The second one is the problem. From 0:00 to 8:19, and again from 9:55 to the end, there is a
DIFFERENT music track playing quietly under my voice. It is soft, but it is there the whole
time. The trip hop file you put in the folder is not that track. I tested it against the video
from start to finish and it does not match anywhere.

To make sure my test was not wrong, I did this: I took that same trip hop file and mixed it
into this video myself, very quietly, and my test found it immediately every time, even when I
made it almost silent. So the test works fine. It simply cannot find that track in your mix,
because it is not in there.

My guess is that the background music came from a template or a preset inside your editing
software, so it was added without you choosing it.

Here is what I need, and it is easy:

Send me the name of the music that plays from 0:00 to 8:19 and after 9:55, or just put that
exact file in the folder. I am not asking you to change the music. It sounds good and it sits
at a good level.

Or, if you cannot find out what it is, just replace that background music with the trip hop
file you already have in the folder, and tell me you did it. That solves it too.

The reason I need this is YouTube. If a music track is Content ID registered, YouTube can
claim or block the video, so I cannot upload it until I know exactly what every track is.

Thanks!

## CORRECTION, 2026-09-22: the verdict above was wrong

Zeeshan sent a no-music export of Video 2 (same cut, sample-aligned). Mix minus no-music = the music stem.
The stem matches the trip hop at r 0.99 from 0:00 to 8:23 and 9:54 to the end, and Knox Gym Thunder at
r 0.999 from 8:24 to 9:54. There is no third track. The envelope test missed the trip hop because his
loudened voice-over masks a -27 dB flat bed. Trap: for a quiet bed under dialogue, ask for a no-music
export and subtract; do not trust envelope correlation. Video 3 Rev 3: its "music" and "No music" files
carry identical audio, and neither Knox nor trip hop is detectable, so V3 appears to have no music.
Work files: /Volumes/Extreme/_edit_work/music-check-20260922/
