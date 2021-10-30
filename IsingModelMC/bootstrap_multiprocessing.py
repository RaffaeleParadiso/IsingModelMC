import os
import re
import time
import numpy as np
import module.func as fnc

import multiprocessing
import time
from multiprocessing import Process
from functools import partial

def bootstrap_binning(array_osservabile, beta, dim, func, bin):
    
  sample=[]
  sigma1=[]
  sigma2=[]
  sigma3=[]
  step=0
    
  start=time.time()
  osservabile_sh=[]
  osservabile_magn=[]
  osservabile_chi=[]
  for _ in range(100):
      sample=[]
      for _ in range(int(len(array_osservabile)/bin)):
        ii=np.random.randint(0, len(array_osservabile)+1)
        sample.extend(array_osservabile[ii:min(ii+bin, len(array_osservabile))]) 
      if func == 1:
        osservabile1=fnc.calculus_on_energy(sample, dim, beta)
        osservabile_sh.append(osservabile1)
      if func == 2:
        osservabile2, osservabile3=fnc.calculus_on_magn(sample, dim, beta)  
        osservabile_magn.append(osservabile3)
        osservabile_chi.append(osservabile2)  
      
  sigma1.append(np.std(osservabile_sh))
  sigma2.append(np.std(osservabile_chi))
  sigma3.append(np.std(osservabile_magn))
  step+=1

  # print('iter: ', step, 'bin: ', bin/2, 'time per iter: ', time.time()-start)
  return(sigma1, sigma2, sigma3)
#########################m=====================multiprocessing================###############################
##########################====================================================###############################
'''Inizio multiprocessing'''
if __name__=='__main__':
  cammino='results'
  for lattice in os.listdir(cammino):
    lattice_dir=os.path.join(cammino, lattice)
    temp = re.findall(r'\d+', lattice_dir)   #####----to avoid cose[a:b]=numero_magico
    res= list(map(int, temp))                #####
    lattice_dim=res[0]
    print(r'Calcolo dei sigma per dimensione:', lattice_dim,'x',lattice_dim)

    sigma_c_array=[]
    sigma_chi_array=[]
    sigma_mean_array=[]

    for directories in os.listdir(lattice_dir):
      start=time.time()
      energies_magn_path=os.path.join(lattice_dir, directories)
      print('energies magnetization path=',energies_magn_path)
      for files in os.listdir(energies_magn_path):
        energies_magn_file=os.path.join(energies_magn_path, files)
        # print('Energy magn path', energies_magn_file)
        
        if files.startswith('e') == True:
          print('eNERGIEEEES', energies_magn_file)
          temp = re.findall(r'\d+', energies_magn_file)   #####----to avoid cose[a:b]=numero_magico
          res= list(map(int, temp))                       #####
          beta_en=res[2]/1000
          print(' ZIRKZIRKALIBABAAAAAAAAAA')
          print(beta_en)
  #########################m=====================multiprocessing================###############################
  #########################==========================energies===================###############################
          with multiprocessing.Pool(processes=7) as pool:
            energies_array=np.loadtxt(f'{energies_magn_file}')
            dim=lattice_dim
            func=1
            print('Calcolo sigma per beta=', beta_en)
            bin_values=[101,202,404,808,1616,3232,6464]
            partial_bootstrap=partial(bootstrap_binning, energies_array, beta_en, dim, func)
            results=np.array(pool.map(partial_bootstrap, bin_values))
            sigma_sp_heat=max(results[0:6,0])
            pool.close()
            pool.join()
            sigma_c_array.append(sigma_sp_heat)
          print(r'Calcolo array di sigma sul calore specifico per dimensione', lattice_dim, 'x', lattice_dim, 'ha impiegato:', round(time.time()-start, 2), 's')

        if files.startswith('m') == True:
          temp = re.findall(r'\d+', energies_magn_file)   #####----to avoid cose[a:b]=numero_magico
          res= list(map(int, temp))                       #####
          beta_magn=res[2]/1000
  #########################m=====================multiprocessing================###############################
  #########################=======================magnetization=================###############################
          with multiprocessing.Pool(processes=7) as pool:
            print('E qua invece ci arrivi??????????')
            magn_array=np.loadtxt(f'{energies_magn_file}')
            dim=lattice_dim
            func=2
            print('Calcolo sigma per beta=', beta_magn)
            bin_values=[101,202,404,808,1616,3232,6464]
            partial_bootstrap=partial(bootstrap_binning, magn_array, beta_magn, dim, func)
            results=np.array(pool.map(partial_bootstrap, bin_values))
            sigma_chi=max(results[0:6,1])
            sigma_mean=max(results[0:6,2])
            pool.close()
            pool.join()
            sigma_chi_array.append(sigma_chi)
            sigma_mean_array.append(sigma_mean)
          print(f'Calcolo array di sigma su <M> e X(Chi) per dimensione', lattice_dim, 'x', \
                lattice_dim, 'ha impiegato:', round(time.time()-start, 2), 's')
###########qua è da sistemare####################################
      np.savetxt(f'results/lattice_dim_{lattice_dim}/sigma_specific_heat_lattice_dim_{lattice_dim}.txt', sigma_c_array) 
      print('Array calore creato')   
      np.savetxt(f'results/lattice_dim_{lattice_dim}/sigma_susceptibility_lattice_dim_{lattice_dim}.txt', sigma_chi_array)
      print('Array chi creato')
      np.savetxt(f'results/lattice_dim_{lattice_dim}/sigma_mean_magn_lattice_dim_{lattice_dim}.txt', sigma_mean_array)
      print('Array mean creato')
      ###########=================verifica con if statement============================####################
      ###########======================================================================####################
      # if os.path.exists(f'results/lattice_dim_{lattice_dim}/energies/sigma_specific_heat.txt')==True:
      #   print('esiste')
      #   continue
      # else:
      #   np.savetxt(f'results/lattice_dim_{lattice_dim}/energies/sigma_specific_heat.txt', sigma_c_array)
      #   print('creato e mannaggiacristo so le 4')
      # if os.path.exists(f'results/lattice_dim_{lattice_dim}/magnetization/sigma_susceptibility.txt')== True:
      #   print('creata lamagn')
      #   continue
      # else:
      #   np.savetxt(f'results/lattice_dim_{lattice_dim}/magnetization/sigma_susceptibility.txt', sigma_chi_array)
      #   print('creato e mannaggiacristo so le 4')
      # if os.path.exists(f'results/lattice_dim_{lattice_dim}/magnetization/sigma_mean_magn.txt')== True:
      #   continue
      # else:
      #   np.savetxt(f'results/lattice_dim_{lattice_dim}/magnetization/sigma_mean_magn.txt', sigma_mean_array)
 