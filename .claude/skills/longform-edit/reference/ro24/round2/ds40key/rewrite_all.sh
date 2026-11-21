#!/bin/bash
set -uo pipefail
cd /Volumes/Expansion/_edit_work/RO-24/round2/recipe/ds40key
mkdir -p /Volumes/Expansion/_edit_work/RO-24/round2/key/v2
(
python3 /Volumes/Expansion/_edit_work/RO-24/round2/recipe/ds40key/write16.py /Volumes/Expansion/_edit_work/RO-24/round2/key/R12/c15 26770 /Volumes/Expansion/_edit_work/RO-24/round2/key/v2/R12.mkv 256 | tail -1
python3 /Volumes/Expansion/_edit_work/RO-24/round2/recipe/ds40key/write16.py /Volumes/Expansion/_edit_work/RO-24/round2/key/R04a/c15 17942 /Volumes/Expansion/_edit_work/RO-24/round2/key/v2/R04a.mkv 752 | tail -1
python3 /Volumes/Expansion/_edit_work/RO-24/round2/recipe/ds40key/write16.py /Volumes/Expansion/_edit_work/RO-24/round2/key/R02/c15 17081 /Volumes/Expansion/_edit_work/RO-24/round2/key/v2/R02.mkv 864 | tail -1
python3 /Volumes/Expansion/_edit_work/RO-24/round2/recipe/ds40key/write16.py /Volumes/Expansion/_edit_work/RO-24/round2/key/R13/c15 29983 /Volumes/Expansion/_edit_work/RO-24/round2/key/v2/R13.mkv 960 | tail -1
python3 /Volumes/Expansion/_edit_work/RO-24/round2/recipe/ds40key/write16.py /Volumes/Expansion/_edit_work/RO-24/round2/key/R03/c15 17635 /Volumes/Expansion/_edit_work/RO-24/round2/key/v2/R03.mkv 752 | tail -1
) &
(
python3 /Volumes/Expansion/_edit_work/RO-24/round2/recipe/ds40key/write16.py /Volumes/Expansion/_edit_work/RO-24/round2/key/R05/c15 20116 /Volumes/Expansion/_edit_work/RO-24/round2/key/v2/R05.mkv 832 | tail -1
python3 /Volumes/Expansion/_edit_work/RO-24/round2/recipe/ds40key/write16.py /Volumes/Expansion/_edit_work/RO-24/round2/key/R07/c15 24324 /Volumes/Expansion/_edit_work/RO-24/round2/key/v2/R07.mkv 880 | tail -1
python3 /Volumes/Expansion/_edit_work/RO-24/round2/recipe/ds40key/write16.py /Volumes/Expansion/_edit_work/RO-24/round2/key/R09/c15 25421 /Volumes/Expansion/_edit_work/RO-24/round2/key/v2/R09.mkv 864 | tail -1
python3 /Volumes/Expansion/_edit_work/RO-24/round2/recipe/ds40key/write16.py /Volumes/Expansion/_edit_work/RO-24/round2/key/R11/c15 26452 /Volumes/Expansion/_edit_work/RO-24/round2/key/v2/R11.mkv 800 | tail -1
python3 /Volumes/Expansion/_edit_work/RO-24/round2/recipe/ds40key/write16.py /Volumes/Expansion/_edit_work/RO-24/round2/key/R15/c15 30747 /Volumes/Expansion/_edit_work/RO-24/round2/key/v2/R15.mkv 912 | tail -1
) &
(
python3 /Volumes/Expansion/_edit_work/RO-24/round2/recipe/ds40key/write16.py /Volumes/Expansion/_edit_work/RO-24/round2/key/R04b/c15 18610 /Volumes/Expansion/_edit_work/RO-24/round2/key/v2/R04b.mkv 752 | tail -1
python3 /Volumes/Expansion/_edit_work/RO-24/round2/recipe/ds40key/write16.py /Volumes/Expansion/_edit_work/RO-24/round2/key/R06/c15 22954 /Volumes/Expansion/_edit_work/RO-24/round2/key/v2/R06.mkv 576 | tail -1
python3 /Volumes/Expansion/_edit_work/RO-24/round2/recipe/ds40key/write16.py /Volumes/Expansion/_edit_work/RO-24/round2/key/R01/c15 16084 /Volumes/Expansion/_edit_work/RO-24/round2/key/v2/R01.mkv 896 | tail -1
python3 /Volumes/Expansion/_edit_work/RO-24/round2/recipe/ds40key/write16.py /Volumes/Expansion/_edit_work/RO-24/round2/key/R16/c15 31535 /Volumes/Expansion/_edit_work/RO-24/round2/key/v2/R16.mkv 560 | tail -1
python3 /Volumes/Expansion/_edit_work/RO-24/round2/recipe/ds40key/write16.py /Volumes/Expansion/_edit_work/RO-24/round2/key/R14/c15 30325 /Volumes/Expansion/_edit_work/RO-24/round2/key/v2/R14.mkv 912 | tail -1
python3 /Volumes/Expansion/_edit_work/RO-24/round2/recipe/ds40key/write16.py /Volumes/Expansion/_edit_work/RO-24/round2/key/R10/c15 26110 /Volumes/Expansion/_edit_work/RO-24/round2/key/v2/R10.mkv 912 | tail -1
) &
wait
echo "REWRITE DONE"
