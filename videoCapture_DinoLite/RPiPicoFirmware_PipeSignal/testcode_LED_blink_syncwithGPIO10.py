# hello_world.py

# Import the machine module
import machine

# Import the time module for delays
import time

# Define the onboard LED pin (usually GPIO 25)
led = machine.Pin(25, machine.Pin.OUT)
t22 = machine.Pin(10, machine.Pin.OUT)
ttt = machine.Pin( 8, machine.Pin.OUT)

def set_val(v):
    led.value(v)
    ttt.value(v)
    t22.value(v)

# Print "Hello, World!" to the serial console
print("Hello, World!")

# Blink the onboard LED as a visual indicator
while True:
    set_val(1)
    time.sleep(1.0)  # Delay for 1 second
    set_val(0)
    time.sleep(0.7)  # Delay for 1 second
