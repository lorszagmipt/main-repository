import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)
leds = [24, 22, 23, 27, 17, 25, 12, 16]
gpio.setup(leds, gpio.OUT)

gpio.output(leds, 0)

up = 9
down = 10
gpio.setup(up, gpio.IN)
gpio.setup(down, gpio.IN)
num = 0

def dec2bin(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]

sleep_time = 0.2
while True:
    if gpio.input(up):
        num = num + 1
        if num < 0:
            num = 0
            print("Достигнуто мин. значение")
        elif num > 256:
            num = 0
            print("Первышено макс. значение")
        print(num ,dec2bin(num))
        time.sleep(sleep_time)
    if gpio.input(down):
        num = num - 1
        if num < 0:
            num = 0
            print("Достигнуто мин. значение")
        elif num > 256:
            num = 0
            print("Первышено макс. значение")
        print(num ,dec2bin(num))
        time.sleep(sleep_time)
    gpio.output(leds, dec2bin(num))