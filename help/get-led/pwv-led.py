import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)
led = 26
gpio.setup(led, gpio.OUT)
pwm = gpio.PWM(led, 200)
duty = 0.0
pwm.start(duty)

while True:
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.05)

    duty += 1.0
    if duty > 100.0:
        duty = 0.0