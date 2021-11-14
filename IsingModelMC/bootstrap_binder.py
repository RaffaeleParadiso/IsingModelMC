import os
import re
import statistics
import time
import numpy as np
from numba import njit, float64
import multiprocessing
import time
from functools import partial
import main_binder as mabin
import model.costants as c

@njit(float64[:](float64[:],float64), fastmath=True)
def ricampionamento(array_osservabile, bin):
    sample=[]
    for _ in range(int(len(array_osservabile)/bin)):
        ii=np.random.randint(0, len(array_osservabile)+1)
        sample.extend(array_osservabile[ii:min(ii+bin, len(array_osservabile))]) 
    return np.array(sample)

def bootstrap_binder(array_osservabile, bin):
    binder_array=[]
    sigma_binder=[]
    for _ in range(100):
        sample=ricampionamento(array_osservabile, bin)
        binder=mabin.binder_function(sample)
        binder_array.append(binder)
    sigma_binder.append(statistics.stdev(binder_array))
    return sigma_binder

if __name__=='__main__':
    beta_start = c.BETA_START
    beta_stop = c.BETA_STOP
    beta_list_range=np.loadtxt(f'results_analysis/binder/beta_range_{beta_start}_{beta_stop}.txt')
    path = 'results'
    bin_array=[101,202,404,808,1616,3232,6464]
    count_magn=10
    for lattice in os.listdir(path):
        lattice=os.path.join(path, lattice, 'magnetization')
        sigmo=[]
        for magn in os.listdir(lattice):
            temp= re.findall(r'\d+', magn)
            res=list(map(int, temp))
            beta= res[1]/1000
            if beta >=beta_start and beta<=beta_stop:
                magn=os.path.join(lattice, magn)
                nomefile=magn
                osservabile=np.loadtxt(magn)
                start=time.time()
                with multiprocessing.Pool(processes=6) as pool:
                    partiale=partial(bootstrap_binder, osservabile)
                    results=np.array(pool.map(partiale, bin_array))
                    sigmo.append(max(results))
        sigm = np.array(sigmo)
        np.savetxt(f'results_analysis/binder/binder_sigma_lattice_dim_{count_magn}.txt', sigm)
        count_magn += 10
