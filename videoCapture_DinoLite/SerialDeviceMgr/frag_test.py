import serial
import time
import sys
import yaml
import threading

def BUG(mesg):
    bug_mode = False
    if bug_mode:
        print(f'[BUG] {mesg}')
def PrimaryLog(mesg):
    print(f'[PiPicoFrag - 1stLOG] {mesg}')
def SecondaryLog(mesg):
    print(f'[PiPicoFrag - 2ndlog] {mesg}')

def list_available_port() -> list:
    import serial.tools.list_ports as list_ports
    ports = list_ports.comports()
    print(f'Got {len(ports)} serial devices: ')
    for idx,port in enumerate(ports):
        print(f'No.{idx}')
        print(f'  Port: {port.device}')
        print(f'  Description: {port.description}')
        print(f'  Hardward ID: {port.hwid}')
    return [ port.device for port in ports ]




def init(serialPORT):
    baud_rate = 9600  # Ensure this matches the baud rate set in your Pico script

    try:
# Initialize the serial connection
        ser = serial.Serial(serialPORT, baud_rate, timeout=1.0) # timeout prevents readline stucks the program
        ser.flush()

        return ser
    except:
        return None


def read_message(serialDEV, flushBEFOREread=False):
    if flushBEFOREread:
        # waiting for first character after clear
        serialDEV.flushInput() # clear buffer after sleeping
    return serialDEV.readline().decode('utf-8').strip()
def forceStopped(externalFLAG:threading.Event) -> bool:
    if externalFLAG.is_set():
        SecondaryLog('Force Stopped')
        return True
    return False

''' old mthod '''
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
''' old mthod '''

