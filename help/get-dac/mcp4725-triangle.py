import time
import mcp4725_driver as mcp
import signal_generator as sg

amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000

try:
    mcp = mcp.mcp4725(dynamic_range=5.0)
    t = time.time()

    while True:
        current_time = time.time() - t
        normalized_value = sg.get_triangle_wave_amplitude(signal_frequency, current_time)
        voltage = normalized_value*amplitude
        mcp.set_voltage(voltage, )
        sg.wait_for_sampling_period(sampling_frequency)

except KeyboardInterrupt:
    print("\nГенерация остановлена пользователем.")
finally:
    mcp.deinit()