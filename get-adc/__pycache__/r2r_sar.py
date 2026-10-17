import r2r_adc_sar as r2r
import adc_plot as plt
import time

voltage_values=[]
time_values=[]
sampling_periods=[]
duration=3.0

try:
    adc=r2r.R2R_ADC(3.22, 0.0001, True)
    start_time=time.perf_counter()

    while (time.perf_counter() - start_time < duration):
        curr_time=time.perf_counter()
        voltage_values.append(adc.get_sar_voltage())
        time_values.append(time.perf_counter()-start_time)
        sampling_periods.append(time.perf_counter()-curr_time)
        time.sleep(0.0001)
    plt.plot_voltage_vs_time(time_values, voltage_values, max(voltage_values))
    plt.plot_sampling_period_hist(sampling_periods)
finally:
    adc.deinit()