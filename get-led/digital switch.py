import RPi.GPIO as GPIO
import time
state = 0
GPIO.setmode(GPIO.BCM)
led = 26
GPIO.setup(led, GPIO.OUT)
button = 13
GPIO.setup(button, GPIO.IN)
while True:
    if GPIO.input(button):
        state = 1 - state
        GPIO.output(led, state)
        time.sleep(0.2)