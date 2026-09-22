import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
state = 0
led = 26
GPIO.setup(led, GPIO.OUT)
sun = 6
GPIO.setup(sun, GPIO.IN)
while True:
    if GPIO.input(sun):
        GPIO.output(led, 0)
    else:
        GPIO.output(led, 1)

        