import serial
import time
import sys

# Replace '/dev/tty.usbmodemXXXX' with your actual device name
#serial_port = '/dev/tty.usbmodem11201'
serial_port = sys.argv[1]
baud_rate = 9600  # Ensure this matches the baud rate set in your Pico script

# Initialize the serial connection
ser = serial.Serial(serial_port, baud_rate, timeout=0)

# Give some time for the connection to be established
time.sleep(2)

print("Starting to read messages from Pico...\n")

mesg_interpret = {
        '0': 'mini gantry report stat high',
        '1': 'mini gantry report stat low',
        }

readON = '0'
readOFF= '1'
writeON = '1'.encode()
writeOFF= '0'.encode()
MINI_GANTRY_OFFSET = 0.25
WAITING_FOR_NEXT_EVENT = 0.4


f = open('mini_gantry_latency.txt','w')
f.write('turn_on,turn_off\n')
try:
    ser.flush()
    counter = 0
    while True:
        #print('                             reading...')
        if ser.in_waiting > 0:
            ser.write(writeON)
            time_ref = time.time()
            time_read_on = None
            time_read_off = None

            current_stat = 0 # read nothing
            while True:
                mesg = ser.readline().decode('utf-8').strip()
                if time_read_on == None:
                    if mesg == readON:
                        time_read_on = time.time()
                        ser.write(writeOFF)
                else:
                    if time_read_off == None:
                        if mesg == readOFF:
                            time_read_off = time.time()
                            break # end of the looping

            read_on_latency = time_read_on - time_ref
            read_off_latency = time_read_off - time_ref - MINI_GANTRY_OFFSET
            print(f'[Show Result] Turn on latency {read_on_latency:.2f} and turn off latency {read_off_latency:.2f}')
            f.write(f'{read_on_latency:.6f},{read_off_latency:.6f}\n')
            time.sleep(WAITING_FOR_NEXT_EVENT)

            #print(f"Received: {message}")
except KeyboardInterrupt:
    print("\nExiting...")
    f.close()

finally:
    ser.write(writeOFF)
    ser.close()
    print("Serial connection closed.")
