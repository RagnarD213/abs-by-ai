#!/usr/bin/env python3
"""Run only after approval for Keychain enrollment and the persistent reader grant."""
import argparse,json,os,pathlib,plistlib,shutil,subprocess
p=argparse.ArgumentParser();p.add_argument('action',choices=['install','start','stop']);args=p.parse_args()
root=pathlib.Path.home()/'Library/Application Support/AbsByAIWallpaper'
agent=pathlib.Path.home()/'Library/LaunchAgents/com.absbyai.wallpaper-reader.plist'
label='gui/'+str(os.getuid())+'/com.absbyai.wallpaper-reader'
if args.action=='stop':
 subprocess.run(['launchctl','bootout',label],check=False)
 print('Reader stopped. Revoke BRIEF_WALLPAPER_PUBLIC_KEY on Railway separately. Originals retained.');raise SystemExit
if args.action=='start':
 subprocess.run(['launchctl','bootstrap','gui/'+str(os.getuid()),str(agent)],check=True)
 print('Reader started. Verify signed receipt and all three Mac wallpaper paths.');raise SystemExit
src=pathlib.Path(__file__).resolve().parent
root.mkdir(parents=True,exist_ok=True,mode=0o700);os.chmod(root,0o700)
bin_dir=root/'bin';bin_dir.mkdir(mode=0o700,exist_ok=True)
subprocess.run(['swiftc',str(src/'mac-helper.swift'),'-o',str(bin_dir/'mac-helper')],check=True)
for name in ['reader.js','rotation.js']:shutil.copy2(src/name,bin_dir/name)
node=shutil.which('node')
if not node:raise SystemExit('Trusted Node installation missing')
# Preserve the existing settings and paths before any wallpaper change.
backup=root/'wallpapers-before.json'
if not backup.exists():
 backup.write_bytes(subprocess.check_output([str(bin_dir/'mac-helper'),'--inspect']));os.chmod(backup,0o600)
public=json.loads(subprocess.check_output([str(bin_dir/'mac-helper'),'--enroll']))['publicKey']
config={'Label':'com.absbyai.wallpaper-reader','ProgramArguments':[str(pathlib.Path(node).resolve()),str(bin_dir/'reader.js')],'StartInterval':60,'RunAtLoad':True,'ProcessType':'Background','StandardOutPath':str(root/'reader.log'),'StandardErrorPath':str(root/'reader-error.log'),'Umask':0o077}
for name in ['reader.log','reader-error.log']:
 file=root/name;file.touch(mode=0o600);os.chmod(file,0o600)
agent.parent.mkdir(exist_ok=True)
with agent.open('wb') as f:plistlib.dump(config,f)
os.chmod(agent,0o600)
print(json.dumps({'BRIEF_WALLPAPER_PUBLIC_KEY':public,'started':False}))
