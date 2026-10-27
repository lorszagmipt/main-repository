import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)
leds = [24, 22, 23, 27, 17, 25, 12, 16]
gpio.setup(leds, gpio.OUT)

gpio.output(leds, 0)
light_time = 0.2

while True:
    for led in leds:
        gpio.output(led, 1)
        time.sleep(light_time)
        gpio.output(led, 0)
    for led in reversed(leds):
        gpio.output(led, 1)
        time.sleep(light_time)
        gpio.output(led, 0)