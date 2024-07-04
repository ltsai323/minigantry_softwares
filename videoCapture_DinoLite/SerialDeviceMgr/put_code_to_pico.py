#!/usr/bin/env python3

def GetPicoDevice() -> str:
    import glob
#import os
#pico_candidate = [ dev for dev in os.listdir('/dev') if 'usb' in dev and 'tty' in dev ]
    pico_candidate = glob.glob('/dev/tty.usb*')
    print(pico_candidate)

    pico_device = ''
    if pico_candidate == []:
        raise IOError('[NoDeviceCandidateFound] Please check whether device connected')
    if len(pico_candidate) == 1:
        pico_device = pico_candidate[0]
    else:
        print('[Choose the device from candidate:')
        for i,candidate in enumerate(pico_candidate):
            print(f'   {i}: {candidate}')

        while True:
            v = input('Input index [(0~{len(pico_candidate)})]')
            try:
                in_idx = int(v)
                pico_device = pico_candidate[in_idx]
                break
            except:
                print('Invalid input, choose it again')

    print(f'Selected Device: {pico_device}')
    return pico_device
    

def TemperorallyRunCodeIntoPico(picoDEV:str, inCODE:str):
    import os
    bash_cmd = f'ampy --port {picoDEV} -b 9600 run {inCODE}'
    print(f'[Exec] {bash_cmd}')
    os.system(bash_cmd)
def PermanentlyPutCodeIntoPico(picoDEV:str, inCODE:str):
    import os
    bash_cmd = f'ampy --port {picoDEV} -b 9600 put {inCODE} /main.py'
    print(f'[Exec] {bash_cmd}')
    os.system(bash_cmd)
    

if __name__ == "__main__":
    pico_device = GetPicoDevice()
    TemperorallyRunCodeIntoPico(pico_device, 'pico_pipe_message_and_show_status.py')
    #TemperorallyRunCodeIntoPico(pico_device, '../helloworld_LEDblink.py')
