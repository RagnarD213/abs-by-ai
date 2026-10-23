#!/bin/bash
# SL-15: track, bars, render, deliver and watch for the named shorts, as ONE render-queue step
cd /Volumes/Extreme/_edit_work/SL-15
python3 batch.py track "$@" && python3 batch.py gfx "$@" && python3 batch.py render "$@"
