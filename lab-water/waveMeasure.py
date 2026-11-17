import time
import RPi.GPIO as GPIO
from mcp3021_driver import MCP3021
import csv

duration = 15                        # секунд записи (калибровка: 10)
waitDoor = True                      # False — для калибровки
filename = "data-wave-120mm.csv"     # калибровка: "data/calibration/60 mm.txt"

doorPin = 15
closedLevel = 1                      # дверца закрыта — на входе 1


def save(samples, times, filename):
    with open(filename, "w", newline="") as outfile:
        writer=csv.writer(outfile, delimeter=" ")
        for sample, time1 in zip(samples, times):
            writer.writerow([time1, sample])


adc = MCP3021(5.0)
GPIO.setmode(GPIO.BCM)
GPIO.setup(doorPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
    if waitDoor:
        print("Ждём открытия дверцы...")
        while GPIO.input(doorPin) == closedLevel:
            pass
    else:
        print("Запись без ожидания дверцы")

    samples = []
    times=[]
    start = time.perf_counter()
    while time.perf_counter() - start < duration:
        samples.append(adc.get_number())
        times.append(time.perf_counter() - start)
    finish = time.perf_counter()

    print("Отсчётов: {}, частота {:.0f} Гц".format(len(samples), len(samples) / (finish - start)))
    with open(filename, "w", newline="") as file:
        writer=csv.writer(file, delimiter=" ")
        for sample, time1 in zip(samples, times):
            writer.writerow([time1, sample])
    print("Сохранено в", filename)
finally:
    adc.deinit()
    GPIO.cleanup()
