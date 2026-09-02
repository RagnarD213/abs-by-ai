#!/bin/zsh
# usage: run_bg.sh <logname> <cmd...>   -- runs cmd, prints DONE/FAILED with code, times it
LOG=$1; shift
cd /Volumes/Extreme/_edit_work/website-video-828
START=$(date +%s)
"$@" > logs/$LOG.log 2>&1
RC=$?
echo "EXIT $RC after $(( $(date +%s)-START ))s" >> logs/$LOG.log
if [ $RC -eq 0 ]; then echo "RENDER COMPLETE ($LOG)" >> logs/$LOG.log; else echo "RENDER FAILED code $RC ($LOG)" >> logs/$LOG.log; fi
