import PhotoCapturingAPI.frag_photo_capture_windows as frag
import time
OPERATION_SYSTEM = 'windows'

debug_mode = True
def BUG(mesg):
    if debug_mode:
        print(f'[BUG] {mesg}')
def SetLog(primaryLOG, secondaryLOG):
    frag.PrimaryLog = primaryLOG
    frag.SecondaryLog = secondaryLOG



class InputConf:
    def __init__(self,
                 init_delay:float,
                 app_activate_str:str,
                 window_name:str,
                 work_delay:float,
                 ):
        self.init_delay = float(init_delay)
        self.app_activate_str = app_activate_str
        self.wildcard = f'.*{window_name}.*'
        self.work_delay = float(work_delay)

class API:
    def __init__(self, inputCONF):
        self.conf = inputCONF

        frag.launch_application(self.conf.app_activate_str, self.conf.init_delay)
        self.w = frag.WindowMgr()
        self.w.find_window_wildcard(self.conf.wildcard)  # Thel window title is different, check task manager
    def set(self, **xargs):
        return
        
    def list_setting(self):
        return []

    def run(self):
        self.w.set_foreground()
        pyautogui.hotkey('ctrl','p', interval=0.1)
        time.sleep(self.conf.work_delay)
        return self.w.IsAlive()
class test_api:
    def __init__(self, inputCONF):
        self.conf = inputCONF
        time.sleep(self.conf.init_delay)
    def set(self, **xargs):
        self.conf.work_delay = float(xargs['work_delay_at_photoCapture'])
        
    def list_setting(self):
        a = [
                { 'name': 'work_delay_at_photoCapture', 'type': 'text', 'default': str(self.conf.work_delay) },
                ]
        return a

    def run(self):
        frag.SecondaryLog('send hotkey to ...')
        time.sleep(self.conf.work_delay)
        frag.SecondaryLog('hotkey sent')
        return 1

def APIfactory(yamlDICT) -> API:
    try:
        ### add validator if needed
        c = InputConf(**yamlDICT)
        if debug_mode:
            BUG('Create a test_api instance from PhotoCapguringAPI')
            return test_api(c)
        return API(c)
    except KeyError as e:
        print(f'[KeyError] Key "{e}" is required. Check the yaml file')
if __name__ == "__main__":
    # put correct string inside var
    app_activate_str = 'Microsoft.WindowsStore_8wekyb3d8bbwe!App' # window store
    window_name = 'Microsoft Store'

    #conf = InputConf(5, app_activate_str, window_name, 2)
    with open('../data/photo_capture_windows.yaml','r') as f:
        yaml_dict = yaml.safe_load(f)
        c = InputConf(**yaml_dict)
        if debug_mode:
            api = test_api(c)
        else:
            api = API(c)

    for i in range(5):
        api.run(0.2)
