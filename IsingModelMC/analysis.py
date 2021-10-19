import statistics
import matplotlib.pyplot as plt
import numpy as np
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



sus, bet = fnc.susceptivity(10)

plt.figure()
plt.scatter(bet, sus)
plt.show()





















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




