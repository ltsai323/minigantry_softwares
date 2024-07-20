#!/usr/bin/env python3

import subprocess

def get_output_from(cmd):
    res = subprocess.run(['powershell', '-Command', cmd], capture_output=True, text=True)
    return res.stdout

if __name__ == "__main__":
    mesg = get_output_from('get-StartApps')
    dino = [ line.strip() for line in mesg.split('\n') if 'DinoCapture' in line ]
    for l in dino:
        print(l)
