import os
import statistics
from pathlib import Path
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
        Array of mean magnetization for different value of beta.
    beta_list : list
        Array of beta at which the mean magnetization was calculated.
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
        Array of susceptivity for different value of beta.
    beta_list : list
        Array of beta at which the susceptivity was calculated.
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
        s = (dim_latt**2)*((media)-(absolutesquared**2))*(beta)
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
        Array of specific heat for different value of beta.
    beta_list : list
        Array of beta at which the susceptivity was calculated.
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

def calculus_on_energy(array, dim, beta):
    osservabile=[]
    square2=np.mean(array)**2
    square1=np.array(array)**2
    osservabile=np.array((dim**2*beta*(statistics.mean(square1)-square2)))
    return(osservabile)

def calculus_on_magn(array, dim, beta):
    osservabile=[]
    osservabile_mean=[]
    square2=(np.mean(np.abs(array)))**2
    square1=[samples**2 for samples in array]
    osservabile.append(dim**2*beta*(statistics.mean(square1)-square2))
    osservabile_mean=np.mean(array)
    return(osservabile, osservabile_mean)
