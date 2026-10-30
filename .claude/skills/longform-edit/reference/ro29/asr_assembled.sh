cd /Volumes/Expansion/_edit_work/RO-29/round1
export PATH="/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
python3 whisper_words.py assembled16k.wav medium.en asr_assembled_medium.json && python3 recipe/words_out.py
