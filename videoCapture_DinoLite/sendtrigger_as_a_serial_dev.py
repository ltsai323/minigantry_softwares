import machine
import utime

# Initialize the UART (serial) interface
uart = machine.UART(0, baudrate=9600)


led = machine.Pin(25, machine.Pin.OUT)

# Print "Hello, World!" to the serial console
print("Hello, World!")

# Blink the onboard LED as a visual indicator

led_flag=False
while True:
    mesg=f'trigger {"ON" if led_flag else "OFF"}'
    print(f'writting mesg "{mesg}"')
    uart.write(f'{mesg}\n')  # Send trigger signal
    led.value(1 if led_flag else 0)
    utime.sleep( 1.0 if led_flag else 0.3 )
    led_flag = not led_flag