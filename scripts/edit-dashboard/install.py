"""Install only the dashboard's own files, helper and LaunchAgent; existing editors stay up."""
import os,plistlib,shutil,socket,subprocess,sys
from pathlib import Path
D=Path(__file__).resolve().parent; HOME=Path.home();ROOT=HOME/'.local/share/abs-edit-dashboard';LABEL='com.absbyai.edit-desk';PORT=8976
PLIST=HOME/'Library/LaunchAgents'/(LABEL+'.plist');U='gui/'+str(os.getuid())
SSH=['ssh','-oBatchMode=yes','-oConnectTimeout=3','m2']
def run(*a,**kw):return subprocess.run(a,check=True,**kw)
def install():
    ROOT.mkdir(parents=True,exist_ok=True)
    if not PLIST.exists():
        with socket.socket() as s:s.bind(('127.0.0.1',PORT))
    for f in ('review_handoff.py','observe.py','server.py','index.html','style.css','app.js','policy.json'):shutil.copy2(D/f,ROOT/f)
    run('clang','-O2','-dynamiclib','-framework','CoreFoundation','-framework','IOKit',str(D/'kernel.c'),'-o',str(ROOT/'kernel.next'));os.replace(ROOT/'kernel.next',ROOT/'kernel.dylib')
    # No shell profile/PATH dependence. Compile against M2's own SDK at install time.
    run(*SSH,'mkdir -p "$HOME/.local/share/abs-edit-dashboard"')
    for f in ('kernel.c','policy.json','review_handoff.py','observe.py'):
        with (D/f).open('rb') as src:run(*SSH,'cd "$HOME/.local/share/abs-edit-dashboard" && cat > '+f+'.new && mv '+f+'.new '+f,stdin=src)
    run(*SSH, """set -e
cd "$HOME/.local/share/abs-edit-dashboard"
clang -O2 -dynamiclib -framework CoreFoundation -framework IOKit kernel.c -o kernel.next
mv kernel.next kernel.dylib
p=$(/usr/bin/python3 -c 'import sys;print(sys.executable)')
printf '#!/bin/sh\nexec "%s" -S -B "$HOME/.local/share/abs-edit-dashboard/observe.py" m2\n' "$p" > collect.new
chmod 755 collect.new
mv collect.new collect""")
    cfg={'Label':LABEL,'ProgramArguments':[sys.executable,'-S','-B',str(ROOT/'server.py')],'Sockets':{'Listeners':{'SockNodeName':'127.0.0.1','SockFamily':'IPv4','SockServiceName':str(PORT),'SockType':'stream'}},'ThrottleInterval':2,'StandardErrorPath':str(ROOT/'service.log')}
    if PLIST.exists():subprocess.run(['launchctl','bootout',U+'/'+LABEL],capture_output=True)
    PLIST.write_bytes(plistlib.dumps(cfg));run('launchctl','bootstrap',U,str(PLIST))
if __name__=='__main__':install()
