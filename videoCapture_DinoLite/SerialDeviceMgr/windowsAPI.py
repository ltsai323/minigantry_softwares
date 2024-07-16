#!/usr/bin/env python3
import time
import SerialDeviceMgr.frag as frag

OPERATION_SYSTEM = 'windows' # used for check code version
COMMUNICATION_PERIOD = 0.4

debug_mode = False
def BUG(mesg):
    if debug_mode:
        print(f'[BUG] {mesg}')
def SetLog(primaryLOG, secondaryLOG):
    BUG('Updating log function at SerialDeviceMgr')
    frag.PrimaryLog = primaryLOG
    frag.SecondaryLog = secondaryLOG


class InputConf:
    def __init__(self, **xargs):
        self.listed_dev = frag.list_available_port()

class API:
    def __init__(self,inputCONF:InputConf):
        self.conf = inputCONF
    def set(self, **xargs):
        self.device_name = xargs['TTY Device']
        BUG(f'Initializing device {self.device_name}')
        self.instance = frag.MachineStatus(frag.init(self.device_name))

    def list_setting(self) -> list:
        return [
                { 'name': 'TTY Device', 'type': 'option', 'options': self.conf.listed_dev },
        ]
    def run(self) -> int:
        '''
        Return job status is alive or not
        1: this run is finished safely
        0: the whole job is stopped. (Finished or connection lost)
        '''
        self.instance.SetValue()
        self.instance.Communicate(COMMUNICATION_PERIOD)
        return self.instance.job_status


class test_api:
    def __init__(self,inputCONF:frag):
        self.conf = inputCONF
        self.max_counter = 5
    def set(self, **xargs):
        self.device_name = xargs['TTY Device']
        BUG(f'Initializing device {self.device_name}')
        self.instance = frag.MachineStatus(frag.init(self.device_name))

    def list_setting(self) -> list:
        return [
                { 'name': 'TTY Device', 'type': 'option', 'options': self.conf.listed_dev },
        ]
    def run(self) -> int:
        '''
        Return job status is alive or not
        1: this run is finished safely
        0: the whole job is stopped. (Finished or connection lost)
        '''
        frag.SecondaryLog('test run start!!!')
        frag.write(self.instance.serial_device, '1')
        time.sleep(1)
        frag.write(self.instance.serial_device, '0')
        time.sleep(0.5)
        frag.SecondaryLog('test run stopped!!!')

        self.max_counter -= 1
        return self.max_counter >= 0

def APIfactory(yamlDICT) -> API:
    try:
        ### add input validation if needed
        c = InputConf(**yamlDICT)
        if debug_mode:
            BUG('Create a test_api instance')
            return test_api(c)
        return API(c)
    except KeyError as e:
        print(f'[KeyError] Key "{e}" is required. Check the yaml file')


if __name__ == "__main__":
    def primary_log(mesg):
        print(f'[p] {mesg}')
    def secondary_log(mesg):
        print(f'[s] {mesg}')
    SetLog(primary_log,secondary_log)
    with open('data/serial_device_windows.yaml','r') as f:
        import yaml
        yaml_dict = yaml.safe_load(f)
        c = InputConf(**yaml_dict)
        if debug_mode:
            api = test_api(c)
        else:
            api = API(c)

    all_settings = api.list_setting()
    setting = [ setting['options'] for setting in all_settings if setting['name'] == 'TTY Device' ]
    all_available_dev = setting[0]
    print(f'[SerialDeviceCandidates] {all_available_dev}')
    chosen_dev = [ dev for dev in all_available_dev if 'COM' in dev or 'usbmodem' in dev ]
    print(f'[ChosenDevices] Filtered serial devices {chosen_dev}. Use the first one {chosen_dev}')
    #print(f'[ChosenDevices] Filtered serial devices {chosen_dev}. Use the first one {chosen_dev[0]}')

    print(api.list_setting())
    api.set( **{'TTY Device': chosen_dev[0]} )
    print(api.device_name)
    print('[Run started] hiiii')
    api.run()
    api.run()
    api.run()
