'''Calcolo degli errori con bootstrap con binning. Il programma prende i file dalle cartelle lattice_dim_ii e ne calcola la deviazione standard
in multiprocessing, parallelizzando i processi sui vari bin (7 in totale)'''
import os
import re
import statistics
import time
import numpy as np
import module.func as fnc
from numba import jit

import multiprocessing
import time
from multiprocessing import Process
from functools import partial

##################===========================bootsrtap con binning function======================================#############################
##################===============================================================================================#############################
# @jit(parallel=True)
def bootstrap_binning(array_osservabile, beta, dim, func, bin):
    
  sigma1=[]
  sigma2=[]
  sigma3=[]
  sigma4=[]
  step=0
  
  osservabile_sh=[]
  osservabile_magn=[]
  osservabile_chi=[]
  osservabile_binder=[]

  start=time.time()
  for _ in range(100):  
      sample=[]
      for _ in range(int(len(array_osservabile)/bin)):
        ii=np.random.randint(0, len(array_osservabile)+1)
        sample.extend(array_osservabile[ii:min(ii+bin, len(array_osservabile))]) 
      if func == 1:
        osservabile1=fnc.calculus_on_energy(sample, dim, beta)
        osservabile1=osservabile1.tolist()
        osservabile_sh.append(osservabile1)
        print('Ricampionamento n° ', len(osservabile_sh),'per beta_en=',beta, 'bin=', bin, 'latt =',dim)
      if func == 2:
        osservabile2, osservabile3=fnc.calculus_on_magn(np.array(sample), dim, beta)  
        osservabile_chi.append(osservabile2)
        osservabile_magn.append(osservabile3)        
        print('Ricampionamento n° ', len(osservabile_chi),'per beta_magn=',beta, 'bin=', bin, 'latt =',dim) 
      if func == 3: #####errori sul binder da rivedere
        mean_2_2=np.array(np.mean(sample**4))
        mean_4=np.array((np.mean(sample**2)**2))
        osservabile4=np.array(mean_4/mean_2_2)
        osservabile4=osservabile4.tolist()
        osservabile_binder.append(osservabile4)
        print('Ricampionamento n° ', len(osservabile_binder),'per beta_binder=',beta, 'bin=', bin)
####################==================if statement sugli array vuoti altrimenti statistics.stdev caca il cazzo============###########
  if osservabile_sh:
    sigma1=statistics.stdev(osservabile_sh)
  else:
    sigma1=[]
  if osservabile_chi and osservabile_magn:
    sigma2=statistics.stdev(np.array(osservabile_chi))
    sigma3=statistics.stdev(np.array(osservabile_magn))
  else:
    sigma2=[]
    print('Calcolo della chi per beta=', beta, 'ha richiesto:', round(time.time()-start, 2))
    sigma3=[]
    print('Calcolo della mean magn per beta=', beta, 'ha richiesto:', round(time.time()-start, 2))
  if osservabile_binder:
    sigma4=statistics.stdev(osservabile_binder)
    print('Calcolo del binder per beta=', beta, 'ha richiesto:', round(time.time()-start, 2))
  else:
    sigma4=[]
  step+=1
  return(sigma1, sigma2, sigma3, sigma4)
#####################=====================multiprocessing======================================================######################
#####################==========================================================================================######################
'''Inizio multiprocessing'''
if __name__=='__main__':

  sigma_c_array=[]
  sigma_chi_array=[]
  sigma_mean_array=[]

  cammino='results'
  for lattice in os.listdir(cammino):
    path_results='results_analysis'
    lattice_dir=os.path.join(cammino, lattice)
    temp = re.findall(r'\d+', lattice_dir)   #####----to avoid cose[a:b]=numero_magico
    res= list(map(int, temp))                #####
    lattice_dim=res[0]
#####################=======if statement sulle cartelle in cui salvare cose=====================================#####################
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
########################========= checking size path, if zero=>don't execute on energies============================#################
      if os.path.exists(f'{path_results}\sigma_specific_heat_lattice_dim_{lattice_dim}.txt')==False or \
        os.path.getsize(f'{path_results}\sigma_specific_heat_lattice_dim_{lattice_dim}.txt')== 0:
########################===========================================================================================##################
        for files in os.listdir(energies_magn_path):
          start2=time.time()
          energies_magn_file=os.path.join(energies_magn_path, files)
########################============if statement sui vari file di energia e magnetizzazione========================##################      
          if files.startswith('e') == True:
            print('Path energia == ', energies_magn_file)
            temp = re.findall(r'\d+', energies_magn_file)   #####----to avoid cose[a:b]=numero_magico
            res= list(map(int, temp))                       #####
