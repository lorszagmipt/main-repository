import mcp3021_driver as mcp
import adc_plot as plt
import time

duration=10.0
time_values=[]
voltage_values=[]
sampling_periods=[]

try:
    mcp3021=mcp.MCP3021(5.2)
    start_time=time.perf_counter()

    while (time.perf_counter() - start_time < duration):
        curr_time=time.perf_counter()
        voltage_values.append(mcp3021.get_voltage())
        time_values.append(time.perf_counter()-start_time)
        sampling_periods.append(time.perf_counter()-curr_time)
        time.sleep(0.0001)
    plt.plot_voltage_vs_time(time_values, voltage_values, max(voltage_values))
    plt.plot_sampling_period_hist(sampling_periods)
finally:
    mcp3021.deinit()