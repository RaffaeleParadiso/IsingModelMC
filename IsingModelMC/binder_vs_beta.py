import os
import re
import time
import numpy as np
import matplotlib.pyplot as plt
import statistics

path='results'


#########################=======Scegli l'intervallo, il cumulante lo offriamo noi!!!======================################################
#########################=================================================================================################################

beta_start=0.38
beta_stop=0.45
beta_list_range=[]

beta_list=np.loadtxt(f'results_analysis/beta/beta_lattice_10.txt')

for beta in beta_list:
    if beta<=beta_start or beta>=beta_stop:
        continue
    else:
        beta_list_range.append(beta)

print(beta_list_range)

Binder_Forma_Perfetta=np.ndarray((5, len(beta_list_range)))
pattichiari=f'results_analysis/binder_vs_beta/binder_vs_beta_range_0.{beta_start}_0.{beta_stop}.txt'

if os.path.exists(f'results_analysis/binder_vs_beta/binder_vs_beta_range_0.{beta_start}_0.{beta_stop}.txt') == True:
    print('Binder forma Perfetta già creato')
    pass
else:
    dir=0
    for direct in os.listdir(path):
        start=time.time()
        print('Calcolando Binder per range beta dato per latt =', (dir+1)*10)
        mm=0
        direct=os.path.join(path, direct, 'magnetization')
        for files in os.listdir(direct):
            temp=re.findall(r'\d+', files)
            res=list(map(int, temp))
            barba=float(res[1]/1000)
            print('barbaaaa', barba)
            if barba<=beta_start or barba>=beta_stop:
                print('next file')
            else:
                files=os.path.join(direct, files)
                print('You are here:', files)
                magn_file=np.loadtxt(files)
                mean_2_2=statistics.mean(np.array(magn_file)**2)**2
                mean_4=statistics.mean(np.array(magn_file)**4)
                binder=mean_4/mean_2_2
                Binder_Forma_Perfetta[dir, mm]=binder
                mm+=1
        print('Calcolo per lattice =', (dir+1)*10, 'ended in: ', round(time.time()-start, 2))
        dir+=1
    np.savetxt(pattichiari, Binder_Forma_Perfetta)

Binder_Forma_Perfetta=np.loadtxt(pattichiari)
print(Binder_Forma_Perfetta[0,:])
plt.figure()
for ii in range(5):
    colors=['green', 'blue', 'yellow', 'red', 'orange']
    plt.scatter(beta_list_range, Binder_Forma_Perfetta[ii,:], s=4, c=colors[ii])
plt.show()
       


    
