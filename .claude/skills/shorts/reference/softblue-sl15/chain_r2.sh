#!/bin/bash
# SL-15 round 2: render both shorts, deliver (audio gate, 540p, transcript, gate plan) and the watch pass, as ONE queue step
cd /Volumes/Extreme/_edit_work/SL-15
python3 batch.py render "$@"
