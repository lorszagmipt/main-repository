import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import time
leds = [16, 12, 25, 17, 27, 23, 22, 24]
GPIO.setup(leds, GPIO.OUT)
GPIO.output(leds, [0,0,0,0,0,0,0,0])

up = 9
down = 10

GPIO.setup(up, GPIO.IN)
GPIO.setup(down, GPIO.IN)
num = 0

def dec2bin(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]
sleep_time = 0.2

while True:
    if GPIO.input(up):
        if num < 255:
            num = num + 1
            print(num, dec2bin(num))
            time.sleep(sleep_time)

    if GPIO.input(down):
        if num > 0:
            num = num - 1
            print(num, dec2bin(num))
            time.sleep(sleep_time)
        

    GPIO.output(leds, dec2bin(num))
    time.sleep(0.1)