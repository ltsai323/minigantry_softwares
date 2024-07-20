import serial
import time
import sys

def BUG(mesg):
    print(f'[BUG] {mesg}')
def WARNING(mesg):
    print(f'[WARNING] {mesg}')
debug_mode = True
LAZY_SLEEP = 0.5
# Replace '/dev/tty.usbmodemXXXX' with your actual device name
#serial_port = '/dev/tty.usbmodem11201'
serial_port = sys.argv[1]
baud_rate = 9600  # Ensure this matches the baud rate set in your Pico script

# Initialize the serial connection
ser = serial.Serial(serial_port, baud_rate, timeout=1.0)


print("Starting to read messages from Pico...\n")

# read off : mini gantry report movement started
# read on  : mini gantry report movement ended
# write on : send trigger to mini gantry
# write off: if mini gantry reports message received, turn it off. (Once both write on and read on detected, turn off it)

# Strategy : Do something and send trigger to mini gantry.



readON = '0'
readOFF= '1'
writeON = '1'.encode()
writeOFF= '0'.encode()
flag = 0


def read_message(serialDEV, flushBEFOREread=False):
    if flushBEFOREread:
        # waiting for first character after clear
        serialDEV.flushInput() # clear buffer after sleeping
    return serialDEV.readline().decode('utf-8').strip()

def do_another_thing():
    time.sleep(2) # simulates another job requires 5 second
    print('[something done]')
    return


COMMUNICATION_TIMEOUT_COUNTER = 30
try:
    ser.flush()
    ser.write(writeOFF)
    write_stat = writeOFF
    read_stat = readOFF

    new_event = False
    lazy_counter = 3
    l_counter = lazy_counter
    print('[standby] Waiting for input signal')
    while True: # Waiting for a trigger for starting program
        if ser.in_waiting<=0: continue # skip no input buffer (Not communicated) situation.
        time.sleep(LAZY_SLEEP)
        mesg = read_message(ser, True)

        if mesg == readON:
            l_counter -= 1
        if mesg == readOFF:
            l_counter = lazy_counter # reset

        if l_counter < 0:
            new_event = True
            BUG(f'[StartMainProgram] Got message "{mesg}" triggered main program')
            ser.write(writeON) # use a ON-OFF pair notifies user that can do next step
            time.sleep(0.3)
            ser.write(writeOFF)
            break

    print('[JobInitialized] Waiting for start trigger')
    while True:
        if ser.in_waiting<=0: continue
        time.sleep(LAZY_SLEEP)
        mesg = read_message(ser, True)
        if mesg == readOFF:
            break
    print('[busyMode] start Looping')
    while new_event:
        if ser.in_waiting<=0: continue # skip no input buffer (Not communicated) situation.

        do_another_thing()

        check_current_status = read_message(ser,True) # waiting for first character after clear
        if check_current_status == readON:
            WARNING(f'New event started but reading signal is activated.')

        ser.write(writeON)

        counter = COMMUNICATION_TIMEOUT_COUNTER
        while True: # check hand shaking from mini gantry
            if counter < 0:
                new_event = False # if mini gantry reports nothing, program reported ended
                BUG(f'Connection timeout. Ending of the program')
                break

            mesg = read_message(ser)
            if not mesg:
                continue
            if mesg == readON:
                ser.write(writeOFF)
                break
            else:
                counter-=1 # if nothing received, count down for checking feedback.
        if new_event == False: continue
        while True: # waiting for end of movement from mini gantry
            mesg = read_message(ser)
            if not mesg:
                continue
            if mesg == readOFF:
                break
except KeyboardInterrupt:
    print("\nExiting...")

finally:
    ser.write(writeOFF)
    ser.close()
    print("Serial connection closed.")
