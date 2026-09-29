import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
pini = [16, 20, 21, 25, 26, 17, 27, 22]
GPIO.setup(pini, GPIO.OUT)
GPIO.output(pini, 0)
volt = 3.16

def voltage_to_number(voltage):
    if not (0.0 <= voltage <= volt):
        print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {volt:.2f} В)")
        print("Устанавлниваем 0.0 В")
        return 0

    return int(voltage / volt * 255)

def dec2(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]

try:
    while True:
        try:
            voltage = float(input("Введите напряжение в Вольтах: "))
            number = voltage_to_number(voltage)
            GPIO.output(pini, dec2(number))

        except ValueError:
            print("Вы ввели не число. Попробуйте ещё раз\n")

finally:
    GPIO.output(pini, 0)
    GPIO.cleanup()