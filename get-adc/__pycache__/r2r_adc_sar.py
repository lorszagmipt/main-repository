import RPi.GPIO as GPIO
import time

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time=0.01, verbose = False):
        self.dynamic_range=dynamic_range
        self.verbose=verbose
        self.compare_time=compare_time

        self.bits_gpio=[26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio=21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def deinit(self):
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()

    def number_to_dac(self, number):
        signal= [int(element) for element in bin(number)[2:].zfill(8)]
        GPIO.output(self.bits_gpio, signal)

    def sequential_counting_adc(self):
        for value in range(255):
            self.number_to_dac(value)
            voltage= value / 255 * self.dynamic_range
            time.sleep(self.compare_time)
            comparatorValue=GPIO.input(self.comp_gpio)
            if comparatorValue == 1:
                break
        
        return voltage
        
    def get_sc_voltage(self):
        return (self.sequential_counting_adc())

    def successive_approximation_adc(self):
        low=0
        high=255
        while(low<=high):
            mid=(low+high)//2
            self.number_to_dac(mid)
            if(GPIO.input(self.comp_gpio)==0):
                result=mid
                high=mid-1
                
            else:
                result=mid
                low=mid+1
        return result

    def get_sar_voltage(self):
        return (self.get_sc_voltage() / 255 * 79.5 * self.dynamic_range)

if __name__=="__main__":
    try:
        adc = R2R_ADC(3.22, 0.001, True)
        while True:
            voltage=adc.get_sar_voltage()
            print(f"Напряжение: {voltage:.2f} В")
    finally:
        adc.deinit()