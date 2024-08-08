#import re as win32gui
import win32gui
import re
import time
import pyautogui
import yaml

debug_mode = True
def BUG(mesg):
    if debug_mode:
        print(f'[BUG] {mesg}')
def info(mesg):
    print(f'i@ {mesg}')

def PrimaryLog(mesg):
    info(f'[Status] {mesg}')
    print(f'[Status] {mesg}')
def SecondaryLog(mesg):
    info(f'[Action] {mesg}')
    print(f'[Action] {mesg}')

DELAY_delay_waiting_for_start = 3
def launch_application(appACTIVATEstr:str, delayWAITINGforSTART=DELAY_delay_waiting_for_start):
    # Find arg1 by executing power shell command "get-StartApps"
    ''' result of get-StartApps
    MyASUS                 B9ECED6F.ASUSPCAssistant_qmba6cd70vzyy!App
    Mail                   microsoft.windowscommunicationsapps_8wekyb3d8bbwe!microsoft.windowslive...
    Calendar               microsoft.windowscommunicationsapps_8wekyb3d8bbwe!microsoft.windowslive...
    Microsoft Store        Microsoft.WindowsStore_8wekyb3d8bbwe!App
    Ubuntu 22.04.3 LTS     CanonicalGroupLimited.Ubuntu22.04LTS_79rhkp1fndgsc!ubuntu2204
    Microsoft Defender     Microsoft.6365217CE6EB4_8wekyb3d8bbwe!App
    Ubuntu on Windows      CanonicalGroupLimited.UbuntuonWindows_79rhkp1fndgsc!ubuntuonwindows
    '''
    # activate application
    import os
    os.system(f'start explorer shell:appsfolder\{appACTIVATEstr}')
    time.sleep(delayWAITINGforSTART) # waiting for app activated

def list_applications():
    import subprocess
    subprocess.call('powershell.exe get-StartApps', shell=True)
    print('Please choose the required name in these content')

class WindowMgr:
    def __init__(self):
        self._handle = None
        self._alive = False

    def find_window(self, class_name, window_name=None):
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            info(f'[GotWindowName] {str(win32gui.GetWindowText(hwnd))} with _handle={hwnd}')
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)
        info(f'[Got Handle] (type:{type(self._handle)}) - {self._handle}')
        if self._handle == None:
            PrimaryLog('ApplicationNotOpened')
            SecondaryLog(f'WindowMgr found no window from wildcard "{wildcard}"')
            self._alive = False
            exit(1)
        self._alive = True

    def set_foreground(self):
        try:
            win32gui.SetForegroundWindow(self._handle)
        except:
            PrimaryLog('ApplicationNoLongerAlive')
            self._alive = False
            exit(2)

    def IsAlive(self):
        return self._alive

def send_hotkey(hotKEY:list, workingDELAY):
    pyautogui.hotkey(*hotKEY, interval=0.1)
    time.sleep(workingDELAY)
'''
pip3 install pywin32
pip3 install pyautogui
'''
if __name__ == "__main__":
    list_applications()
