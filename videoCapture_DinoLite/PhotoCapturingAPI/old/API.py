#!/usr/bin/env python3

import PhotoCapturingAPI.frag_mac as frag
import time
class InputConf:
    def __init__(self,
                 init_delay:float,
                 app_name:str,
                 work_delay:float,
                 ):
        self.app_name = str(app_name)
        self.init_delay = float(init_delay)
        self.work_delay = float(work_delay)
class API:
    def __init__(self,inputCONF):
        self.conf = inputCONF
        self.app = frag.init(self.conf.app_name, self.conf.init_delay)
    def set(self, **xargs):
        #self.conf.work_delay = float(xargs['work_delay'])
        return
        
    def list_setting(self):
        # a = [ { 'name': 'work_delay', 'type': 'text', 'default': str(self.conf.work_delay) }, ] # work_delay is only adjusted in yaml file
        return []

    def run(self):
        if self.app == None: return 0 # Once app is not activated or not in search list, disable thrunrun.
        frag.send_hotkey_to(self.app, self.conf.work_delay)
        return 1 # return status activate this app

class test_api:
    def __init__(self,inputCONF):
        self.conf = inputCONF
        #self.app = frag.init(self.conf.app_name, self.conf.init_delay)
    def set(self, **xargs):
        self.conf.work_delay = float(xargs['work_delay'])
        
    def list_setting(self):
        a = [
                { 'name': 'work_delay', 'type': 'text', 'default': str(self.conf.work_delay) },
                ]
        return a

    def run(self):
        frag.SecondaryLog('send hotkey to ...')
        time.sleep(self.conf.work_delay)
        frag.SecondaryLog('hotkey sent')
        return 1


def APIfactory(yamlFILE):
    with open(yamlFILE,'r') as f:
        yaml_dict = yaml.safe_load(f)
        try:
            c = InputConf(**yaml_dict)
            return API(c)
        except KeyError as e:
            print(f'[KeyError] Key "{e}" is required. Check the yaml file')

def SetLog(primaryLOG, secondaryLOG):
    frag.PrimaryLog = primaryLOG
    frag.SecondaryLog = secondaryLOG

if __name__ == "__main__":
    api = APIfactory('../data/photo_capture_macOS.yaml')
    api.run()
