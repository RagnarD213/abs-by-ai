#!/bin/bash
# One-shot Seagate health check. Dan runs this once in Terminal and types his Mac password when asked.
# Installs Homebrew + smartmontools if missing, reads the drive's SMART data, starts a long self-test.
# Output goes to Docs/SEAGATE_HEALTH_RAW_20261106.txt (no passwords are written anywhere).
set -u
REPO="$HOME/Projects/Claude/Projects/Abs By AI"
OUT="$REPO/Docs/SEAGATE_HEALTH_RAW_20261106.txt"
BREW=/opt/homebrew/bin/brew
[ -x "$BREW" ] || BREW=/usr/local/bin/brew
if [ ! -x "$BREW" ]; then
  echo "Installing Homebrew (asks for your Mac password once)..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  BREW=/opt/homebrew/bin/brew; [ -x "$BREW" ] || BREW=/usr/local/bin/brew
fi
[ -x "$(dirname "$BREW")/smartctl" ] || "$BREW" install smartmontools
SMART="$(dirname "$BREW")/smartctl"
NODE=$(diskutil info /Volumes/Expansion | awk '/Part of Whole/{print $4}')
echo "Seagate whole-disk node: /dev/$NODE"
{
  echo "== diskutil =="; diskutil info /Volumes/Expansion
  echo; echo "== smartctl -a -d sat =="; sudo "$SMART" -a -d sat "/dev/$NODE"
  echo; echo "== smartctl -a (auto) =="; sudo "$SMART" -a "/dev/$NODE"
  echo; echo "== start long self-test =="; sudo "$SMART" -t long -d sat "/dev/$NODE"
} 2>&1 | tee "$OUT"
echo
echo "Done. Results saved to $OUT. Tell Claude it finished."
