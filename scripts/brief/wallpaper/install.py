#!/usr/bin/env python3
"""Run only after approval for Keychain enrollment and the persistent reader grant."""
import argparse,json,os,pathlib,plistlib,shutil,subprocess,time
p=argparse.ArgumentParser();p.add_argument('action',choices=['install','start','stop','restore']);args=p.parse_args()
root=pathlib.Path.home()/'Library/Application Support/AbsByAIWallpaper'
bin_dir=root/'bin'
agent=pathlib.Path.home()/'Library/LaunchAgents/com.absbyai.wallpaper-reader.plist'
label='gui/'+str(os.getuid())+'/com.absbyai.wallpaper-reader'
def stop():
 root.mkdir(parents=True,exist_ok=True,mode=0o700)
 # This sentinel also stops an explicit reader invocation from rotating offline.
 (root/'disabled').touch(mode=0o600)
 subprocess.run(['launchctl','disable',label],check=True)
 bootout=subprocess.run(['launchctl','bootout',label],capture_output=True,text=True)
 check=subprocess.run(['launchctl','print',label],capture_output=True,text=True)
 if check.returncode==0 or 'could not find service' not in (check.stderr+check.stdout).lower():
  raise SystemExit('Could not verify reader unload: '+bootout.stderr.strip())
 if agent.exists():agent.rename(agent.with_suffix('.plist.disabled'))
 # Check exact paths belonging to this feature, never stop unrelated processes.
 for attempt in range(25):
  listing=subprocess.check_output(['ps','-ww','-axo','pid=,uid=,command='],text=True)
  active=[]
  for line in listing.splitlines():
   fields=line.strip().split(None,2)
   if len(fields)!=3 or fields[1]!=str(os.getuid()):continue
   command=fields[2]
   if command.startswith(str(bin_dir/'mac-helper')+' ') or command.endswith(' '+str(bin_dir/'reader.js')):active.append(fields[0])
  if not active:break
  time.sleep(1)
 else:raise SystemExit('Reader remains running after unload; PIDs '+','.join(active)+'. No success claimed.')
 print('Verified: reader unloaded, future launches disabled, no reader/helper running. Offline rotation stopped. Server grant must be revoked separately.')
if args.action in ['stop','restore']:
 stop()
 if args.action=='restore':
  before=json.loads((root/'wallpapers-before.json').read_text())
  observed=json.loads(subprocess.check_output([str(bin_dir/'mac-helper'),'--inspect']))
  plan=[]
  for old in before:
   match=next((d for d in observed if d.get('uuid')==old.get('uuid') and old.get('uuid')),None)
   if not match:raise SystemExit('Prior display unavailable; no automatic restore. Keep the private backup and use System Settings.')
   if not old.get('path') or not pathlib.Path(old['path']).is_file():raise SystemExit('A prior image is unavailable; restore remains incomplete.')
   plan.append({'id':match['id'],'path':old['path']})
  subprocess.run([str(bin_dir/'mac-helper'),'--apply'],input=json.dumps(plan),text=True,check=True)
  print('Prior image paths restored and read back. Prior Photos shuffle and Space-specific timing must be reselected in System Settings; their original configuration is preserved in wallpaper-store-before.plist.')
 raise SystemExit
if args.action=='start':
 if not agent.exists() and agent.with_suffix('.plist.disabled').exists():agent.with_suffix('.plist.disabled').rename(agent)
 subprocess.run(['launchctl','enable',label],check=True)
 (root/'disabled').unlink(missing_ok=True)
 subprocess.run(['launchctl','bootstrap','gui/'+str(os.getuid()),str(agent)],check=True)
 check=subprocess.run(['launchctl','print',label],capture_output=True,text=True)
 if check.returncode:raise SystemExit('Reader load not verified')
 print('Reader loaded. Verify signed receipt, three wallpaper paths and the next real 30-minute transition.');raise SystemExit
src=pathlib.Path(__file__).resolve().parent
root.mkdir(parents=True,exist_ok=True,mode=0o700);os.chmod(root,0o700)
bin_dir.mkdir(mode=0o700,exist_ok=True)
subprocess.run(['swiftc',str(src/'mac-helper.swift'),'-o',str(bin_dir/'mac-helper')],check=True)
for name in ['reader.js','rotation.js']:shutil.copy2(src/name,bin_dir/name)
node=shutil.which('node')
if not node:raise SystemExit('Trusted Node installation missing')
# Preserve settings before any wallpaper change, without overwriting earlier undo evidence.
backup=root/'wallpapers-before.json'
if not backup.exists():
 backup.write_bytes(subprocess.check_output([str(bin_dir/'mac-helper'),'--inspect']));os.chmod(backup,0o600)
store=pathlib.Path.home()/'Library/Application Support/com.apple.wallpaper/Store/Index.plist'
config_backup=root/'wallpaper-store-before.plist'
if store.exists() and not config_backup.exists():shutil.copy2(store,config_backup);os.chmod(config_backup,0o600)
public=json.loads(subprocess.check_output([str(bin_dir/'mac-helper'),'--enroll']))['publicKey']
config={'Label':'com.absbyai.wallpaper-reader','ProgramArguments':[str(pathlib.Path(node).resolve()),str(bin_dir/'reader.js')],'StartInterval':60,'RunAtLoad':True,'ProcessType':'Background','StandardOutPath':str(root/'reader.log'),'StandardErrorPath':str(root/'reader-error.log'),'Umask':0o077}
for name in ['reader.log','reader-error.log']:
 file=root/name;file.touch(mode=0o600);os.chmod(file,0o600)
agent.parent.mkdir(exist_ok=True)
with agent.open('wb') as f:plistlib.dump(config,f)
os.chmod(agent,0o600)
print(json.dumps({'BRIEF_WALLPAPER_PUBLIC_KEY':public,'started':False}))
