import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)
led = 26
gpio.setup(led, gpio.OUT)
phototranz = 6
gpio.setup(phototranz, gpio.IN)
state = 0

while True:
    if not gpio.input(phototranz):
        state = not state
        gpio.output(led, state)
