#!/bin/zsh
# stage.zsh <stage-name> <command...>
#
# Times one pipeline stage and appends a record to stage_times.log. Correlate
# with ffmpeg_calls.log by timestamp window to split each stage into
# "inside ffmpeg" vs "single-threaded Python (PIL / numpy / Whisper)".
#
# Deliberately does NOT use /usr/bin/time: that writes to stderr, and several
# stages in this pipeline have their stderr parsed. Timing comes from zsh's
# EPOCHREALTIME instead, so the child's stdio is inherited completely untouched.

emulate -L zsh
zmodload zsh/datetime

_DIR="${ABSBYAI_TIMING_DIR:-/Volumes/Extreme/_edit_work/_timing}"
_name=$1; shift

_t0=$EPOCHREALTIME
"$@"
_rc=$?
_t1=$EPOCHREALTIME

printf '%s\t%s\t%.3f\t%d\n' "$_t0" "$_name" "$((_t1 - _t0))" "$_rc" >> "$_DIR/stage_times.log"
exit $_rc
