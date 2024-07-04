import serial

def read_from_uart():
    # Replace '/dev/ttyUSB0' with the correct port on your computer
    ser = serial.Serial('/dev/tty.usbmodem11301', 9600, timeout=1)
    ser.flush()

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(f"Received: {line}")

if __name__ == "__main__":
    read_from_uart()
