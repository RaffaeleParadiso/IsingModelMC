import os
import statistics
from pathlib import Path
import time
import numpy as np
import matplotlib.pyplot as plt
import makedir as mk
from makedir import go_up

path = mk.go_up(1)
def susceptivity(dim_latt):
    '''
    Easy way to create a folder. You can go up from the current path up to 4 times.

    Parameters
    ----------
    name_dir : str
        From level you have set, complete path of the directory you want to create
    level_up : int, optional
        How many step up you want to do from the current path. The default is 0.

    Returns
    -------
    None.
    '''
    chi = []
    for element in os.listdir(path+f"//results/lattice_dim_{dim_latt}/magnetization"):
        file_ = os.path.join(path+f"//results/lattice_dim_{dim_latt}/magnetization", element)
        beta = float(element[19:24])
        magnetization = np.loadtxt(file_)
        media = statistics.mean(magnetization**2)
        absolute = np.abs(magnetization)
        absolutesquared = statistics.mean(absolute)
        s = (dim_latt**2)*((media)-(absolutesquared**2))*(beta/100)
        chi.append(s)
    return chi

def mean_magnetization(dim_latt):
    '''
    Easy way to create a folder. You can go up from the current path up to 4 times.

    Parameters
    ----------
    name_dir : str
        From level you have set, complete path of the directory you want to create
    level_up : int, optional
        How many step up you want to do from the current path. The default is 0.

    Returns
    -------
    None.
    '''
    mean_m = []
    for i in np.arange(20,85,5):
        magnetization = np.loadtxt(f"results\lattice_dim_latt_{dim_latt}\magnetization_beta_0.{i}0.txt")
        a = np.abs(magnetization)
        media = statistics.mean(a)
        mean_m.append(media)
    return mean_m

def specific_heat(dim_latt):
    '''
    Easy way to create a folder. You can go up from the current path up to 4 times.

    Parameters
    ----------
    name_dir : str
        From level you have set, complete path of the directory you want to create
    level_up : int, optional
        How many step up you want to do from the current path. The default is 0.

    Returns
    -------
    None.
    '''
    s_heat = []
    for i in np.arange(20,85,5):
        energy = np.loadtxt(f"results\lattice_dim_latt_{dim_latt}\energies_beta_0.{i}0.txt")
        var_energy = statistics.pvariance(energy)
        s_heat.append((dim_latt**2)*var_energy)
    return s_heat


a = susceptivity(10)



def bootstrap_binning(array_osservabile, func, beta, dim):
    '''
    Easy way to create a folder. You can go up from the current path up to 4 times.

    Parameters
    ----------
    name_dir : str
        From level you have set, complete path of the directory you want to create
    level_up : int, optional
        How many step up you want to do from the current path. The default is 0.

    Returns
    -------
    None.
    '''
    bin=1+len(array_osservabile)//1000
    sample=[]
    sigma=[]
    step=0
    while(bin<=1+len(array_osservabile)/10):
        start=time.time()
        osservabile=[]
        for _ in range(100):
            sample=[]
            #il ciclo for sotto mi crea l'array ricampionato
            for _ in range(int(len(array_osservabile)/bin)):
                ii=np.random.randint(0, len(array_osservabile)+1)
                sample.extend(array_osservabile[ii:min(ii+bin, len(array_osservabile))]) #questo è il miglior modo,
                                                                                       #altrimenti un ciclo while (len(sample)<=len(array_osservabile))
                                                                                       #e poi un for per assegnare gli elementi (fununzia ma il tempo è altissimo)
            '''qui specifico le funzioni da far agire sugli array ricampionati'''
            if func == 1:
                osservabile.append(statistics.mean(sample))
            
            if func == 2:
                square2=(np.mean(np.abs(sample)))**2
                square1=[samples**2 for samples in sample]
                osservabile.append(dim**2*beta*(statistics.mean(square1)-square2))

            if func == 3:
                square2=(np.mean(sample))**2
                square1=[samples**2 for samples in sample]
                osservabile.append(dim**2*beta*(statistics.mean(square1)-square2))      
            # osservabile.append(obs) #ho una len(osservabile)=100
        sigma.append(np.std(osservabile)) #len(sigma)=numero di bin diversi
        step+=1
        bin*=2 
        print('iter: ', step, 'bin: ', bin/2, 'time per iter: ', round((time.time()-start), 2))
    return(max(sigma))
