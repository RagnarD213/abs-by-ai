#!/bin/zsh
cd /Volumes/Extreme/_edit_work/sl09/round2
python3 batch.py plan J > logs_plan_J.txt 2>&1 && python3 batch.py cues J >> logs_plan_J.txt 2>&1 && python3 chipplace.py J > sl09_r4/look/chip_J.txt 2>&1
echo "done $?" >> sl09_r4/look/chip_J.txt
