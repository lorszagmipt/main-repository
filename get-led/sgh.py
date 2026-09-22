import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

led = 26
GPIO.setup(led, GPIO.OUT)

GPIO.output(led, 0)




