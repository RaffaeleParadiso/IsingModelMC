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

def calore_specifico(dim):
    cs = []
    for i in np.arange(20,85,5):
        energy = np.loadtxt(f"results\lattice_dim_{dim}\energies_beta_0.{i}0.txt")
        var_energy = statistics.pvariance(energy)
        cs.append((dim**2)*var_energy)
    return cs

plt.figure()
for i in range(10,80,10):
    plt.plot(np.arange(0.2,0.85,0.05), calore_specifico(i))
plt.show()
