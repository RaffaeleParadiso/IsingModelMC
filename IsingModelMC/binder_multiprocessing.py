import os
import re
from numba import njit, float64
import numpy as np
import module.makedir as mk
path='results'
lattice_directories=['results/lattice_dim_10/magnetization','results/lattice_dim_20/magnetization','results/lattice_dim_30/magnetization','results/lattice_dim_40/magnetization','results/lattice_dim_50/magnetization']

beta_start=0.340
beta_stop=0.480

beta_list=np.loadtxt(f'results_analysis/beta/beta_lattice_dim_10.txt')
beta_list_range=[x for x in beta_list if x < 0.481 and x > 0.339]
mk.smart_makedir('results_analysis/binder')
np.savetxt(f'results_analysis/binder/beta_range_{beta_start}_{beta_stop}.txt', beta_list_range, fmt='%.3f')

@njit(float64(float64[:]),cache=True, parallel=True, fastmath=True)
def binder_function(array_osservabile):
    mean_2_2=np.mean(array_osservabile**2)**2
    mean_4=np.mean(array_osservabile**4)
    binder=mean_4/mean_2_2
    return binder

latt = 10
for i in lattice_directories:
    binder_l = []
    for j in os.listdir(i):
        temp=re.findall(r'\d+', j)
        res=list(map(int, temp))
        barba=float(res[1]/1000)
        if barba < 0.481 and barba > 0.339:
            magn = np.loadtxt(f'{i}/{j}')
            binder_f = binder_function(magn)
            binder_l.append(binder_f)
        binder = np.array(binder_l)
    np.savetxt(f"results_analysis/binder/binder_lattice_dim_{latt}.txt", binder)
    latt += 10
