import os
import statistics
import numpy as np
import matplotlib.pyplot as plt
import makedir as mk
from makedir import go_up

path = mk.go_up(1)
def susceptivity(dim_latt):
    chi = []
    for element in os.listdir(path+f"//results/lattice_dim_{dim_latt}/magnetization"):
        file_ = os.path.join(path+f"//results/lattice_dim_{dim_latt}/magnetization", element)
        beta = float(element[19:24])
        magnetization = np.loadtxt(file_)
        media = statistics.mean(magnetization**2)
        absolute = np.abs(magnetization)
        absolutesquared = statistics.mean(absolute)
        s = (dim_latt**2)*((media)-(absolutesquared**2))*(beta/100)
        chi.append(s)
    return chi

def mean_magnetization(dim_latt):
    mean_m = []
    for i in np.arange(20,85,5):
        magnetization = np.loadtxt(f"results\lattice_dim_latt_{dim_latt}\magnetization_beta_0.{i}0.txt")
        a = np.abs(magnetization)
        media = statistics.mean(a)
        mean_m.append(media)
    return mean_m

def specific_heat(dim_latt):
    s_heat = []
    for i in np.arange(20,85,5):
        energy = np.loadtxt(f"results\lattice_dim_latt_{dim_latt}\energies_beta_0.{i}0.txt")
        var_energy = statistics.pvariance(energy)
        s_heat.append((dim_latt**2)*var_energy)
    return s_heat


a = susceptivity(10)