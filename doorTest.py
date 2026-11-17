import RPi.GPIO as GPIO
import time

doorPin = 15
closedLevel = 1          # дверца закрыта — на входе 1

GPIO.setmode(GPIO.BCM)
GPIO.setup(doorPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
    for i in range(5):
        print("Ждём открытия дверцы...")
        while GPIO.input(doorPin) == closedLevel:
            pass
        start = time.time()
        print(f"Дверца открыта! {time.strftime('%H:%M:%S')}")
        # ждём, пока дверцу закроют, чтобы поймать следующее открытие
        time.sleep(0.5)
        while GPIO.input(doorPin) != closedLevel:
            pass
        time.sleep(0.5)
finally:
    GPIO.cleanup()
