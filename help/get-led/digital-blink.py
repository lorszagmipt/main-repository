import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)
led = 26
gpio.setup(led, gpio.OUT)
state = 0
period = 1.0
while True:
    gpio.output(led, state)
    state = not state
    time.sleep(period)
