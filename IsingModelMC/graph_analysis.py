import numpy as np
import statistics

mag = []

for i in np.arange(38,48,1):
    a = np.loadtxt(f"results\magnetization_1_40_0.{i}.txt")
    mean = abs(a)
    mean = statistics.mean(mean)
    mag.append(mean)


print((mag))

import matplotlib.pyplot as plt

plt.figure()
plt.plot(np.arange(0.38,0.48,0.01), mag)
plt.show()