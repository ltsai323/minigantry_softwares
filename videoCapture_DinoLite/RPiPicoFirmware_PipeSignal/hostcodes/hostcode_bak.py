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

flag = 0
try:
    ser.flush()
    counter = 0
    while True:
        #print('                             reading...')
        if ser.in_waiting > 0:
            # Read the incoming data
            #message = ser.readline().decode('utf-8').strip()


            print('[add counter]')
            counter += 1
            #if counter %30 == 0:
            #    ser.write(f'{flag%10}'.encode())
            #    flag = 1 if flag == 0 else 0
            ### tesitng
            ser.write(f'{flag%10}'.encode())# flip every 0.1 second
            flag = 1 if flag == 0 else 0
            ### tesitng end
            print('[reading message]')
            mesg = ''
            #while True:
            #    mesg += ser.read(ser.in_waiting).decode('utf-8')
            #    print(f'[got mesg] {mesg}')
            mesg = ser.readline().decode('utf-8').strip()
            print(f'[got mesg] {mesg}')

            #mesg = ser.readlines().decode('utf-8').strip()
            #print(f'[mesg] {mesg}')

            time.sleep(0.1)

            #print(f"Received: {message}")
except KeyboardInterrupt:
    print("\nExiting...")

finally:
    ser.close()
    print("Serial connection closed.")
