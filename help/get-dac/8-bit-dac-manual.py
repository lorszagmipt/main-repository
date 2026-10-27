import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)
dac_bits = [16, 20, 21, 25, 26, 17, 27, 22]
gpio.setup(dac_bits, gpio.OUT)

dynamic_range = 3.3

def voltage_to_number(voltage):
    if not (0.0 <= voltage <= dynamic_range):
        print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {dynamic_range:.2f} В)")
        print("Устанавливаем 0.0 В")
        return 0
    return int(voltage / dynamic_range * 255)

def number_to_dac(number):
    bits = [int(element) for element in bin(number)[2:].zfill(8)]
    print(f"Число на вход ЦАП: {number}, биты: {bits}")
    for i in range(8):
        gpio.output(dac_bits[i], bits[i])


try:
    while True:
        try:
            voltage = float(input("Введите напряжение в Вольтах: "))
            number = voltage_to_number(voltage)
            number_to_dac(number)

        except ValueError:
            print("Вы ввели не число. Попробуйте еще раз\n")

finally:
    gpio.output(dac_bits, 0)
    gpio.cleanup()