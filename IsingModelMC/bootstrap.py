from functools import partial
import multiprocessing
import os
import re
import statistics
from numba import njit, float64, types
import numpy as np
import bootstrap_binder as btb

@njit(types.UniTuple(float64,2)(float64[:], float64, float64), fastmath=True)
def calcoliamo_lamanna(array_osservabile, nlatt, beta):
  abs=np.abs(array_osservabile)
  susceptibility=np.var(abs)*nlatt**2*beta
  mean=np.mean(abs)
  return float(susceptibility), float(mean)

def bootstrap_binning(array_osservabile, beta, dim, bin):
    sigma2=[]
    sigma3=[]
    osservabile_magn=[]
    osservabile_chi=[]
    for _ in range(100):
        sample=btb.ricampionamento(array_osservabile, bin)
        osservabile2, osservabile3=calcoliamo_lamanna(np.array(sample), dim, beta)  
        osservabile_chi.append(osservabile2)
        osservabile_magn.append(osservabile3)        
        print('Ricampionamento n° ', len(osservabile_chi),'per beta_magn=',beta, 'bin=', bin, 'latt =',dim)
    sigma2=statistics.stdev(osservabile_chi)
    sigma3=statistics.stdev(osservabile_magn)
    return (sigma2, sigma3)

if __name__=='__main__':
  sigma_chi_array=[]
  sigma_mean_array=[]
  cammino='results'
  for lattice in os.listdir(cammino):
    path_results='results_analysis'
    lattice_dir=os.path.join(cammino, lattice)
    temp = re.findall(r'\d+', lattice_dir)
    res= list(map(int, temp))
    lattice_dim=res[0]
    sigma_chi_array=[]
    sigma_mean_array=[]
    path_results=os.path.join(path_results, 'sigma')
    path_results=os.path.join(path_results, f'sigma_latt_{lattice_dim}')
    for directories in os.listdir(lattice_dir):     
      path=os.path.join(lattice_dir, directories)
      for files in os.listdir(path):
        energies_magn_file=os.path.join(path, files)
        if files.startswith('m') == True:
          temp = re.findall(r'\d+', energies_magn_file)
          res= list(map(int, temp))
          with multiprocessing.Pool(processes=7) as pool:
            magn_array=np.loadtxt(f'{energies_magn_file}')
            beta_magn=round(res[2]/1000, 4)
            dim=lattice_dim
            bin_values=[101,202,404,808,1616,3232,6464]
            partial_bootstrap=partial(bootstrap_binning, magn_array, beta_magn, dim)
            results=np.array(pool.map(partial_bootstrap, bin_values))
            sigma_chi=max(results[0:6,0])
            sigma_mean=max(results[0:6,1])
            pool.close()
            pool.join()
            sigma_chi_array.append(sigma_chi)
            sigma_mean_array.append(sigma_mean)
      np.savetxt(f'results_analysis/suscettività/sigma_susceptibility_lattice_dim_{lattice_dim}.txt', sigma_chi_array)
      np.savetxt(f'results_analysis/magnetizzazione_media/sigma_mean_magn_lattice_dim_{lattice_dim}.txt', sigma_mean_array)
