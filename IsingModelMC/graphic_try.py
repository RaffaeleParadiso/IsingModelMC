import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path
import module.func as fnc

susc10=np.loadtxt('results_analysis/suscettività_riscalata/dim_10_suscettività_rescaled.txt')
susc20=np.loadtxt('results_analysis/suscettività_riscalata/dim_20_suscettività_rescaled.txt')

mean10=np.loadtxt('results_analysis/magnetizzazione_riscalata/dim_10_magn_rescaled.txt')
mean20=np.loadtxt('results_analysis/magnetizzazione_riscalata/dim_20_magn_rescaled.txt')

beta_resc10=np.loadtxt('results_analysis/beta_riscalato/dim_10_beta_rescaled.txt')
beta_resc20=np.loadtxt('results_analysis/beta_riscalato/dim_20_beta_rescaled.txt')

# a, bet = fnc.mean_magnetization(10)
# b, bet= fnc.mean_magnetization(20)

plt.figure()
plt.scatter(beta_resc10, mean10, s=0.5)
plt.scatter(beta_resc20, mean20, s=0.5)
# plt.scatter(beta_resc20, mean20, s=0.5)
plt.show()

print(len(mean10), len(mean20))

differenza=np.array(susc10)-np.array(susc20)

for ii in range(len(differenza)):
    if differenza[ii]>=0.0001:
      print(differenza[ii])

print(np.mean(differenza))
print(np.mean(differenza[140::]))
print(np.mean(differenza[0:140]))

