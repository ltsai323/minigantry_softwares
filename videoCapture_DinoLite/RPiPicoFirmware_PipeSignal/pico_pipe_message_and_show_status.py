import machine
import utime
#import uos
import select
import sys
''' Manual
This code makes Raspberry pi pico as a serial device connecting to
PC. 1 input and 1 output port used to bidirectional communication 
to connected machine.

refresh period = 0.1 second
GPIO Pin10: Monitor the input state of Pin10 and send 0/1 to PC.
GPIO Pin16: Receive PC message 0/1 to control the state of Pin16.
(LED reflects the statement of Control GPIO Pin17.)


Example code uses this device:
    Baud rate : 9600
    Write message : 1 or 0. (Continuting write message until the timing you need)
    Message reading from this device : 1 or 0.


Note: This code does no logic analysis. You need to send message you need.
And you need to judge how to handle the IO behaviour.
'''

# Setup GPIO pins
gpio_read  = machine.Pin(10, machine.Pin.IN)
gpio_write = machine.Pin(16, machine.Pin.OUT)
led = machine.Pin(25, machine.Pin.OUT)  # On-board LED
REFRESH_PERIOD = 0.1

# Setup UART
#uart = machine.UART(0, baudrate=9600)
#uos.dupterm(uart)
def BUG(mesg):
    debug_mode = False
    if debug_mode:
        print(mesg)

def read_gpio_read():
    return gpio_read.value()

def set_gpio_write(value):
    gpio_write.value(value)
    led.value(value)

def main():
    while True:
        # Monitor GPIO 16 and send its status to the host device
        gpio_read_status = read_gpio_read()
        #uart.write('uart GPIO16 Status: {}\n'.format(gpio_read_status)) # UART communcates message through GPIO pin

        #sys.stdout.write( str(gpio_read_status) )
        #sys.stdout.flush()
        print( str(gpio_read_status) )
        BUG(' -> GPIO16 Status: {}\n'.format(gpio_read_status))

        data = ''
        while True:
            res = select.select([sys.stdin], [], [], 0)
            if not res[0]:
                break
            # data = data+sys.stdin.read(1) # restore all data
            data = sys.stdin.read(1) # only show latest data

        BUG(f'received data {data}')

        if '0' == data:
            set_gpio_write(0)
            BUG('reset GPIO17')
        if '1' == data:
            set_gpio_write(1)
            BUG('set GPIO17 HIGH')

        
        utime.sleep(REFRESH_PERIOD)

if __name__ == "__main__":
    main()
