import mcp4725_driver as mcp
import signal_generator as sg


amplitude = 5.2
signal_frequency = 10
sampling_frequency = 1000
times=0.0

try:
    mcp4725=mcp.MCP4725(5.2)
    while True:
        signal=sg.get_sin_wave_amplitude(signal_frequency, times)
        sg.wait_for_sampling_period(sampling_frequency)
        times=times+(1/sampling_frequency)
        mcp4725.set_voltage(amplitude*signal)
        continue
finally:
    mcp4725.deinit()