import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)
led = 26
gpio.setup(led, gpio.OUT)
button = 13
gpio.setup(button, gpio.IN)
state = 0

while True:
    if gpio.input(button):
        state = not state
        gpio.output(led, state)
        time.sleep(0.2)