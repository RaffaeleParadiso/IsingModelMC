import os
import statistics
from pathlib import Path
import time
import numpy as np

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
    path = os.getcwd()
    magnetization_path = Path(path + f"/results/lattice_dim_{dim_latt}/magnetization")
    mean_m = []
    beta_list = []
    for element in os.listdir(magnetization_path):
        file_ = os.path.join(magnetization_path, element)
        beta = float(element[19:24])
        beta_list.append(beta)
        magnetization = np.loadtxt(file_)
        mean = np.abs(magnetization)
        media = statistics.mean(mean)
        mean_m.append(media)
    return mean_m ,beta_list

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
    path = os.getcwd()
    chi = []
    beta_list = []
    magnetization_path = Path(path + f"/results/lattice_dim_{dim_latt}/magnetization")
    for element in os.listdir(magnetization_path):
        file_ = os.path.join(magnetization_path, element)
        beta = float(element[19:24])
        beta_list.append(beta)
        magnetization = np.loadtxt(file_)
        media = statistics.mean(magnetization**2)
        absolute = np.abs(magnetization)
        absolutesquared = statistics.mean(absolute)
        s = (dim_latt**2)*((media)-(absolutesquared**2))*(beta/100)
        chi.append(s)
    return chi, beta_list

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
    path = os.getcwd()
    s_heat = []
    beta_list = []
    energy_path = Path(path + f"/results/lattice_dim_{dim_latt}/energies")
    for element in os.listdir(energy_path):
        file_ = os.path.join(energy_path, element)
        beta = float(element[14:19])
        beta_list.append(beta)
        energy = np.loadtxt(file_)
        var_energy = statistics.pvariance(energy)
        s_heat.append((dim_latt**2)*var_energy)
    return s_heat, beta_list

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
