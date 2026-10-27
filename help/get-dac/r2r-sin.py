import r2r_dac as r2r
import signal_generator as sg
import time

amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000

try:
    gpio_bits = [16, 20, 21, 25, 26, 17, 27, 22]
    dac = r2r.R2R_DAC(gpio_bits, dynamic_range=3.3, verobse=False)

    t =time.time()

    while True:
        t = time.time()-t
        normalized_value = sg.get_sin_wave_amplitude(signal_frequency, t)
        voltage = normalized_value*amplitude
        dac.set_voltage(voltage)
        sg.wait_for_sampling_period(sampling_frequency)
        

except KeyboardInterrupt:
    print("\nГенерация остановлена пользователем.")
finally:
    dac.deinit()
