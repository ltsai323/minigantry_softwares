import subprocess
import time
import pyautogui
from AppKit import NSWorkspace, NSApplicationActivateIgnoringOtherApps
from appscript import app, k
'''
conda install appscript
'''

# Launch TextEdit
#subprocess.Popen(["/System/Applications/TextEdit.app/Contents/MacOS/TextEdit"])
subprocess.Popen(['open', '-a', 'TextEdit'])

# Allow some time for the application to launch
#time.sleep(2)

# Bring TextEdit to the foreground
workspace = NSWorkspace.sharedWorkspace()
apps = workspace.runningApplications()
textedit_app = None
print('activating')
time.sleep(2)
for app in apps:
    if app.localizedName() == "TextEdit":
        app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)
        textedit_app = app
        break

for a in range(5):
    time.sleep(3)
    print('activating {a}')
    textedit_app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)
    textedit_app = app
    pyautogui.keyDown('command')
    pyautogui.press('n')
    pyautogui.keyUp('command')
# Allow some time for the application to come to the foreground
#pyautogui.hotkey('command', 'n')
exit()
time.sleep(1)

# Check the number of windows in TextEdit using appscript
textedit = app('TextEdit')
num_windows = len(textedit.windows())

if num_windows > 1:
    print("Warning: More than one window is open in TextEdit. Hotkey will not be sent.")
else:
    # Send a hotkey (for example, Command + N to create a new document)
    pyautogui.hotkey('command', 'n')
