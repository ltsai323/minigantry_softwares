#!/usr/bin/env python3
import subprocess
import time
import pyautogui
from AppKit import NSWorkspace, NSApplicationActivateIgnoringOtherApps


def PrimaryLog(mesg): print(f'[Status] {mesg}')
def SecondaryLog(mesg): print(f'[Action] {mesg}')


def init(appNAME, initDELAY):
# Launch TextEdit
    subprocess.Popen(['open', '-a', appNAME])

# Allow some time for the application to launch
    time.sleep(initDELAY)

# Bring TextEdit to the foreground
    workspace = NSWorkspace.sharedWorkspace()
    apps = workspace.runningApplications()
    for app in apps:
        if app.localizedName() == appNAME:
            return app

    PrimaryLog('App Not Found')
    SecondaryLog(f'App name "{appNAME}" activates no application')
    return None


def set_foreground(app):
    app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)


def send_hotkey(hotKEY, workingDELAY):
# Send a hotkey (for example, Command + N to create a new document)
    pyautogui.hotkey(*hotKEY, interval=0.1)
    time.sleep(workingDELAY)
# Allow some time for the application to come to the foreground

if __name__ == "__main__":
    app = init("TextEdit", 5)
    hotkey = ['command','n']
    send_hotkey( app, hotkey, 2)
    hotkey = ['command','n']
    send_hotkey( app, hotkey, 2)
