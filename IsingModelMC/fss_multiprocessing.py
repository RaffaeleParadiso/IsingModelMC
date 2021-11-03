'''Finite size scaling in multiprocessing'''
import os
import re
import time
import numpy as np
import multiprocessing
from multiprocessing import Pool
from functools import partial
from numba import jit

import module.func as func
import model.costants as c

latt_dim_start=c.LATT_DIM_START
latt_dim_stop=c.LATT_DIM_STOP
latt_dim_passo=c.PASSO_LATT_DIM
gamma=c.GAMMA_TEORICO
nu=c.NU_TEORICO
beta_c=c.BETA_CRITICO

@jit()
def finite_size_scaling(count, lattice_dim):
    mean_magn=[] 
    mean_magn_rescaled=[]
    susceptibility=[]
    suscept_rescaled=[] 
    specific_heat=[] 
    beta_list=[] 
    beta_rescaled=[]
    start=time.time()
    print('Avvio in multiprocessing per lattice = ', lattice_dim)
    # if count[0]==0:
    #   mean_magn, beta_list=func.mean_magnetization(lattice_dim)#scemo chi legge
    if count[0]==0 and count[1]==0:
      print('Calcolo e riscalo la media')
      mean_magn, beta_list=func.mean_magnetization(lattice_dim)#scemo chi legge
      beta_list=np.array(np.round(beta_list, decimals=3, out=None))
      mean_magn_rescaled=np.array(mean_magn)*lattice_dim**(1/8)
    if (count[2]==0 and count[3]==0) or (count[2]==0 or count[3]==0):
      print('Calcolo e riscalo la chi')
      susceptibility, beta_list=func.susceptivity(lattice_dim)
      suscept_rescaled=np.array(np.array(susceptibility)*1/(lattice_dim)**(gamma/nu))#scemo chi legge
    if count[4]==0:
      print('Calcolo il calore specifico')
      specific_heat, beta_list=func.specific_heat(lattice_dim)
    if count[6]==0:
      beta_rescaled=np.array((np.array(beta_list)-beta_c)*lattice_dim**(1/nu))
    print('Tempo per il processo n° ', lattice_dim/10,'=', round(time.time()-start, 1), 'secondi')
 
    return(mean_magn, mean_magn_rescaled, susceptibility, suscept_rescaled, specific_heat, beta_list, beta_rescaled)

if __name__=='__main__':
    path='results_analysis'
    lattices=[ii for ii in range(10,60,10)]#scemo chi legge
    path_list=['magnetizzazione', 'magnetizzazione_riscalata','suscettività', 'suscettività_riscalata', 'calore_specifico','beta', 'beta_riscalato']
    ii=0      
    count=np.ones(7)
    print(count)
    for element in path_list:
        if os.path.exists(os.path.join(path, element))==False:
            count[ii]=0 ####in base ai valori di questo array eseguo vari pezzi della funzione di fss    
        else:
            count[ii]=1
        ii+=1    
###########================multiprocessing====================##################    
    with multiprocessing.Pool(processes=5) as pool:
        parziale=partial(finite_size_scaling, count)
        results=np.array(pool.map(parziale, lattices))
        print('Adesso mi trovo nel limbo')
###########===================================================################## 
    kk=0
    for dir in path_list:
        direct=os.path.join(path, dir)
        if os.path.exists(direct)==True:
            print('La directory', dir, 'esiste già')
        else:
            os.mkdir(direct)
        jj=0
        for lattice_dim in lattices:
            file_in_questione=os.path.join(direct, f'{dir}_lattice_{lattice_dim}.txt')
            if os.path.exists(file_in_questione)==True: 
                # os.path.getsize(file_in_questione)=0:
                print('Il file', file_in_questione, 'esiste già')
            else:
                np.savetxt(file_in_questione, results[jj, kk])
            jj+=1
        kk+=1
        print('File nella cartella', direct, 'creati successfully')
    print(results)


            
        

    




