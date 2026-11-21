#!/bin/bash
# SL-16: track + bars + proof for the named shorts, as ONE render-queue step
cd /Volumes/Extreme/_edit_work/SL-16
python3 batch.py track "$@" && python3 batch.py plan "$@" > logs_plan.txt && python3 batch.py gfx "$@" && python3 batch.py proof "$@"
