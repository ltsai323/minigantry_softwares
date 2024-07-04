import serial
import time
import sys

# Replace '/dev/tty.usbmodemXXXX' with your actual device name
#serial_port = '/dev/tty.usbmodem11201'
serial_port = sys.argv[1]
baud_rate = 9600  # Ensure this matches the baud rate set in your Pico script

# Initialize the serial connection
ser = serial.Serial(serial_port, baud_rate)

# Give some time for the connection to be established
time.sleep(2)

print("Starting to read messages from Pico...\n")

flag = 0
try:
    ser.flush()
    while True:
        #print('                             reading...')
        if ser.in_waiting > 0:
            # Read the incoming data
            #message = ser.readline().decode('utf-8').strip()
            
            
            ser.write(f'{flag%10}'.encode())
            flag = 1 if flag == 0 else 0
            time.sleep(3)

            #print(f"Received: {message}")
except KeyboardInterrupt:
    print("\nExiting...")

finally:
    ser.close()
    print("Serial connection closed.")
