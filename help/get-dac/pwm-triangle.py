import pwm_dac as pd
import signal_generator as sg 
import time

amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000

try:
    gpio_pin = 12
    dac = pd.PWM_DAC(gpio_pin, pwm_frequency=5000, dynamic_range=3.3)

    t = time.time()

    while True:
        current_time = time.time() - t
        normalized_value = sg.get_triangle_wave_amplitude(signal_frequency, current_time)
        voltage = normalized_value*amplitude
        dac.set_voltage(voltage)
        sg.wait_for_sampling_period(sampling_frequency)


except KeyboardInterrupt:
    print("\nГенерация остановлена пользователем.")
finally:
    dac.deinit()