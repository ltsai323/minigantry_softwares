import serial
import time
import sys

# Replace '/dev/tty.usbmodemXXXX' with your actual device name
#serial_port = '/dev/tty.usbmodem11201'
serial_port = sys.argv[1]
baud_rate = 9600  # Ensure this matches the baud rate set in your Pico script

# Initialize the serial connection
ser = serial.Serial(serial_port, baud_rate, timeout=5.0)
#ser = serial.Serial(serial_port, baud_rate)

# Give some time for the connection to be established
time.sleep(2)

print("Starting to read messages from Pico...\n")

mesg_interpret = {
        '0': 'mini gantry report stat high',
        '1': 'mini gantry report stat low',
        }

readON = '0'
readOFF= '1'

def count_timing(func, *args):
    t0 = time.time()
    mesg = func(*args)
    t1 = time.time()
    diff = 1000.*(t1-t0)
    #if mesg:
    #    print(f'[GotMesg ({diff:5.1f} us)] "{mesg}"')
    print(f'[GotMesg ({diff:5.1f} ms)] "{mesg}"')
    return mesg

def read_message(serialDEV):
    mesg = serialDEV.read().decode('utf-8').strip()
    return mesg
def read_message_readline(serialDEV):
    mesg = serialDEV.readline().decode('utf-8').strip()
    return mesg


try:
    ser.flush()
    counter = 0
    while True:
        if ser.in_waiting > 0:
            time.sleep(1.0)
            ser.flushInput() # clear buffer after sleeping
            mesg = count_timing(read_message_readline, ser)
except KeyboardInterrupt:
    print("\nExiting...")

finally:
    ser.close()
    print("Serial connection closed.")
