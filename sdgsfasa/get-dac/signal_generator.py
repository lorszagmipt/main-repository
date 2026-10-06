import numpy as np
import time

def get_sin_wave_amplitude(freq, time):
    return ((1+np.sin(2*np.pi*freq*time))/2)

def wait_for_sampling_period(sampling_frequency):
    dt=1/sampling_frequency
    time.sleep(dt)
