import RPi.GPIO as gpio

class PWM_DAC:
    def __init__(self, gpio_pin, pwm_frequency, dynamic_range, verobse = False):
        self.gpio_pin = gpio_pin
        self.dynamic_range = dynamic_range
        self.verbose = verobse
        self.pwm_frequency = pwm_frequency

        gpio.setmode(gpio.BCM)
        gpio.setup(self.gpio_pin, gpio.OUT, initial = 0)

        self.pwm = gpio.PWM(self.gpio_pin, self.pwm_frequency)
        self.pwm.start(0)
    def deinit(self):
        gpio.output(self.gpio_pin, 0)
        gpio.cleanup()
    
    def set_voltage(self, voltage):
        if voltage < 0 or voltage > self.dynamic_range:
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {self.dynamic_range:.2f} В)")
            return

        duty = (voltage/self.dynamic_range) * 100.0

        self.pwm.ChangeDutyCycle(duty)

if __name__ == "__main__":
    try:
        dac = PWM_DAC(12, 500, 3.290, True)

        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте еще раз\n")
    
    finally:
        dac.deinit()