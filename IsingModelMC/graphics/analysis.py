import statistics
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import module.func as fnc
import model.costants as c

flag = c.FLAG
latt_dim_start = c.LATT_DIM_START
latt_dim_stop = c.LATT_DIM_STOP
passo_latt_dim = c.PASSO_LATT_DIM
i_decorrel = c.IDECORREL
measures = c.MEASURES
extfield = c.EXTFIELD
beta_start = c.BETA_START
beta_stop = c.BETA_STOP
passo_beta = c.PASSO_BETA

monte_history_m = False
monte_history_e = False
mean = False
chi = False
heat = False
binder = False

# passo montecarlo per la magnetizzazione a fissati beta
if monte_history_m == True:
    beta_num = 0.450
    plt.figure()
    for i in range(latt_dim_start, latt_dim_stop, passo_latt_dim):
        magnetization = np.loadtxt(f"results/lattice_dim_{i}/magnetization/magnetization_beta_{beta_num}.txt")
        plt.plot(np.arange(0,100000), magnetization)
    plt.show()

# passo montecarlo per l'energia a fissati beta
if monte_history_e == True:
    beta_num = 0.450
    plt.figure()
    for i in range(latt_dim_start, latt_dim_stop, passo_latt_dim):
        energy = np.loadtxt(f"results/lattice_dim_{i}/energies/energies_beta_{beta_num}.txt")
        plt.plot(np.arange(0,100000), energy)
    plt.show()

# grafico magnetizzazione media al variare di beta e L
if mean == True:
    plt.figure()
    # for i in range(latt_dim_start, latt_dim_stop, passo_latt_dim):
    mean, bet = fnc.mean_magnetization(10)
    # plt.plot(bet, mean)
    error = np.loadtxt("results/lattice_dim_10/error_magnetization.txt")
    plt.errorbar(bet, mean, yerr=error)
    plt.show()

# grafico suscettività al variare di beta ed L
if chi == True:
    plt.figure()
    for i in range(latt_dim_start, latt_dim_stop, passo_latt_dim):
        bet = np.loadtxt("results_analysis/beta/beta_lattice_dim_10.txt")
        chi = np.loadtxt(f"results_analysis/suscettività/suscettività_lattice_dim_{i}.txt")
        plt.scatter(bet, chi)
    plt.show()

# grafico calore specifico al variare di beta ed L
if heat == True:
    plt.figure()
    for i in range(latt_dim_start, latt_dim_stop, passo_latt_dim):
        speci_heat, bet = fnc.specific_heat(i)
        plt.scatter(bet, speci_heat)
    plt.show()

# grafico binder al variare di beta ed L
if binder == True:
    plt.figure()
    bet = np.loadtxt("results_analysis/binder/beta_range_0.34_0.48.txt")
    for i in range(latt_dim_start, latt_dim_stop, passo_latt_dim):
        bin = np.loadtxt(f"results_analysis/binder/binder_lattice_dim_{i}.txt")
        plt.scatter(bet, bin, s=0.4)
    plt.show()

# a = np.loadtxt("results/lattice_dim_60/magnetization/magnetization_beta_0.400.txt")
# a2 = np.loadtxt("results/lattice_dim_60/magnetization/magnetization_beta_0.450.txt")
# plt.hist(a, density=True, bins=50, label="beta=0.45")
# plt.hist(a2, density=True, bins=50, label="beta=0.40")
# plt.ylabel('Probability')
# plt.xlabel('Magnetization')
# plt.title("Histogram");
# plt.show()
