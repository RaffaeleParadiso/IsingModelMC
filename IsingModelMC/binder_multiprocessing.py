import os
import re
import time
import numpy as np
import matplotlib.pyplot as plt
from numba import njit, float64
import concurrent.futures

path='results'

beta_start=0.340
beta_stop=0.480
beta_list_range=[]
beta_list=np.loadtxt(f'results_analysis/beta/beta_lattice_10.txt')
beta_range_path=f'results_analysis/binder_vs_beta/beta_list_range_{beta_start}_{beta_stop}.txt'

for beta in beta_list:
    if beta<=beta_start or beta>=beta_stop:
        continue
    else:
        beta_list_range.append(beta)
np.savetxt(beta_range_path, beta_list_range) if os.path.exists(beta_range_path)==False else print('beta_range esiste già')

@njit(float64(float64[:]),cache=True, parallel=True, fastmath=True)
def binder_function(array_osservabile):
    mean_2_2=np.mean(array_osservabile**2)**2
    mean_4=np.mean(array_osservabile**4)
    binder=mean_4/mean_2_2
    return binder
    
#########################=======Scegli l'intervallo, il cumulante lo offriamo noi!!!======================################################
#########################=================================================================================################################
def binder_multiprocessing(nlatt_dir):
    Binder_Forma_Perfetta=[]
    
    if os.path.exists(pattichiari) == True:
        print('Binder forma Perfetta già creato')
        pass
    else:
        direct=nlatt_dir
        start=time.time()
        for files in os.listdir(os.path.join(direct, 'magnetization')):
            temp=re.findall(r'\d+', files)
            res=list(map(int, temp))
            barba=float(res[1]/1000)
            if barba<=beta_start or barba>=beta_stop:
                # print('questo non serve', files)
                pass
            else:
                start=time.time()
                files=os.path.join(direct, 'magnetization', files)
                magn_file=np.loadtxt(files)
                Binder_Forma_Perfetta.append(binder_function(magn_file))
                print('Cumulante per file', files, 'calcolato in', round(time.time()-start,2), 'secs')
        print('Calcolo per ', nlatt_dir, 'ended in: ', round(time.time()-start, 2))
    return Binder_Forma_Perfetta

pattichiari=f'results_analysis/binder_vs_beta/binder_vs_beta_range_{beta_start}_{beta_stop}.txt'
lattice_directories=['results/lattice_dim_10','results/lattice_dim_20','results/lattice_dim_30','results/lattice_dim_40','results/lattice_dim_50']

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures=[]
    bindor=[]
    latt=0
    for dir in lattice_directories:
        futures.append(executor.submit(binder_multiprocessing, nlatt_dir=dir))
    for future in concurrent.futures.as_completed(futures):
        bindor.append(future.result()) #appende volta per volta l'array di binder per determinato lattice, creando automaticamente una lista di liste di dimensione(5, len(beta_list_range))
    np.savetxt(pattichiari, bindor) if os.path.exists(pattichiari)==False else print('Bindler per round [',beta_start,',', beta_stop,'] esistente già')
############===========plotting Binder===============#############
bindlers=np.loadtxt(f'results_analysis/binder_vs_beta/binder_vs_beta_range_{beta_start}_{beta_stop}.txt')
beta_list_range=np.loadtxt(f'results_analysis/binder_vs_beta/beta_list_range_{beta_start}_{beta_stop}.txt')
plt.figure()
for ii in range(5):
    plt.scatter(beta_list_range, bindor[ii], s=0.5)
plt.show()
