import serial
import time
import sys
import yaml

def BUG(mesg):
    bug_mode = False
    if bug_mode:
        print(f'[BUG] {mesg}')
def PrimaryLog(mesg):
    print(f'[Status] {mesg}')
def SecondaryLog(mesg):
    print(f'[Action] {mesg}')



def init(serialPORT):
    baud_rate = 9600  # Ensure this matches the baud rate set in your Pico script

    try:
# Initialize the serial connection
        ser = serial.Serial(serialPORT, baud_rate)
        ser.flush()

        time.sleep(1)
        return ser
    except:
        return None



def read(serialDEV) -> str:
    try:
        if serialDEV.in_waiting > 0:
            return serialDEV.readline().decode('utf-8').strip()
        return ''
    except KeyboardInterrupt:
        PrimaryLog('Abort')
        SecondaryLog('exiting serial device reading')
def write(serialDEV, theMESG:str):
    try:
        #serialDEV.write(f'{theMESG}'.encode())
        serialDEV.write(theMESG.encode())
    except KeyboardInterrupt:
        PrimaryLog('Abort')
        SecondaryLog('exiting serial device writing')

STAT_ON  = '1'
STAT_OFF = '0'
class MachineStatus:
    MAX_COUNTER = 5 # how much Communicate() iterates.
    def __init__(self,serialDEV):
        self.serial_device = serialDEV
        self.stat_read = STAT_OFF
        self.stat_write = STAT_OFF
        self.job_status = 1 if serialDEV else 0
        self.job_status_counter = MachineStatus.MAX_COUNTER

    def communicate_once(self) -> bool:
        '''
        return the communication status. False: Job is finished. True: job is still working
        workflow: Write a signal to device, then waiting for feedback and waiting for ending of the feedback.

        Detail of check the read and write status:
            * if both write and read are OFF: finish communication
            * if write is ON but read OFF:
                - If situation keeps for a long time. Reguard serial device is dead or job finished. (And job will be finished at next communication)
                - If further received read ON, set write to OFF.
            * if write is OFF and read is ON: Job is still working
        '''
        
        if self.job_status == 0:
            PrimaryLog('Job Stopped')
            SecondaryLog('serial device disconnected')
            return False

        self.stat_read = read(self.serial_device)
        write(self.serial_device, self.stat_write)

        BUG(f'Read {self.stat_read} and Write {self.stat_write}')
        if self.stat_write == STAT_ON:
            if self.stat_read == STAT_ON:
                # hand shake established. Got bidirectional communication.
                self.stat_write = STAT_OFF # got feedback from device. Connection checked.
                self.job_status_counter = MachineStatus.MAX_COUNTER # reset counter
                # end of communication. Signal sent and got feedback
            else:
                # Once counter goes to 0, Either missing connection or Job finished.
                self.job_status_counter -= 1
                if self.job_status_counter == 0:
                    self.job_status = 0 # Disconnected
                    PrimaryLog('Timeout')
                    SecondaryLog('Automatically disconnected the serial device')
                    return False
        else:
            if self.stat_read == STAT_OFF:
                # both read and write are off: End of communication. The device returned a finished job
                return False
            # if stat_wirte is OFF and state_read is also ON: Keep monitoring until stat_read OFF
        return True
    def Communicate(self, monitoringPERIOD) -> None:
        communicating = True
        while communicating:
            time.sleep(monitoringPERIOD)
            communicating = self.communicate_once()

        
    @property
    def GetStatus(self):
        return int(self.stat_read)
    def SetValue(self):
        self.stat_write = STAT_ON

def GetPicoDevice(deviceWILDCARD:str) -> str:
    # '/dev/tty.usb*'
    import glob
    return glob.glob(deviceWILDCARD)






def testfunc_direct_run():
    serial_dev = init('/dev/tty.usbmodem101')
    t=10
    while t>0:
        time.sleep(1.2)
        write(serial_dev, '0')
        time.sleep(0.4)
        write(serial_dev, '1')
        t-=1
        print(f't {t}')
    write(serial_dev, '0')

if __name__ == "__main__":
    testfunc_direct_run()
