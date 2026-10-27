import time
import RPi.GPIO as gpio
import r2r_adc
import adc_plot

adc = r2r_adc.R2R_ADC(3.3, compare_time=0.0001, verbose=True)
voltage_values = []
time_values = []
duration = 5.0

try:q
    t_start = time.time()
    while (time.time() - t_start < duration):
        voltage_values.append(adc.get_sar_voltage())
        time_values.append(time.time()-t_start)
    adc_plot.plot_voltage_vs_time(time_values, voltage_values, 4, filename="sar-plot.png")
    adc_plot.plot_sampling_period_hist(time_values, filename="sar-hist.png")
finally:
    adc.deinit()
