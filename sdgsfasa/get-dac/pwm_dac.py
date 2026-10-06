import RPi.GPIO as GPIO

class PWM_DAC:
    def __init__(self, gpio_pin, pwm_frequency, dynamic_range, verbose = False):
        self.gpio_pin=gpio_pin
        self.dynamic_range=dynamic_range
        self.verbose=verbose
        self.frequency=pwm_frequency

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT, initial = 0)

        self.pwm=GPIO.PWM(self.gpio_pin, self.frequency)
        


    def deinit(self):
        self.pwm.stop()
        GPIO.cleanup()

    def set_number(self, number):
        duty=number * 100
        self.pwm.start(duty)
        print(f"Коэффициент заполнения: {duty:2f}")
    
    def set_voltage(self, voltage):
        if not (0.0<=voltage<=self.dynamic_range):
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {self.dynamic_range:.2f} В)")
            print ("Устанавливаем 0.0 В")
            voltage=0
        self.set_number(voltage/self.dynamic_range)

if __name__ == "__main__":
    try:
        dac = PWM_DAC(12, 500, 3.16, True)

        while True:
            try:
                voltage = float((input("Введите напряжение в Вольтах:")))
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте еще раз\n")

    finally:
        dac.deinit()