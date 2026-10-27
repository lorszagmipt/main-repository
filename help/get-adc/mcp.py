import time
import RPi.GPIO as gpio
import mcp3021_driver
import adc_plot

dynamic_range = 5

mcp = mcp3021_driver.MCP3021(dynamic_range, verbose = True)
voltage_values = []
time_values = []
duration = 10.0

try:
    t_start = time.time()
    while (time.time() - t_start < duration):
        voltage_values.append(mcp.get_voltage())
        time_values.append(time.time()-t_start)
        time.sleep(0.001)
    adc_plot.plot_voltage_vs_time(time_values, voltage_values, dynamic_range, filename="mcp-plot.png")
    adc_plot.plot_sampling_period_hist(time_values, filename="mcp-hist.png")
finally:
    mcp.deinit()
