import serial
import time
import sys

debug_mode = True
CHECKING_PERIOD = 0.03
# Replace '/dev/tty.usbmodemXXXX' with your actual device name
#serial_port = '/dev/tty.usbmodem11201'
serial_port = sys.argv[1]
baud_rate = 9600  # Ensure this matches the baud rate set in your Pico script

# Initialize the serial connection
ser = serial.Serial(serial_port, baud_rate, timeout=0)

# Give some time for the connection to be established
time.sleep(2)

print("Starting to read messages from Pico...\n")


readON = '0'
readOFF= '1'
writeON = '1'.encode()
writeOFF= '0'.encode()
flag = 0
try:
    ser.flush()
    write_stat = writeOFF
    ser.write(writeOFF)
    read_stat = 0

    print('[Looping]')
    while True:
        #print('                             reading...')
        if ser.in_waiting > 0:
            # Read the incoming data
            #message = ser.readline().decode('utf-8').strip()
            mesg = ser.readline().decode('utf-8').strip()
            if not mesg: continue
            prev_read_stat = read_stat
            read_stat = mesg[-1]

            if debug_mode:
                mesg_r = 'readON' if read_stat == readON else 'readOFF'
                mesg_w = 'writeON' if write_stat == writeON else 'writeOFF'
                print(f'[one loop] read:{mesg_r} and write status {mesg_w}')


            if read_stat == readOFF and write_stat == writeOFF: # waiting for 30 looping. After that, set writing ON to trigger mini gantry
                print('[Waiting] Sleep for a while')
                time.sleep(2)
                ser.write(writeON)
                write_stat = writeON
                print('[Trigger sent] Pico told mini gantry for next point')

            if read_stat == readON and write_stat == writeON: # keep monitoring until communication established
                ser.write(writeOFF)
                write_stat = writeOFF
                print('[Communication Established] Reset Pico output trigger')
            if prev_read_stat == readOFF and prev_read_stat == readON:
                print('[PointArrival] Mini gantry reported movement finished.')

            time.sleep(CHECKING_PERIOD)


            #print(f"Received: {message}")
except KeyboardInterrupt:
    print("\nExiting...")

finally:
    ser.write(writeOFF)
    ser.close()
    print("Serial connection closed.")
