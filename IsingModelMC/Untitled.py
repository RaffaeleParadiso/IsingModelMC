import matplotlib.pyplot as plt
import numpy as np

err=np.loadtxt('results_analysis/calore_specifico/sigma_specific_heat_lattice_dim_10.txt')
sh=np.loadtxt('results_analysis/calore_specifico/calore_specifico_lattice_dim_10.txt')
beta=np.loadtxt('results_analysis/beta/beta_lattice_dim_10.txt')

plt.errorbar(beta, sh, yerr=2*err, fmt='.')
plt.show()