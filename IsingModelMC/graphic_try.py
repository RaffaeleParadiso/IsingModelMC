from statistics import mean
import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path

from numpy.core.defchararray import count
import module.func as fnc

'''Si deve fare con un cazz di for'''

# for lattice1 in range(20, 50, 10):
#    for lattice in range(10, 20, 10):
#       lista_di_cose=[(np.loadtxt('results_analysis/suscettività_riscalata/dim_{lattice}_suscettività_rescaled.txt')), \
#       np.loadtxt('results_analysis/magnetizzazione_riscalata/dim_{lattice}_magn_rescaled.txt')\
#       (np.loadtxt('results_analysis/beta_riscalato/dim_{lattice}_beta_rescaled.txt')), lattice1]

#    lista_di_cose=[ii for ii in lista_di_cose]
  
spec_hat10=np.loadtxt('results_analysis/calore_specifico/dim_10_calore_specifico.txt')
spec_hat20=np.loadtxt('results_analysis/calore_specifico/dim_20_calore_specifico.txt')
spec_hat30=np.loadtxt('results_analysis/calore_specifico/dim_30_calore_specifico.txt')
spec_hat40=np.loadtxt('results_analysis/calore_specifico/dim_40_calore_specifico.txt')








susc10=np.loadtxt('results_analysis/suscettività_riscalata/dim_10_suscettività_rescaled.txt')
susc20=np.loadtxt('results_analysis/suscettività_riscalata/dim_20_suscettività_rescaled.txt')
susc30=np.loadtxt('results_analysis/suscettività_riscalata/dim_30_suscettività_rescaled.txt')
susc40=np.loadtxt('results_analysis/suscettività_riscalata/dim_40_suscettività_rescaled.txt')

mean10=np.loadtxt('results_analysis/magnetizzazione_riscalata/dim_10_magn_rescaled.txt')
mean20=np.loadtxt('results_analysis/magnetizzazione_riscalata/dim_20_magn_rescaled.txt')
mean30=np.loadtxt('results_analysis/magnetizzazione_riscalata/dim_30_magn_rescaled.txt')
mean40=np.loadtxt('results_analysis/magnetizzazione_riscalata/dim_40_magn_rescaled.txt')

beta_resc10=np.loadtxt('results_analysis/beta_riscalato/dim_10_beta_rescaled.txt')
beta_resc20=np.loadtxt('results_analysis/beta_riscalato/dim_20_beta_rescaled.txt')
beta_resc30=np.loadtxt('results_analysis/beta_riscalato/dim_30_beta_rescaled.txt')
beta_resc40=np.loadtxt('results_analysis/beta_riscalato/dim_40_beta_rescaled.txt')

# a, bet = fnc.mean_magnetization(10)
# b, bet= fnc.mean_magnetization(20)


beta1=plt.scatter(beta_resc10, susc10, s=10, marker='p')
beta2=plt.scatter(beta_resc20, susc20, s=10, marker='s')
beta3=plt.scatter(beta_resc30, susc30, s=10, marker='v')
beta4=plt.scatter(beta_resc40, susc40, s=10, marker='x')
plt.legend((beta1, beta2, beta3, beta4),('Sush 10','sush 20', 'sush 30', 'sush 40'), scatterpoints=1, loc='lower right', ncol=3, fontsize=10)
# plt.scatter(beta_resc20, mean20, s=0.5)
plt.show()

plt.figure()
plt.scatter(beta_resc10, mean10, s=0.5)
plt.scatter(beta_resc20, mean20, s=0.5)
plt.scatter(beta_resc30, mean30, s=0.5)
plt.scatter(beta_resc40, mean40, s=0.5)
plt.show()


plt.figure()
plt.scatter(beta_resc10, spec_hat10, s=0.5)
plt.scatter(beta_resc20, spec_hat20, s=0.5)
plt.scatter(beta_resc30, spec_hat30, s=0.5)
plt.scatter(beta_resc40, spec_hat40, s=0.5)
plt.show()


# print(len(mean10), len(mean20))

# differenza=np.array(susc10)-np.array(susc20)

# for ii in range(len(differenza)):
#     if differenza[ii]>=0.0001:
#       print(differenza[ii])

# print(np.mean(differenza))
# print(np.mean(differenza[140::]))
# print(np.mean(differenza[0:140]))
