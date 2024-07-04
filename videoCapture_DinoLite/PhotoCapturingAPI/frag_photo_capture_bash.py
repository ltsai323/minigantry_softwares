import subprocess
import time
import pyautogui

def Status(mesg): print(f'[Status] {mesg}')
def Action(mesg): print(f'[Action] {mesg}')
print('[NotImplementedCode]')
exit(1)


# Launch the application
# For Windows Notepad:
# subprocess.Popen(["notepad.exe"])
# For macOS TextEdit:
subprocess.Popen(["open", "-a", "TextEdit"])


# Give the application some time to launch
time.sleep(3)

#pyautogui.hotkey('command','N')
#pyautogui.keyDown('command')
#pyautogui.keyDown('shift')
#pyautogui.press('/')
#pyautogui.keyUp('command')
#pyautogui.keyUp('shift')

pyautogui.keyDown('command')
pyautogui.press('n')
pyautogui.keyUp('command')

time.sleep(1)

DELAY_delay_waiting_for_start = 3
def launch_application(appACTIVATEstr:str, delayWAITINGforSTART=DELAY_delay_waiting_for_start):
    # activate application
    import os
    os.system(f'start explorer shell:appsfolder\{app_activate_str}')
    time.sleep(delayWAITINGforSTART) # waiting for app activated


class WindowMgr:
    def __init__(self):
        self._handle = None
        self._alive = False

    def find_window(self, class_name, window_name=None):
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)
        if self._handle == None:
            Status('ApplicationNotOpened')
            Action(f'WindowMgr found no window from wildcard "{wildcard}"')
            self._alive = False
            exit(1)
        self._alive = True

    def set_foreground(self):
        try:
            win32gui.SetForegroundWindow(self._handle)
        except:
            Status('ApplicationNoLongerAlive')
            self._alive = False
            exit(2)

    def IsAlive(self):
        return self._alive

# Send keystrokes
pyautogui.typewrite("Hello, world!")


if __name__ == "__main__":
