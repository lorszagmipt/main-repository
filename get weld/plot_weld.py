import matplotlib.pyplot as plt
import numpy as np


def plot_voltage_vs_time(time, voltage, max_voltage):
    plt.figure(figsize=(10, 6))
    plt.plot(time, voltage)
    plt.title("График зависимости напряжения на конденсаторе от времени")
    plt.xlabel("Время, с")
    plt.ylabel("Напряжение, В")
    plt.xlim(0, max(time))
    plt.ylim(0, max_voltage * 1.1)
    plt.grid(True)
    plt.savefig("rc-plot.png", dpi=300)
    plt.show()


def plot_sampling_period_hist(time):
    sampling_periods = []
    for i in range(1, len(time)):
        sampling_periods.append(time[i] - time[i - 1])
    plt.figure(figsize=(10, 6))
    plt.hist(sampling_periods, bins=50, range=(0, 0.003))
    plt.title("Распределение количества измерений по их продолжительности")
    plt.xlabel("Период измерения, с")
    plt.ylabel("Количество измерений")
    plt.xlim(0, 0.003)
    plt.grid(True)
    plt.show()


def find_tau(time, voltage, charge_time):
    time = np.array(time)
    voltage = np.array(voltage)
    # сглаживаем шум АЦП: скользящее среднее по 50 точкам
    smooth = np.convolve(voltage, np.ones(50) / 50, mode="same")

    charging = time < charge_time
    discharging = time >= charge_time

    # зарядка: за время τ напряжение доходит до 63 % от установившегося
    u_inf = np.mean(voltage[charging][-1000:])
    level_63 = 0.632 * u_inf
    tau_charge = time[charging][np.argmax(smooth[charging] >= level_63)]

    # разрядка: за время τ напряжение падает до 37 % от начального
    u_0 = np.mean(voltage[charging][-100:])
    level_37 = 0.368 * u_0
    discharge_time = time[discharging] - charge_time
    tau_discharge = discharge_time[np.argmax(smooth[discharging] <= level_37)]

    return tau_charge, tau_discharge, u_inf, u_0


if __name__ == "__main__":
    charge_time = 60.0   # как в mcp-weld.py: duration / 2
    R = 1e6              # резистор R1: 1 МОм
    C = 10e-6            # конденсатор C1: 10 мкФ

    data = np.loadtxt("data.csv",
                      delimiter=",",
                      skiprows=1,
                      encoding="utf-8")
    time = data[:, 0].astype(float)
    voltage = data[:, 1].astype(float)

    tau_charge, tau_discharge, u_inf, u_0 = find_tau(time, voltage, charge_time)
    tau = (tau_charge + tau_discharge) / 2
    print(f"Установившееся напряжение при зарядке: {u_inf:.3f} В")
    print(f"Напряжение в начале разрядки: {u_0:.3f} В")
    print(f"τ по зарядке (63 %): {tau_charge:.2f} с")
    print(f"τ по разрядке (37 %): {tau_discharge:.2f} с")
    print(f"Среднее: τ = {tau:.2f} с")
    print(f"Номинал: τ = RC = {R * C:.1f} с, отличие {(tau - R * C) / (R * C) * 100:+.1f} %")

    plot_voltage_vs_time(time, voltage, max(voltage))