readON = '0'
readOFF= '1'
writeON = '1'.encode()
writeOFF= '0'.encode()
class MachineStatus:
    MAX_COUNTER = 5 # how much Communicate() iterates.
    STANDBY_COUNTER = 3
    STANDBY_SLEEP = 0.4
    COMMUNICATION_TIMEOUT_COUNTER = 30
    def __init__(self,serialDEV):
        self.serial_device = serialDEV

        self.stat_read = readOFF # new
        self.stat_write = writeOFF # new
        #self.stat_read = STAT_OFF # old
        #self.stat_write = STAT_OFF # old
        self.job_status = 1 if serialDEV else 0
        #self.job_status_counter = MachineStatus.MAX_COUNTER
        if self.job_status:
            self.serial_device.write(writeOFF) # new
            self.stat_write = writeOFF # new
            #write(self.serial_device, self.stat_write) # initialize IO as program started # old
    def close(self):
        self.job_status = 0
        self.serial_device.write(writeOFF)
        self.write_stat = writeOFF
        self.serial_device.close()

    # old
    #def communicate_once(self) -> bool:
    #    '''
    #    return the communication status. False: Job is finished. True: job is still working
    #    workflow: Write a signal to device, then waiting for feedback and waiting for ending of the feedback.

    #    Detail of check the read and write status:
    #        * if both write and read are OFF: finish communication
    #        * if write is ON but read OFF:
    #            - If situation keeps for a long time. Reguard serial device is dead or job finished. (And job will be finished at next communication)
    #            - If further received read ON, set write to OFF.
    #        * if write is OFF and read is ON: Job is still working
    #    '''

    #    if self.job_status == 0:
    #        PrimaryLog('PiPico Aborts communications')
    #        SecondaryLog('serial device disconnected')
    #        return False

    #    self.stat_read = read(self.serial_device)
    #    write(self.serial_device, self.stat_write)

    #    BUG(f'Read {self.stat_read} and Write {self.stat_write}')
    #    if self.stat_write == STAT_ON:
    #        if self.stat_read == STAT_ON:
    #            # hand shake established. Got bidirectional communication.
    #            self.stat_write = STAT_OFF # got feedback from device. Connection checked.
    #            self.job_status_counter = MachineStatus.MAX_COUNTER # reset counter
    #            # end of communication. Signal sent and got feedback
    #        else:
    #            # Once counter goes to 0, Either missing connection or Job finished.
    #            self.job_status_counter -= 1
    #            if self.job_status_counter == 0:
    #                self.job_status = 0 # Disconnected
    #                PrimaryLog('Timeout')
    #                SecondaryLog('Automatically disconnected the serial device')
    #                return False
    #    else:
    #        if self.stat_read == STAT_OFF:
    #            # both read and write are off: End of communication. The device returned a finished job
    #            return False
    #        # if stat_wirte is OFF and state_read is also ON: Keep monitoring until stat_read OFF
    #    return True
    def standby_mode(self, stopFLAG:threading.Event = threading.Event()) -> None:
        ''' monitoring for read port. Turn off stand by mode once read port keeping ON for a period of time.
        1. Check the initial state is OFF
        2. Check the secondary state is ON or OFF
           * ON: counting the number. Once the counter reaches threshold, trigger closing stand by mode procedure.
           * OFF: reset counter
        3. Once stand by mode is off, set the write ON - OFF pair. To inform the user that stand by mode is closing now.
        4. Once the closing procedure is triggered, the stand by mode is OFF when a read OFF is received.
        '''
        if self.job_status == 0:
            PrimaryLog('PiPico Aborts StandBy Mode')
            SecondaryLog('serial device disconnected')
            #self.close()
            return

        SecondaryLog('Waiting for input trigger...')
        self.serial_device.flush()
        self.serial_device.write(writeOFF)
        self.stat_read = readOFF
        self.stat_write = writeOFF

        counter = MachineStatus.STANDBY_COUNTER
        stateInitialized = False
        while True: # waiting for a trigger starting main program from keep reading ON.
            if forceStopped(stopFLAG): return  # force stop from external process
            if not (self.serial_device.in_waiting>0): continue # skip nothing in buffer.
            time.sleep(MachineStatus.STANDBY_SLEEP)
            mesg = read_message(self.serial_device, True)

            if not stateInitialized:
                if mesg == readOFF:
                    stateInitialized = True
            if not stateInitialized: continue
            ### initial state is checked to OFF. waiting for ON.

            if mesg == readON:
                counter -= 1

            if mesg == readOFF:
                if counter != MachineStatus.STANDBY_COUNTER: # only reset it if counter is not default
                    counter = MachineStatus.STANDBY_COUNTER # reset conter if OFF
            if counter < 0:
                SecondaryLog('Program activated...')

                # Use a ON-OFF pair notifies user that can do next step
                self.serial_device.write(writeON)
                time.sleep(0.4)
                self.serial_device.write(writeOFF)
                break

        SecondaryLog('Waiting for start button')
        while True:
            if forceStopped(stopFLAG): return # force stop from external process
            if not (self.serial_device.in_waiting>0): continue # skip nothing in buffer.
            time.sleep(MachineStatus.STANDBY_SLEEP)
            mesg = read_message(self.serial_device, True)
            if mesg == readOFF: break
        SecondaryLog('End of Standby Mode')
        return

    def waitFeedback(self, stopFLAG:threading.Event = threading.Event()) -> None:
        '''
        | channel | t0 | t1 | t2 | t3 | t4 | t5 | t6 |
        |  write  |  0 |  1 |  1 |  0 |  0 |  0 |  0 |
        |   read  |  0 |  0 |  1 |  1 |  1 |  0 |  0 |
        t0 : initialize state
        t1 : this function set write ON
        t2 : waiting for read ON
        t3 : once read ON detected, set write OFF
        t4 : waiting for read OFF
        t5 : read OFF from control end.
        t6 : Finish this function.
        1. write ON
        2. checking read port
          * ON : handshaking established. set write OFF when handshaked.
          * OFF: Counting the number, once the counter reaches threshold, set a TIMEOUT error
        3. check read port OFF for ending of the action
        '''
        if self.job_status == 0:
            PrimaryLog('PiPico Aborts function')
            SecondaryLog('A closed Job detected. Abort waitFeedback().')
            return
        if forceStopped(stopFLAG): return

        if not (self.serial_device.in_waiting>0): return
        check_current_status = read_message(self.serial_device, True)
        if check_current_status == readON:
            PrimaryLog('PiPico WARNING')
            SecondaryLog('read status ON but it is assumed OFF now. Ignoring...')
            time.sleep(5)
            self.serial_device.flushInput()

        self.serial_device.write(writeON)
        self.write_stat = writeON

        counter = MachineStatus.COMMUNICATION_TIMEOUT_COUNTER
        SecondaryLog('Downstream handshaking...')
        while True: # waiting for readON
            if forceStopped(stopFLAG): return
            mesg = read_message(self.serial_device)
            if not mesg: continue
            if mesg == readON:
                self.serial_device.write(writeOFF)
                self.write_stat = writeOFF
                SecondaryLog('Communication Established')
                break
            else:
                counter -= 1 # if readOFF received, activate counter.
                if counter < 0:
                    break

        if counter < 0:
            SecondaryLog('Timeout Detected. Program Stopped')
            self.job_status = False
            return

        
        read_timeout = COMMUNICATION_TIMEOUT_COUNTER
        while True: # waiting for readOFF
            if forceStopped(stopFLAG): return
            mesg = read_message(self.serial_device)
            if not mesg: continue
            if mesg == readOFF: break
            else:
                read_counter -= 1
            if read_counter == 0:
                SecondaryLog('Stopped from mini gantry, Press START button to restart')
        SecondaryLog('Action Finished')




        
    def Communicate(self, stopFLAG=threading.Event()) -> int:
        try:
            self.waitFeedback(stopFLAG)
        except KeyboardInterrupt:
            SecondaryLog('Keyboard Interrupts Communicate')
        finally:
            self.close()
        return self.job_status
    def StandBy(self, stopFLAG=threading.Event()) -> bool:
        try:
            self.standby_mode(stopFLAG)
        except KeyboardInterrupt:
            SecondaryLog('Keyboard Interrupts StandBy')
        finally:
            self.close()
        return self.job_status
        
        ### monitoringPERIOD is disabled
        # old
        #communicating = True
        #while communicating:
        #    time.sleep(monitoringPERIOD)
        #    communicating = self.communicate_once()


   # old
   # @property
   # def GetStatus(self):
   #     return int(self.stat_read)
   # def SetValue(self):
   #     self.stat_write = STAT_ON

''' Replaced by list_available_port
def GetPicoDevice(deviceWILDCARD:str) -> str:
    # '/dev/tty.usb*'
    import glob
    return glob.glob(deviceWILDCARD)
 '''





def testfunc_direct_run():
    all_dev = list_available_port()
    possible_dev = [ dev for dev in all_dev if 'COM' in dev or 'usbmodem' in dev ]
    if len(possible_dev) == 0:
        print(f'[NoAvailableSerialDevice] All listed devices are {all_dev}. But no candidate found')
        exit()
    print(f'possible candidates {possible_dev} found. Only use the first one "{possible_dev[0]}"')
    dev = possible_dev[0]
    serial_dev = init(dev)

    #serial_dev = init('/dev/tty.usbmodem101') # From bash
    #serial_dev = init('COM8') # From windows
    print('[Running] Looping for 10 run()')
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