#########################==========================================================================================##################
#########################=====================multiprocessing======================================================##################
#########################==========================energies========================================================##################
            energies_array=np.loadtxt(f'{energies_magn_file}')

            with multiprocessing.Pool(processes=7) as pool:
              print('wewewewewewewewewewewewewewewewewewewewwew')
              dim=lattice_dim
              beta_en=round(res[2]/1000, 4)
              func=1
              print('Calcolo sigma per beta_en=', beta_en)
              bin_values=[101,202,404,808,1616,3232,6464]
              partial_bootstrap=partial(bootstrap_binning, energies_array, beta_en, dim, func)
              results=np.array(pool.map(partial_bootstrap, bin_values))
              print('Questo è resultsssssssss', results)
              sigma_sp_heat=max(results[0:6,0])
              print('Verifica calore specificoooo',sigma_sp_heat)
              pool.close()
              pool.join()
              sigma_c_array.append(sigma_sp_heat)
              print(f'Calcolo sigma sul singono array {energies_magn_file} ha impiegato:', round(time.time()-start2, 2), 's')
        print(f'Calcolo array di sigma su calore specifico per lattice {lattice_dim} ha impiegato:', round(time.time()-start1, 2), 's')
        np.savetxt(f'{path_results}\sigma_specific_heat_lattice_dim_{lattice_dim}.txt', sigma_c_array) 
        print('Array calore creato') 
      else:
        print('Array di sigma sul calore specfico per lattice', lattice_dim, 'esistente già')
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
              func=2
              print('Calcolo sigma per beta_magn=', beta_magn)
              bin_values=[101,202,404,808,1616,3232,6464]
              partial_bootstrap=partial(bootstrap_binning, magn_array, beta_magn, dim, func)
              results=np.array(pool.map(partial_bootstrap, bin_values))
              sigma_chi=max(results[0:6,1])
              sigma_mean=max(results[0:6,2])
              pool.close()
              pool.join()
              sigma_chi_array.append(sigma_chi)
              sigma_mean_array.append(sigma_mean)
              print(f'Calcolo sul file magnetizzazione {energies_magn_file} <M> e X(Chi), per dimensione', lattice_dim, 'x', \
              lattice_dim, 'ha impiegato:', round(time.time()-start1, 2), 's')
        print(f'Calcolo array di sigma sugli array della magnetizzazione, per lattice {lattice_dim} ha impiegato:', round(time.time()-start1, 2), 's')
        np.savetxt(f'{path_results}/sigma_susceptibility_lattice_dim_{lattice_dim}.txt', sigma_chi_array)
        print('Array chi creato')
        np.savetxt(f'{path_results}/sigma_mean_magn_lattice_dim_{lattice_dim}.txt', sigma_mean_array)
        print('Array mean creato')
      else:
        print('Array sigma sulla magnetizzazione e sulla suscettività esistenti già per lattice=', lattice_dim)
'''Binder sigma'''
######################==============================Multiprocessing sigma Binder====================================#################
######################==============================================================================================#################
# if __name__=='__main__':
#   cammino='results_analysis/binder'
#   beta_values=[0.35, 0.45]
#   for beta_dir in os.listdir(cammino):
#     ii=0
#     if os.path.exists(f'{cammino}/sigma_binder_beta_{beta_values[ii]}.txt')==True:
#       ii+=1
#     else:
#       beta_array=os.path.join(cammino, beta_dir)
#       sigma_binder_array=[]
#       for magn in os.listdir(beta_array):
#         start=time.time()
#         if magn.startswith('m')==True:
#           magn_path=os.path.join(beta_array, magn)
#           with multiprocessing.Pool(processes=7) as pool:
#             magnet_array=np.loadtxt(f'{magn_path}')
#             print('Analazying the file:', magn_path)
#             temp = re.findall(r'\d+', magn_path)   #####----to avoid cose[a:b]=numero_magico
#             res= list(map(int, temp)) 
#             latt_dim=res[0]
#             bin_values=[101,202,404,808,1616,3232,6464]
#             func=3
#             partial_bootstrap=partial(bootstrap_binning, magnet_array, beta_values[ii], latt_dim, func)
#             risultato=np.array(pool.map(partial_bootstrap, bin_values))
#             sigma_binder=max(risultato[0:6,3])
#             sigma_binder_array.append(sigma_binder)
#           print('Array', magn, 'completed in:', round(time.time()-start,2), 'seconds')
#       np.savetxt(f'{cammino}/sigma_binder_beta_{beta_values[ii]}.txt', sigma_binder_array)
#       print('Array di errori per beta=', beta_values[ii], 'completato')
#       ii+=1
      
'''Manca ancora il calcolo degli errori sul cumulante di Binder per binder_vs_beta al variare del lattice, ma credo non ce ne sia nemmeno bisogno'''


