#!/bin/sh
# after.sh "PID PID ..." clipq-args...   -- wait for those pids to exit, then run clipq.py with the args
for p in $1; do while kill -0 $p 2>/dev/null; do sleep 5; done; done
shift; exec python3 clipq.py "$@"
