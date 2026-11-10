import mcp3021_driver as mcp
import plot_weld as plt
import time
import RPi.GPIO as GPIO
import numpy as np

duration = 120.0             # продолжительность измерений, с
charge_time = duration / 2   # первые 60 с зарядка, следующие 60 с разрядка
time_values = []
voltage_values = []
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)

try:
    mcp3021 = mcp.MCP3021(5.2)

    # перед измерением разряжаем конденсатор
    GPIO.output(14, 0)
    print("Разряжаю конденсатор...")
    wait_start = time.perf_counter()
    while mcp3021.get_voltage() > 0.05 and time.perf_counter() - wait_start < 60:
        time.sleep(0.1)
    print("Начинаю измерения")

    GPIO.output(14, 1)
    start_time = time.perf_counter()
    while time.perf_counter() - start_time < duration:
        if time.perf_counter() - start_time >= charge_time:
            GPIO.output(14, 0)
        voltage_values.append(mcp3021.get_voltage())
        time_values.append(time.perf_counter() - start_time)

    data = np.column_stack((time_values, voltage_values))
    np.savetxt("data.csv",
               data,
               delimiter=",",
               fmt="%.4f",
               header="Время[с],Напряжение[В]",
               comments="",
               encoding="utf-8")
    print(f"Сохранено {len(time_values)} измерений в data.csv")

    plt.plot_voltage_vs_time(time_values, voltage_values, max(voltage_values))
    plt.plot_sampling_period_hist(time_values)
finally:
    GPIO.output(14, 0)
    GPIO.cleanup()
    mcp3021.deinit()
