from pathlib import Path
import subprocess,json,hashlib
P=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');S=Path('/Volumes/Extreme/_edit_work/RO-30/setup');D=P/'Codex Content Videos/Love Handles - RO-30';RC=str(Path.home()/'bin/rclone');remote='gdrive:Codex Content Videos/Love Handles - RO-30'
for name in ['Love Handles | codex | 16x9 | RO-30.mp4','Love Handles | codex | 16x9 | RO-30.srt']:
 subprocess.run([RC,'copyto',str(D/name),remote+'/'+name],check=True)
link=subprocess.check_output([RC,'link',remote],text=True).strip();md5=subprocess.check_output([RC,'md5sum',remote],text=True);size=subprocess.check_output([RC,'lsl',remote],text=True)
(S/'backup-receipt.json').write_text(json.dumps(dict(status='complete',drive_folder=link,remote=remote,remote_md5=md5,remote_sizes=size,project=str(D),extreme='/Volumes/Extreme/Codex Content Videos/Love Handles - RO-30'),indent=2)+'\n');print(link,md5,size,flush=True)
