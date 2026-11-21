#!/bin/zsh
# Timing shim for the Abs By AI video pipeline.
#
# Installed at Media/video_edit/bin/ffmpeg (and ffprobe); the real binaries are
# moved aside to *.real. Every call site in every skill resolves to those paths
# (directly or through /Volumes/Extreme/_edit_work/bin symlinks), so this
# catches 100% of invocations.
#
# HARD REQUIREMENTS (each one is a way this can silently break the pipeline):
#   1. Never write to stdout or stderr. The two-pass loudnorm chain in
#      finish_audio.py does  json.loads(stderr[stderr.rindex('{'):...])  on
#      ffmpeg's stderr; one extra character there breaks the audio chain and it
#      presents as an audio defect, not an instrumentation bug. All timing goes
#      to a separate log file, and every write to it is redirected to /dev/null
#      on failure.
#   2. stdin/stdout/stderr are inherited untouched by the real binary. No pipe,
#      no tee, no buffering, no filtering.
#   3. The exit code is propagated exactly (scripts use check=True).
#   4. "$@" everywhere, never $* -- every path here contains spaces.
#
# Note: this does NOT exec the real binary, because the duration has to be read
# after it returns. It runs as a direct child with inherited fds, which is
# stdio-identical to exec; the only difference is one extra process in the tree,
# which nothing in this pipeline inspects.

emulate -L zsh
zmodload zsh/datetime 2>/dev/null

_REAL="${0:A:h}/${0:t}.real"
[[ -x $_REAL ]] || _REAL="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/${0:t}.real"

_LOG="${ABSBYAI_TIMING_LOG:-/Volumes/Extreme/_edit_work/_timing/ffmpeg_calls.log}"

_t0=$EPOCHREALTIME
"$_REAL" "$@"
_rc=$?
_t1=$EPOCHREALTIME

# ---- everything below is logging only; it must never affect the caller ----
{
  # Summarise the invocation cheaply: output file, video codec, preset, crf.
  _out=- ; _vc=- ; _pre=- ; _crf=- ; _filt=-
  _prev=
  for _a in "$@"; do
    case $_prev in
      -c:v|-vcodec) _vc=$_a ;;
      -preset)      _pre=$_a ;;
      -crf)         _crf=$_a ;;
      -filter_complex|-vf|-lavfi) _filt=complex ;;
    esac
    _prev=$_a
  done
  # last non-flag argument is conventionally the output
  _last=${@[-1]}
  [[ -n $_last && $_last != -* ]] && _out=${_last:t}

  printf '%s\t%.3f\t%d\t%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$_t0" "$((_t1 - _t0))" "$_rc" "${0:t}" "$_out" "$_vc" "$_pre" "$_crf" "$_filt" \
    >> "$_LOG"
} 2>/dev/null

exit $_rc
