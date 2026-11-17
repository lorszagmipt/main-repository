import time
import RPi.GPIO as GPIO
from mcp3021_driver import MCP3021

duration = 15                        # секунд записи (калибровка: 10)
waitDoor = True                      # False — для калибровки
filename = "data/wave 60 mm.txt"     # калибровка: "data/calibration/60 mm.txt"

doorPin = 15
closedLevel = 1                      # дверца закрыта — на входе 1


def save(samples, start, finish, filename):
    with open(filename, "w") as outfile:
        outfile.write("- Wave Lab\n")
        outfile.write("- Date: {}\n".format(time.strftime("%Y-%m-%d %H:%M:%S")))
        outfile.write("- Duration: {:.2f} s\n\n".format(finish - start))
        for sample in samples:
            outfile.write("{}\n".format(sample))


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
    start = time.time()
    while time.time() - start < duration:
        samples.append(adc.get_number())
    finish = time.time()

    print("Отсчётов: {}, частота {:.0f} Гц".format(len(samples), len(samples) / (finish - start)))
    save(samples, start, finish, filename)
    print("Сохранено в", filename)
finally:
    adc.deinit()
    GPIO.cleanup()
