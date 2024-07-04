# hello_world.py

# Import the machine module
import machine

# Import the time module for delays
import time

# Define the onboard LED pin (usually GPIO 25)
led = machine.Pin(25, machine.Pin.OUT)

# Print "Hello, World!" to the serial console
print("Hello, World!")

# Blink the onboard LED as a visual indicator
while True:
    led.value(1)  # Turn the LED on
    time.sleep(0.2)  # Delay for 1 second
    led.value(0)  # Turn the LED off
    time.sleep(0.2)  # Delay for 1 second
