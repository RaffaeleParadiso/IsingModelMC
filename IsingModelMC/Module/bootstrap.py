import numpy as np
import statistics
from pathlib import Path
import time

def bootstrap_binning(array_osservabile, func, beta, dim):
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
            # osservabile.append(obs) #ho una len(osservabile)=100
        sigma.append(np.std(osservabile)) #len(sigma)=numero di bin diversi
        step+=1
        bin*=2 
        print('iter: ', step, 'bin: ', bin/2, 'time per iter: ', round((time.time()-start), 2))
    return(max(sigma))
