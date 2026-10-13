import numpy as np
import time

def get_tri_wave_amplitude(freq, time):
    return (0.5+(np.arcsin(np.sin(2*np.pi*freq*time)))/np.pi)

def wait_for_sampling_period(sampling_frequency):
    dt=1/sampling_frequency
    time.sleep(dt)