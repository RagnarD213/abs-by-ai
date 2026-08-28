#!/bin/zsh
# Build a scratch copy of the Ad 1 vertical build for a COLD, clean-machine timing run.
# Never writes into the real build dir. Excludes analysis/QC output dirs (ref_audit,
# watch, contact sheets) but keeps ref_audit/his.wav, which build_audio/finish_audio
# fit the voice against. Then removes every generated artifact so the build is COLD.
set -e
SRC=/Volumes/Extreme/_edit_work/ad1-8-14/vert9x16
DST=/Volumes/Extreme/_edit_work/_timing/build

rm -rf "$DST"; mkdir -p "$DST"

rsync -a \
  --exclude 'ref_audit/***' --exclude 'watch/***' --exclude 'review_ab/***' \
  --exclude '_probe/***' --exclude '_ab/***' --exclude '_ab2/***' --exclude '_chk/***' \
  --exclude '_cast*/***' --exclude '_pick*/***' --exclude '_captest/***' --exclude '_dbg/***' \
  --exclude '_fullres/***' --exclude '_style/***' --exclude '_rev/***' --exclude '_t2/***' \
  --exclude '_fin/***' --exclude '_open_*/***' --exclude '_cut/***' --exclude 'logs/***' \
  "$SRC/" "$DST/"

mkdir -p "$DST/ref_audit"
cp "$SRC/ref_audit/his.wav" "$DST/ref_audit/his.wav"
mkdir -p "$DST/logs"

# --- make it COLD: drop everything the build regenerates ---
cd "$DST"
rm -rf seg out gfx cap cut _cx   # _flash/final is an INPUT (his fitted flash frames), never delete it
rm -f base.mp4 picture.mp4 picture_raw.mp4 captions.mov audio.wav audio_final.wav \
      voice_raw.wav sfx.wav ad1_vertical_9x16.mp4 ad1_vertical_59s.mp4 \
      REVIEW_540p_vertical_master.mp4 REVIEW_540p_vertical_59s.mp4 \
      AB_music_his-bed-vs-ours.mp4 *.mov 2>/dev/null || true

echo "scratch build ready: $DST"
du -sh "$DST"
