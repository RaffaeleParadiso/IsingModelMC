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

# passo montecarlo per la magnetizzazione a fissati beta e L

# plt.figure()
# a = np.loadtxt("results/lattice_dim_60/magnetization/magnetization_beta_0.450.txt")
# plt.plot(np.arange(1,100001), a)

# grafico magnetizzazione media al variare di beta e L

# a1, bet1 = fnc.mean_magnetization(10)
# a2, bet2 = fnc.mean_magnetization(20)
# a3, bet3 = fnc.mean_magnetization(30)
# a4, bet4 = fnc.mean_magnetization(40)
# a5, bet5 = fnc.mean_magnetization(50)
# a6, bet6 = fnc.mean_magnetization(60)

# grafico suscettività al variare di beta ed L

# s1, bet1 = fnc.susceptivity(10)
# s2, bet2 = fnc.susceptivity(20)
# s3, bet3 = fnc.susceptivity(30)
# s4, bet4 = fnc.susceptivity(40)
# s5, bet5 = fnc.susceptivity(50)
s1, bet1 = fnc.susceptivity(60)
max_index = s1.index(max(s1))
bet1 = np.array(bet1)
print(bet1[max_index])
print(bet1)
bet1 = bet1 - (bet1[max_index])
print(bet1)

s6 = np.log(s1)
bet6 = np.abs(bet1)
bet6 = np.log(bet6)

print(s6)
print(bet6)
# # storia montecarlo energia media
# a, bet = fnc.specific_heat(10)

#FINITE SIZE SCALING PER CALORE SPECIFICO E SUSCETTIVITà MAGNETICA


# plt.scatter(bet1, s1)
# plt.scatter(bet2, s2)
# plt.scatter(bet3, s3)
# plt.scatter(bet4, s4)
# plt.show()


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




