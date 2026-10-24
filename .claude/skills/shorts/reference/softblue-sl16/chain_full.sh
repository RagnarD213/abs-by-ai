#!/bin/bash
# SL-16: plan (shot table from plans.py: covers, grades, crops), track, bars, render, deliver and watch, as ONE render-queue step
# (plan was missing until 2026-10-24: a plans.py grade change never reached the render, review r1c)
cd /Volumes/Extreme/_edit_work/SL-16
python3 batch.py plan "$@" > logs_plan_chain.txt && python3 batch.py track "$@" && python3 batch.py gfx "$@" && python3 batch.py render "$@"
