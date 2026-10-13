import pwm_dac as pwm
import signal_generator as sg

amplitude = 3.16
signal_frequency = 10
sampling_frequency = 1000
times=0.0

try:
    dac=pwm.PWM_DAC(12, 500, 3.16, True)

    while (True):
        signal=sg.get_sin_wave_amplitude(signal_frequency, times)
        sg.wait_for_sampling_period(sampling_frequency)
        times=times+(1/sampling_frequency)
        dac.set_voltage(amplitude*signal)
        continue
finally:
    dac.deinit()