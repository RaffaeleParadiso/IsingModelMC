import logging
import multiprocessing
import os
import re
import statistics
import time
from functools import partial
from numba import njit, float64, types, jit
import numpy as np
import bootstrap_binder as btp

gorbaciov=False #sulla magnetizzazione eseguo o no?
logging.basicConfig(level=logging.INFO)

@njit(types.UniTuple(float64,2)(float64[:], float64, float64), cache=True, parallel=True, fastmath=True)
def calcoliamo_lamanna(array_osservabile, nlatt, beta):
  abs=np.abs(array_osservabile)
  susceptibility=np.var(abs)*nlatt**2*beta
  mean=np.mean(abs)
  return float(susceptibility), float(mean)

@njit(float64(float64[:], float64), cache=True, parallel=True, fastmath=True)
def calcolo_calore(array_osservabile, nlatt):
  specific_heat=np.var(array_osservabile)*nlatt**2
  return float(specific_heat)

def bootstrap_binning(array_osservabile, beta, dim, func, path, bin):
    sigma2=[]
    sigma3=[]
    sigma1=[]
    osservabile_magn=[]
    osservabile_chi=[]
    osservabile_calore=[]
    for _ in range(100):
        sample=btp.ricampionamento(array_osservabile, bin)
        if func==2:
          osservabile2, osservabile3=calcoliamo_lamanna(np.array(sample), dim, beta)  
          osservabile_chi.append(osservabile2)
          osservabile_magn.append(osservabile3)
        if func==1:
          osservabile1=calcolo_calore(np.array(sample), dim)
          osservabile_calore.append(osservabile1)
    sigma2=statistics.stdev(osservabile_chi) if osservabile_chi else []
    sigma3=statistics.stdev(osservabile_magn) if osservabile_magn else []
    sigma1=statistics.stdev(osservabile_calore) if osservabile_calore else []
    
    return(sigma1, sigma2, sigma3)

if __name__=='__main__':
  cammino='results'
  for lattice in os.listdir(cammino):
    path_results='results_analysis'
    lattice_dir=os.path.join(cammino, lattice)
    temp = re.findall(r'\d+', lattice_dir)   
    res= list(map(int, temp))                
    lattice_dim=res[0]
    sigma_chi_array=[]
    sigma_mean_array=[]
    sigma_specific_heat_array=[]
    path_results=os.path.join(path_results, f'sigma_latt_{lattice_dim}')
    for directories in os.listdir(lattice_dir):     
      path=os.path.join(lattice_dir, directories)
      for files in os.listdir(path):
        toc=time.perf_counter()
        en_magn_file=files
        energies_magn_file=os.path.join(path, files)
        with multiprocessing.Pool(processes=7) as pool:
          bin_values=[101,202,404,808,1616,3232,6464]
          dim=lattice_dim
          if files.startswith('e') == True:
              func=1
              temp = re.findall(r'\d+', energies_magn_file)   
              res= list(map(int, temp)) 
              en_array=np.loadtxt(f'{energies_magn_file}')
              beta_en=round(res[2]/1000, 4)
              partial_bootstrap=partial(bootstrap_binning, en_array, beta_en, dim, func, en_magn_file)
              results=np.array(pool.map(partial_bootstrap, bin_values))
              sigma_specific_heat=max(results[0:6,0])
              pool.close()
              pool.join()
              sigma_specific_heat_array.append(sigma_specific_heat)
              tic=time.perf_counter()
              logging.info(f'time {tic-toc:.4f}, s, dim: {lattice_dim}, file {files}')
          else:
            if gorbaciov==False:
              logging.info('Passing on magn')
              pass
            else:
              func=2
              temp = re.findall(r'\d+', energies_magn_file)   
              res= list(map(int, temp)) 
              magn_array=np.loadtxt(f'{energies_magn_file}')
              en_magn_file=energies_magn_file
              beta_magn=round(res[2]/1000, 4)
              partial_bootstrap=partial(bootstrap_binning, magn_array, beta_magn, dim, func, en_magn_file)
              results=np.array(pool.map(partial_bootstrap, bin_values))
              sigma_chi=max(results[0:6,1])
              sigma_magn= max(results[0:6, 2])
              pool.close()
              pool.join()
              sigma_chi_array.append(sigma_chi)
              sigma_mean_array.append(sigma_magn)
    if gorbaciov==True: np.savetxt(f'results_analysis/suscettività/sigma_susceptibility_lattice_dim_{lattice_dim}.txt', sigma_chi_array)
    if gorbaciov==True: np.savetxt(f'results_analysis/magnetizzazione_media/sigma_mean_magn_lattice_dim_{lattice_dim}.txt', sigma_mean_array)
    np.savetxt(f'results_analysis/calore_specifico/sigma_specific_heat_lattice_dim_{lattice_dim}.txt', sigma_specific_heat_array)