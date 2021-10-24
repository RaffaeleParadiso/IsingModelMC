'''Calcola gli errori di suscettività, magnetizzazione media e calore specifico richiamando func.bootstrap_binning'''
import os
import numpy as np

import module.func as fnc

path=('results')

osservabile=[]
sigma_measure_specific_heat=[]
sigma_measure_susceptibility=[]
sigma_measure_magnetization=[]
sigma_measure=[]
           
for cartella in os.listdir(path):
   directory=os.path.join(path, cartella)
   dim=int(os.path.join(cartella)[12:14])
   for root, dirs, files in os.walk(directory):
      for name in files:
         a=os.path.join(name)
         if a[0:8]=='energies':
            beta = float(a[14:19])
            ics=os.path.join(directory, name)
            osservabile=np.loadtxt(f"{path}/{cartella}/energies/{name}")
            sigma_measure_specific_heat.append(fnc.bootstrap_binning(osservabile, 2, beta, dim))
        
         if a[0:1]=='m':
            beta=float(a[19:24])
            osservabile=np.loadtxt(os.path.join(directory, name))
            sigma_measure_magnetization.append(fnc.bootstrap_binning(osservabile, 1, beta, dim))
            sigma_measure_susceptibility.append(fnc.bootstrap_binning(osservabile, 2, beta, dim))
      #forse vanno sull'altro for 
      np.savetxt(f'{directory}/error_specific_heat.txt', sigma_measure_specific_heat)
      np.savetxt(f'{directory}/error_susceptibility.txt', sigma_measure_susceptibility)
      np.savetxt(f'{directory}/error_magnetization.txt', sigma_measure_magnetization)


