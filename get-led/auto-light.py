import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
state = 0
led = 26
GPIO.setup(led, GPIO.OUT)
sun = 6
GPIO.setup(sun, GPIO.IN)
while True:
    if GPIO.input(sun):
        state = 1 - state
        GPIO.output(led, state)