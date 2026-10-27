import time
import RPi.GPIO as gpio

class R2R_ADC:
    def __init__ (self, dynamic_range, compare_time = 0.01, verbose = False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time

        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        gpio.setmode(gpio.BCM)
        gpio.setup(self.bits_gpio, gpio.OUT, initial = 0)
        gpio.setup(self.comp_gpio, gpio.IN)

    def deinit(self):
        gpio.output(self.bits_gpio, 0)
        gpio.cleanup()

    def number_to_dac(self, number):
        number = [int(i) for i in bin(number)[2:].zfill(8)]
        gpio.output(self.bits_gpio, number)

    def sequential_counting_adc(self):
        max_number = 2**len(self.bits_gpio)-1
        for number in range(max_number+1):
            self.number_to_dac(number)
            time.sleep(self.compare_time)

            if gpio.input(self.comp_gpio) == 1:
                return number
        return max_number

    def get_sc_voltage(self):
        number = self.sequential_counting_adc()
        voltage = number / (2**len(self.bits_gpio)-1) * self.dynamic_range
        if self.verbose:
            print(f"Число {number}, нарпяжение: {voltage:.3f} В")
        return voltage

    def successive_approximation_adc(self):
        number = 0

        for bit in range(len(self.bits_gpio) -1, -1, -1):
            number |= 1 << bit
            self.number_to_dac(number)
            time.sleep(self.compare_time)

            if gpio.input(self.comp_gpio) == 1:
                number &= ~(1 << bit)

        return number

    def get_sar_voltage(self):
        number = self.successive_approximation_adc()
        voltage = number / (2**len(self.bits_gpio)-1) * self.dynamic_range
        if self.verbose:
            print(f"Число {number}, нарпяжение: {voltage:.3f} В")
        return voltage

        
if __name__ == "__main__":
    try:
        adc = R2R_ADC(3.3, verbose=True)
        while True:
                adc.get_sar_voltage()
                time.sleep(0.1)
    finally:
        adc.deinit()