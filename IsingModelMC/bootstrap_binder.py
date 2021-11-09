import os
import re
import statistics
import time
from numba.core.errors import NumbaDeprecationWarning, NumbaPendingDeprecationWarning, NumbaPerformanceWarning
import numpy as np
from numba import njit, float64
import multiprocessing
import time
from functools import partial
import warnings
####======qui imposto il range di beta su cui si deve calcolare gli errori per ogni lattice =====#####
####======l'importante è impostare lo stesso range che per il calcolo di binder==================#####
beta_start=0.34
beta_stop=0.48
####=============================================================================================#####
#beta_list_range=np.loadtxt(f'results_analysis/binder_vs_beta/beta_list_range_{beta_start}_{beta_stop}.txt')
warnings.simplefilter('ignore', category=NumbaDeprecationWarning)
warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)
warnings.simplefilter('ignore', category=NumbaPerformanceWarning)
###########==============qui definisco le varie funzioni in cui posso usare njit===============##############
###########====================================================================================##############
@njit(float64(float64[:]),cache=True, parallel=True, fastmath=True)
def binder_function(array_osservabile):
    mean_2_2=np.mean(array_osservabile**2)**2
    mean_4=np.mean(array_osservabile**4)
    binder=mean_4/mean_2_2
    return binder

@njit(float64[:](float64[:],float64), cache=True, parallel=True, fastmath=True)
def ricampionamento(array_osservabile, bin):
  sample=[]
  for _ in range(int(len(array_osservabile)/bin)):
    ii=np.random.randint(0, len(array_osservabile)+1)
    sample.extend(array_osservabile[ii:min(ii+bin, len(array_osservabile))]) 
  return np.array(sample)
###########====================================================================================#############
###########================inizio bootstrap su binder in multiprocessing=======================#############
###########====================================================================================#############
def bootstrap_binder(array_osservabile, nomefile, bin):
    binder_array=[]
    sigma_binder=[]
    for _ in range(100):
        print('Ricampionamento n°', _ , 'per file:', nomefile, 'bin = ', bin)
        sample=ricampionamento(array_osservabile, bin)
        binder=binder_function(sample)
        binder_array.append(binder)
    sigma_binder.append(statistics.stdev(binder_array))
    return sigma_binder

if __name__=='__main__':
    array_sigmi=np.ndarray((5, int((beta_stop-beta_start+0.001)*1000)))
    bin_array=[101,202,404,808,1616,3232,6464]
    path='results'
    count_magn=0
    if os.path.exists(f'results_analysis/binder_vs_beta/binder_range_{beta_start}_{beta_stop}.txt')==True:
        print('Gno questi errori li ho già calcolati')
    else:
        for lattice in os.listdir(path):
            lattice=os.path.join(path, lattice, 'magnetization')
            sigmo=[]
            for magn in os.listdir(lattice):
                temp= re.findall(r'\d+', magn)
                res=list(map(int, temp))
                beta= res[1]/1000
                if beta >=beta_start and beta<beta_stop:
                    print('Calcolo errore per ', magn)
                    magn=os.path.join(lattice, magn)
                    nomefile=magn
                    osservabile=np.loadtxt(magn)
                    start=time.time()
                    with multiprocessing.Pool(processes=len(bin_array)) as pool:
                        partiale=partial(bootstrap_binder, osservabile, nomefile)
                        results=np.array(pool.map(partiale, bin_array))
                        sigmo.append(max(results))
                        pool.close()
                        pool.join()
                    print('Ricampionamento di',nomefile,'ha richiesto', round(time.time()-start, 2), 'secondi')
                else: 
                    pass
                np.savetxt(f'results_analysis/binder_vs_beta/sigma_temp_range_{beta_start}_{beta_stop}.txt', sigmo)
            array_sigmi[count_magn]=sigmo
            count_magn+=1
        np.savetxt(f'results_analysis/binder_vs_beta/binder_sigma_range_{beta_start}_{beta_stop}.txt',array_sigmi)
#############=======================plot con errori=======================##################
#############=============================================================##################