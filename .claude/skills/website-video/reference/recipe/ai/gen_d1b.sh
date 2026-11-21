#!/bin/zsh
cd /Volumes/Extreme/_edit_work/website-video-828/ai
node "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/gemini-image.js" generate --prompt-file prompts/D1b_still.txt --out stills/D1b.jpg --tier draft --aspect 16:9 --image stills/A.jpg --env ~/.absbyai-secrets.env || exit 1
node veo.js stills/D1b.jpg prompts/D1_video.txt clips/D1.mp4 8 16:9
