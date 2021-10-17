import matplotlib.pyplot as plt
import numpy as np
import module.func as gf

plt.figure()
for i in range(10,80,10):
    plt.plot(np.arange(0.2,0.85,0.05), gf.calore_specifico(i))
plt.show()
