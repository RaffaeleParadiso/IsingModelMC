'''Calcolo i sigma sugli array magntizzazione per suscettività e magnetizzazione media, 
in multiprocessing per i vari bin. Ciascun array viene ricampionato 100 volte per 7 bin bla bla bla
e le funzioni vengono spacchettate come segue:
1. funzione ricampionamento che effettua ovviamente il ricampionamento per un certo bin
2. calcoliamo_lamanna che restituisce i valori di chi e magnetizzazione media per ogni 
    ricampionato.
Tutt cos con njit'''
import os
import re
import statistics
import time
from numba.core.decorators import jit
import numpy as np
from numba import njit, float64, types, jit

import multiprocessing
import time
from functools import partial
##################===========================bootsrtap con binning functions======================================#############################
##################===============================================================================================#############################
@njit(float64[:](float64[:],float64), cache=True, parallel=True, fastmath=True)
def ricampionamento(array_osservabile, bin):
  sample=[]
  for _ in range(int(len(array_osservabile)/bin)):
    ii=np.random.randint(0, len(array_osservabile)+1)
    sample.extend(array_osservabile[ii:min(ii+bin, len(array_osservabile))]) 
  return np.array(sample)

@njit(types.UniTuple(float64,2)(float64[:], float64, float64), cache=True, parallel=True, fastmath=True)
def calcoliamo_lamanna(array_osservabile, nlatt, beta):
  abs=np.abs(array_osservabile)
  susceptibility=np.var(abs)*nlatt**2*beta
  mean=np.mean(abs)
  return float(susceptibility), float(mean)
###########=====================bootstrap con binning core=====================##############
###########====================================================================##############
def bootstrap_binning(array_osservabile, beta, dim, bin):
    sigma2=[]
    sigma3=[]
    osservabile_magn=[]
    osservabile_chi=[]
    for _ in range(100):
        sample=ricampionamento(array_osservabile, bin)
        osservabile2, osservabile3=calcoliamo_lamanna(np.array(sample), dim, beta)  
        osservabile_chi.append(osservabile2)
        osservabile_magn.append(osservabile3)        
        print('Ricampionamento n° ', len(osservabile_chi),'per beta_magn=',beta, 'bin=', bin, 'latt =',dim)
    sigma2=statistics.stdev(osservabile_chi)
    sigma3=statistics.stdev(osservabile_magn)
    return(sigma2, sigma3)
###########======================multiprocessing===============================#####################
###########====================================================================#####################
if __name__=='__main__':

  sigma_chi_array=[]
  sigma_mean_array=[]

  cammino='results'
  for lattice in os.listdir(cammino):
    path_results='results_analysis'
    lattice_dir=os.path.join(cammino, lattice)
    temp = re.findall(r'\d+', lattice_dir)   #####----to avoid cose[a:b]=numero_magico
    res= list(map(int, temp))                #####
    lattice_dim=res[0]
    sigma_chi_array=[]
    sigma_mean_array=[]
##############=======if statement sulle cartelle in cui salvare cose=================#############
##############=======================================================================#############
    if os.path.exists(f'{path_results}/sigma') == True:
      print(f'jack johnson {path_results} created yet')
    else:
      os.mkdir(f'{path_results}/sigma')
  
    path_results=os.path.join(path_results, 'sigma')

    if os.path.exists(f'{path_results}/sigma_latt_{lattice_dim}') ==True:
      print(f'jack johnson 2 {path_results} created yet')
    else:
      os.mkdir(f'{path_results}/sigma_latt_{lattice_dim}')
######################=============================================================================================##################
    path_results=os.path.join(path_results, f'sigma_latt_{lattice_dim}')

    for directories in os.listdir(lattice_dir):     
      start1=time.time()
      energies_magn_path=os.path.join(lattice_dir, directories)
      print('energies magnetization path=',energies_magn_path)

#########################==============if statements sui file sigma associati alla magnetizzazione=================##################
      if (os.path.exists(f'{path_results}\sigma_mean_magn_lattice_dim_{lattice_dim}.txt') == False and\
        os.path.exists(f'{path_results}\sigma_susceptibility_lattice_dim_{lattice_dim}.txt') == False) or\
        (os.path.getsize(f'{path_results}\sigma_susceptibility_lattice_dim_{lattice_dim}.txt') == 0 and\
        os.path.getsize(f'{path_results}\sigma_mean_magn_lattice_dim_{lattice_dim}.txt') == 0):
########################===========================================================================================##################
        print('Inizio calcolo della magnetizzazione su lattice=', lattice_dim)
        for files in os.listdir(energies_magn_path):
          start1=time.time()
          energies_magn_file=os.path.join(energies_magn_path, files)
########################============if statement sui vari file di energia e magnetizzazione=========================#################
          if files.startswith('m') == True:
            temp = re.findall(r'\d+', energies_magn_file)   #####----to avoid cose[a:b]=numero_magico
            res= list(map(int, temp))                       #####
######################==============================================================================================#################
######################===========================multiprocessing====================================================#################
######################=============================magnetization====================================================#################
            with multiprocessing.Pool(processes=7) as pool:
              magn_array=np.loadtxt(f'{energies_magn_file}')
              beta_magn=round(res[2]/1000, 4)
              dim=lattice_dim
              print('Calcolo sigma per beta_magn=', beta_magn)
              bin_values=[101,202,404,808,1616,3232,6464]
              partial_bootstrap=partial(bootstrap_binning, magn_array, beta_magn, dim)
              results=np.array(pool.map(partial_bootstrap, bin_values))
              sigma_chi=max(results[0:6,0])
              sigma_mean=max(results[0:6,1])
              pool.close()
              pool.join()
              sigma_chi_array.append(sigma_chi)
              sigma_mean_array.append(sigma_mean)
              np.savetxt(f'{path_results}/sigma_mean_temp_latt_{lattice_dim}.txt',sigma_mean_array)
              np.savetxt(f'{path_results}/sigma_chi_temp_latt_{lattice_dim}.txt',sigma_chi_array)
              print(f'Calcolo sul file magnetizzazione {energies_magn_file} <M> e X(Chi), per dimensione', lattice_dim, 'x', \
              lattice_dim, 'ha impiegato:', round(time.time()-start1, 2), 's')
        print(f'Calcolo array di sigma sugli array della magnetizzazione, per lattice {lattice_dim} ha impiegato:', round(time.time()-start1, 2), 's')
        np.savetxt(f'{path_results}/sigma_susceptibility_lattice_dim_{lattice_dim}.txt', sigma_chi_array)
        print('Array chi creato')
        np.savetxt(f'{path_results}/sigma_mean_magn_lattice_dim_{lattice_dim}.txt', sigma_mean_array)
        print('Array mean creato')
      else:
        print('Array sigma sulla magnetizzazione e sulla suscettività esistenti già per lattice=', lattice_dim)