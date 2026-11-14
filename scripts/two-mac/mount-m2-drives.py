#!/usr/bin/python3
"""Reconnect the two M2 SMB shares using macOS NetFS and saved Keychain login.

Runs silently when the cable is absent or the expected shares are mounted.
No credentials are stored here and authentication dialogs are suppressed.
"""
import ctypes as c
import os
from pathlib import Path
import socket
import subprocess
import sys

HOST = "10.66.0.2"
USER = "danielrose"
SHARES = ("Extreme", "Expansion")


def mount_lines():
    return subprocess.check_output(["/sbin/mount", "-t", "smbfs"], text=True).splitlines()


def correct_mount(share, lines):
    return any(line.startswith(f"//{USER}@{HOST}/{share} on /Volumes/{share} (") for line in lines)


def mount_share(share):
    cf = c.CDLL("/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation")
    nf = c.CDLL("/System/Library/Frameworks/NetFS.framework/NetFS")
    ptr = c.c_void_p
    cf.CFStringCreateWithCString.argtypes = [ptr, c.c_char_p, c.c_uint32]
    cf.CFStringCreateWithCString.restype = ptr
    cf.CFURLCreateWithString.argtypes = [ptr, ptr, ptr]
    cf.CFURLCreateWithString.restype = ptr
    cf.CFDictionaryCreateMutable.argtypes = [ptr, c.c_long, ptr, ptr]
    cf.CFDictionaryCreateMutable.restype = ptr
    cf.CFDictionarySetValue.argtypes = [ptr, ptr, ptr]
    nf.NetFSMountURLSync.argtypes = [ptr, ptr, ptr, ptr, ptr, ptr, c.POINTER(ptr)]
    nf.NetFSMountURLSync.restype = c.c_int
    def string(value):
        return cf.CFStringCreateWithCString(None, value.encode(), 0x08000100)
    options = cf.CFDictionaryCreateMutable(None, 0, None, None)
    cf.CFDictionarySetValue(options, string("UIOption"), string("NoUI"))
    url = cf.CFURLCreateWithString(None, string(f"smb://{USER}@{HOST}/{share}"), None)
    mounts = ptr()
    status = nf.NetFSMountURLSync(url, None, string(USER), None, options, None, c.byref(mounts))
    if status or not correct_mount(share, mount_lines()):
        print(f"{share}: reconnect failed, NetFS status {status}", flush=True)
        return 1
    print(f"{share}: reconnected at /Volumes/{share}", flush=True)
    return 0


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--mount" and sys.argv[2] in SHARES:
        return mount_share(sys.argv[2])
    missing = [share for share in SHARES if not correct_mount(share, mount_lines())]
    if not missing:
        return 0
    try:
        with socket.create_connection((HOST, 445), timeout=2):
            pass
    except OSError:
        return 0  # Cable absent; launchd retries later without a prompt.
    failed = False
    for share in missing:
        target = Path("/Volumes") / share
        if target.exists() and (os.path.ismount(target) or any(target.iterdir())):
            print(f"{share}: unexpected occupied path, leaving it alone", flush=True)
            failed = True
            continue
        try:
            result = subprocess.run([sys.executable, __file__, "--mount", share], timeout=45)
            failed |= result.returncode != 0
        except subprocess.TimeoutExpired:
            print(f"{share}: reconnect timed out; will retry", flush=True)
            failed = True
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
