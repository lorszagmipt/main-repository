import numpy as np
import matplotlib.pyplot as plt

dataPath = "wave/data/"
plotPath = "wave/plots/"
L = 1.00                                  # м, расстояние дверца — электроды (СВОЁ!)
g = 9.81                                  # м/с^2
heights = [20, 40, 60, 80, 100]           # мм, налитые уровни
degree = 3                                # степень калибровочного многочлена
autoTau = True                            # False — взять tauManual
tauManual = [2.15, 1.50, 1.06, 0.85, 1.16]   # с, найденные «глазами и руками»


def read(filename):
    """Файл: три строки шапки, пустая строка, затем по отсчёту в строке."""
    with open(filename) as f:
        lines = f.read().split("\n")
    duration = float(lines[2].split(":")[1].split()[0])
    samples = np.array([int(s) for s in lines[4:] if s.strip() != ""])
    return samples, duration, len(samples)


# ------------------------- п3.5 калибровка -------------------------
adcMeans = []
for h in heights:
    samples, duration, count = read(dataPath + "calibration/%d mm.txt" % h)
    adcMeans.append(np.mean(samples))
    print("%3d mm.txt  среднее %.0f, шум %.1f, частота %.0f Гц"
          % (h, np.mean(samples), np.std(samples), count / duration))

levels = np.array(heights) / 1000        # м
fit = np.polyfit(adcMeans, levels, degree)
minAdc, maxAdc = min(adcMeans), max(adcMeans)
dev = (np.polyval(fit, adcMeans) - levels) * 1000
print("Отклонения точек калибровки от многочлена, мм:", np.round(dev, 2))

x = np.linspace(minAdc, maxAdc, 200)
plt.figure(figsize=(7, 5))
plt.plot(x, np.polyval(fit, x) * 1000, label="многочлен степени %d" % degree)
plt.plot(adcMeans, heights, "o", label="калибровка")
plt.title("Калибровка датчика уровня")
plt.xlabel("отсчёт АЦП")
plt.ylabel("уровень воды, мм")
plt.grid(True)
plt.legend()
plt.savefig(plotPath + "height-calibration.png", dpi=150)
plt.close()


# ---------------------- п3.6 скорость волны ------------------------
def load(h):
    samples, duration, count = read(dataPath + "wave %d mm.txt" % h)
    level = np.polyval(fit, np.clip(samples, minAdc, maxAdc))   # м
    t = np.linspace(0, duration, count)                          # с
    return t, samples, level, count / duration


def two_lines(t, y):
    """Метод двух прямых по сглаженной кривой y(t) (отсчёты АЦП: они растут
    с уровнем и не обрезаются калибровкой). Горизонталь — среднее на 0,2–0,5 с,
    наклонная — прямая по первым 0,3 с спада; tau — точка их пересечения."""
    base = (t > 0.2) & (t < 0.5)
    a1 = np.mean(y[base])
    threshold = max(4 * np.std(y[base]), 3)       # отсчёты АЦП
    # начало спада — первая точка ниже порога, после которой кривая
    # уже не возвращается к исходному уровню (качание от рывка дверцы возвращается)
    low = y < a1 - threshold
    back = y > a1 - threshold / 2
    candidates = np.where(low & (t > 0.5))[0]
    for i in candidates:
        if not np.any(back[i:i + int(0.5 / (t[1] - t[0]))]):
            break
    t0 = t[i]
    part = (t >= t0) & (t <= t0 + 0.3)
    b2, a2 = np.polyfit(t[part], y[part], 1)      # y = a2 + b2 t
    return (a1 - a2) / b2


taus, speeds = [], []
for i, h in enumerate(heights):
    t, samples, level, rate = load(h)
    k = int(0.3 * rate)                            # отсчётов в 0,3 с: длиннее периода качания
    smooth = np.convolve(level, np.ones(k) / k, mode="same")
    smoothAdc = np.convolve(samples, np.ones(k) / k, mode="same")
    tau = two_lines(t, smoothAdc) if autoTau else tauManual[i]
    a1 = np.mean(smooth[(t > 0.2) & (t < 0.5)])
    c = L / tau
    taus.append(tau)
    speeds.append(c)

    plt.figure(figsize=(8, 5))
    edge = slice(k // 2, -k // 2)                  # края сглаживания искажены — не рисуем
    plt.plot(t[edge], smooth[edge] * 1000)
    plt.axhline(a1 * 1000, color="gray", linestyle=":")
    plt.axvline(tau, color="r", linestyle="--")
    text = "L = %.2f [м]\nτ = %.2f [с]\nc = %.2f [м/с]\n√(gh) = %.2f [м/с]" % (
        L, tau, c, np.sqrt(g * h / 1000))
    plt.text(0.97, 0.95, text, transform=plt.gca().transAxes, ha="right", va="top",
             bbox={"boxstyle": "round", "facecolor": "white", "alpha": 0.8})
    plt.xlim(0, min(t[-1], tau + 3))
    plt.ylim((a1 - 0.025) * 1000, (a1 + 0.004) * 1000)
    plt.title("wave %d mm" % h)
    plt.xlabel("время после открытия дверцы, с")
    plt.ylabel("уровень воды, мм")
    plt.grid(True)
    plt.savefig(plotPath + "wave %d mm.png" % h, dpi=150)
    plt.close()

print("\nГлубина, мм   tau, с   c, м/с   √(gh), м/с   расхождение")
for h, tau, c in zip(heights, taus, speeds):
    ct = np.sqrt(g * h / 1000)
    print("%8d     %5.2f    %5.2f     %5.2f      %+4.0f %%" % (h, tau, c, ct, (c / ct - 1) * 100))

# --------------------- сравнение с теорией -------------------------
hh = np.linspace(0, 0.12, 200)
plt.figure(figsize=(7, 5))
plt.plot(hh * 1000, np.sqrt(g * hh), label="теория c = √(gh)")
plt.plot(heights, speeds, "o", label="опыт")
plt.xlabel("глубина, мм")
plt.ylabel("скорость волны, м/с")
plt.grid(True)
plt.legend()
plt.savefig(plotPath + "speed-vs-depth.png", dpi=150)
plt.close()

lnh = np.log(np.array(heights) / 1000)
lnc = np.log(speeds)
(p, cov) = np.polyfit(lnh, lnc, 1, cov=True)
slope, intercept = p
dslope, dintercept = np.sqrt(np.diag(cov))
print("Наклон: %.2f ± %.2f (теория 0.5)" % (slope, dslope))
print("Свободный член: %.2f ± %.2f (теория %.2f)" % (intercept, dintercept, 0.5 * np.log(g)))

x = np.linspace(lnh.min() - 0.2, lnh.max() + 0.2, 10)
plt.figure(figsize=(7, 5))
plt.plot(lnh, lnc, "o", label="опыт")
plt.plot(x, slope * x + intercept, label="МНК: наклон %.2f ± %.2f" % (slope, dslope))
plt.plot(x, 0.5 * x + 0.5 * np.log(g), "--", label="теория: наклон 0,5")
plt.xlabel("ln h  (h в метрах)")
plt.ylabel("ln c  (c в м/с)")
plt.grid(True)
plt.legend()
plt.savefig(plotPath + "log-check.png", dpi=150)
plt.close()
