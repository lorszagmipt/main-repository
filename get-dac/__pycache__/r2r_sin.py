import r2r_dac as r2r
import signal_generator as sg
import time

amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000
times=0.0

if __name__ == "__main__":
    try:
        dac=r2r.R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.2, True)

        while (True):
            signal=sg.get_sin_wave_amplitude(signal_frequency, times)
            sg.wait_for_sampling_period(sampling_frequency)
            times=times+(1/sampling_frequency)
            dac.set_voltage(amplitude*signal)
            continue
    finally:
        dac.deinit()