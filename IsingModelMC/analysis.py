import statistics
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import module.func as fnc
import model.costants as c
#==========================================================
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
#==========================================================
monte_history_m = False
monte_history_e = False
mean = True
chi = False
heat = False
#==========================================================
# passo montecarlo per la magnetizzazione a fissati beta
if monte_history_m == True:
    beta_num = 0.450
    plt.figure()
    for i in range(latt_dim_start, latt_dim_stop, passo_latt_dim):
        magnetization = np.loadtxt(f"results/lattice_dim_{i}/magnetization/magnetization_beta_{beta_num}.txt")
        plt.plot(np.arange(0,100000), magnetization)
    plt.show()
#==========================================================
# passo montecarlo per l'energia a fissati beta
if monte_history_e == True:
    beta_num = 0.450
    plt.figure()
    for i in range(latt_dim_start, latt_dim_stop, passo_latt_dim):
        energy = np.loadtxt(f"results/lattice_dim_{i}/energies/energies_beta_{beta_num}.txt")
        plt.plot(np.arange(0,100000), energy)
    plt.show()
#==========================================================
# grafico magnetizzazione media al variare di beta e L
if mean == True:
    plt.figure()
    # for i in range(latt_dim_start, latt_dim_stop, passo_latt_dim):
    mean, bet = fnc.mean_magnetization(10)
    # plt.plot(bet, mean)
    error = np.loadtxt("results/lattice_dim_10/error_magnetization.txt")
    plt.errorbar(bet, mean, yerr=error)
    plt.show()
#==========================================================
# grafico suscettività al variare di beta ed L
if chi == True:
    plt.figure()
    for i in range(latt_dim_start, latt_dim_stop, passo_latt_dim):
        chi, bet = fnc.susceptivity(i)
        plt.scatter(bet, chi)
    plt.show()
#==========================================================
# grafico calore specifico al variare di beta ed L
if heat == True:
    plt.figure()
    for i in range(latt_dim_start, latt_dim_stop, passo_latt_dim):
        speci_heat, bet = fnc.specific_heat(i)
        plt.scatter(bet, speci_heat)
    plt.show()
#==========================================================







# max_index = s1.index(max(s1))
# bet1 = np.array(bet1)
# print(bet1[max_index])
# print(bet1)
# bet1 = bet1 - (bet1[max_index])
# print(bet1)

# s6 = np.log(s1)
# bet6 = np.abs(bet1)
# bet6 = np.log(bet6)

# print(s6)
# print(bet6)



#FINITE SIZE SCALING PER CALORE SPECIFICO E SUSCETTIVITà MAGNETICA





# plt.figure()
# for i in range(10,80,10):
#     plt.plot(np.arange(0.2,0.85,0.05), fnc.calore_specifico(i))
# plt.show()

# def binder(vec):
#     '''Calculates binder cumulant'''
#     binder = []
#     for i in vec:
#         m2 = i**2
#         m4 = i**4
#         binder.append(m4/m2**2)
#     return binder

# def binderCumulant(x) :
#     x2 = statistics.mean(x**2)
#     x4 = statistics.mean(x**4)
#     return 1 - (x4/(x2**2))

# a = np.loadtxt("results/lattice_dim_60/magnetization/magnetization_beta_0.400.txt")
# a2 = np.loadtxt("results/lattice_dim_60/magnetization/magnetization_beta_0.450.txt")

# plt.hist(a, density=True, bins=50, label="beta=0.45")
# plt.hist(a2, density=True, bins=50, label="beta=0.40")
# plt.ylabel('Probability')
# plt.xlabel('Magnetization')
# plt.title("Histogram");
# plt.show()




