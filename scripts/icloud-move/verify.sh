#!/bin/zsh
# Post-move checks for the iCloud move (handoff 2026-10-21, step 5).
D="$HOME/Documents/Claude/Projects/Abs By AI"
C="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Documents/Claude"
echo "~/Documents/Claude -> $(readlink ~/Documents/Claude)"
echo "container Claude   -> $(readlink "$C")"
echo "real folder: $(readlink -f "$D")"
echo "entries at old path: $(ls -1A "$D" | wc -l | tr -d ' ')"
echo "entries at container path: $(ls -1A "$C/Projects/Abs By AI" | wc -l | tr -d ' ')"
echo "symlinks left inside ~/Projects/Claude pointing into iCloud: $(find ~/Projects/Claude -type l -lname '*Mobile Documents*' 2>/dev/null | wc -l | tr -d ' ')"
echo "anything under the project resolving into Mobile Documents: $(find ~/Projects/Claude -maxdepth 3 -print0 2>/dev/null | xargs -0 readlink -f 2>/dev/null | grep -c 'Mobile Documents')"
echo "cloud-only items: $(find ~/Projects/Claude -flags +dataless 2>/dev/null | wc -l | tr -d ' ')"
echo "file-provider tags on the new folder: $(xattr ~/Projects/Claude 2>/dev/null | grep -c -i fileprovider)"
cd "$D" && echo "git: $(git status -sb | head -1)" && git rev-parse --short HEAD && git worktree list | wc -l | xargs echo "worktrees listed:"
python3 "$D/.claude/skills/_shared/renderq/renderq.py" status 2>&1 | head -3
echo "fileproviderd CPU: $(ps -o %cpu= -p $(pgrep -x fileproviderd)) bird CPU: $(ps -o %cpu= -p $(pgrep -x bird))"
