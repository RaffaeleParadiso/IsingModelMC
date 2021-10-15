import statistics
import numpy as np
import matplotlib.pyplot as plt


def susceptivity(dim):
    chi = []
    for i in np.arange(20,85,5):
        magnetization = np.loadtxt(f"results\lattice_dim_{dim}\magnetization_beta_0.{i}0.txt")
        media = statistics.mean(magnetization**2)
        absulute = np.abs(magnetization)
        ab = statistics.mean(absulute)
        s = (dim**2)*((media)-(ab**2))*(i/100)
        chi.append(s)
    return chi


def ma(dim):
    magn = []
    for i in np.arange(20,85,5):
        magnetization = np.loadtxt(f"results\lattice_dim_{dim}\magnetization_beta_0.{i}0.txt")
        a = np.abs(magnetization)
        media = statistics.mean(a)
        magn.append(media)
    return magn

for i in range(10,80,10):
    ma10=ma(10)
    ma20=ma(20)
    ma30=ma(30)
    ma40=ma(40)
    ma50=ma(50)
    ma60=ma(60)
    ma70=ma(70)
    print(i)

ch10 = susceptivity(10)
ch20 = susceptivity(20)
ch30 = susceptivity(30)
ch40 = susceptivity(40)
ch50 = susceptivity(50)
ch60 = susceptivity(60)
ch70 = susceptivity(70)
# plt.figure()
# plt.plot(np.arange(0.20,0.85,0.05), ch10)
# plt.plot(np.arange(0.20,0.85,0.05), ch20)
# plt.plot(np.arange(0.20,0.85,0.05), ch30)
# plt.plot(np.arange(0.20,0.85,0.05), ch40)
# plt.plot(np.arange(0.20,0.85,0.05), ch50)
# plt.plot(np.arange(0.20,0.85,0.05), ch60)
# plt.plot(np.arange(0.20,0.85,0.05), ch70)
# plt.show()
