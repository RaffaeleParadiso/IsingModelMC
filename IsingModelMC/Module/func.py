import os
import statistics
from pathlib import Path
import time
import numpy as np

def mean_magnetization(dim_latt):
    '''
    Return the mean magnetization for a specific beta and the list of the beta.
    ==========
    Parameters
    ----------
    dim_latt : int
        Dimension of the lattice.
    ==========
    Returns
    ----------
    mean_m : list
        List of mean magnetization for different value of beta.
    beta_list : list
        List of beta at which the mean magnetization was calculated.
    ==========
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
    Return the susceptivity for a specific beta and the list of the beta.
    ==========
    Parameters
    ----------
    dim_latt : int
        Dimension of the lattice.
    ==========
    Returns
    ----------
    chi : list
        List of susceptivity for different value of beta.
    beta_list : list
        List of beta at which the susceptivity was calculated.
    ==========
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
    Return the specific heat for a specific beta and the list of the beta.
    ==========
    Parameters
    ----------
    dim_latt : int
        Dimension of the lattice.
    ==========
    Returns
    ----------
    s_heat : list
        List of specific heat for different value of beta.
    beta_list : list
        List of beta at which the susceptivity was calculated.
    ==========
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
    Returns the max value of the standard deviation for 
    the observable array calculated for all the values of beta
    ==========
    Parameters
    ----------
    array_osservabile :

    func : int
        Define the behaviour of the function.
        If is set to 1 : return the maximum value of the mean of all the array for a fixed L.
        If is set to 2 : return the maximum value of the variance of all the array for a fixed L.
        If is set to 3 : return the maximum value of the st. dev. of all the array for a fixed L.

    beta :

    dim :
    ==========
    Returns
    ----------
    max(sigma) :

    ==========
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
        sigma.append(np.std(osservabile)) #len(sigma)=numero di bin diversi

        step+=1
        bin*=2 
        print('iter: ', step, 'bin: ', bin/2, 'time per iter: ', round((time.time()-start), 2))
    return (max(sigma))
