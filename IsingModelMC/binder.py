'''Calcolo cumulante di Binder. Occorre:
1. creare gli array per due beta diversi, 0.35 e 0.45, ma per vari reticoli, ber beta=0.35 dim_latt=1,..., 70 a step di 1
    per beta=0.45 dim_latt=1,...,200 a step di 5 circa
2. calcolare <M^4> e <M^2>^2 di ciascun array
3. plottare in 2 grafici diversi Binder (su y) e L (su x)'''

import os
import numpy as np 

import module.utils as ut
import module.func as fnc
import model.costants as c

i_decorrel=c.IDECORREL
measures=c.MEASURES
extfield=0

path='results_analysis/binder'

xmagn=[]
lattice_n=[]
list_beta=[0.35, 0.45]
energies=[]

if os.path.exists(path) == True:
        print('Binder directory already exists')
else:
        os.mkdir(path)

for beta in list_beta:
    path1=os.path.join(path, f'beta_{beta}')
    if os.path.exists(path1) ==True :
        continue
    else:
        os.mkdir(path1)


for beta in list_beta:
    for nlatt in range(50, 60, 1):
        if os.path.exists(f'results_analysis/binder/beta_{beta}/magnetization_latt_{nlatt}_beta_{beta}.txt') ==True:
            continue
        else:
            lattice_n=ut.initialize_lattice(1, nlatt)
            xmagn, energies=ut.run_metropolis(1, nlatt, lattice_n, i_decorrel, measures, extfield, beta)
            np.savetxt(f'results_analysis/binder/beta_{beta}/magnetization_latt_{nlatt}_beta_{beta}.txt', xmagn)

'''Binder calcolo'''

mean_magn=[]
binder=[]
mean_4=[]
mean_2_2=[]

for beta in list_beta:
  path=(f'results_analysis/binder/beta_{beta}')
  if os.path.exists(f'results_analysis/binder/beta_{beta}/binder_beta_{beta}.txt') == True:
      continue
  else: 
    for file in os.listdir(path):
        name=os.path.join(path, file)
        pattern=np.loadtxt(name)
        magn=np.array(pattern)
        mean_4=np.array(np.mean(magn**4))
        mean_2_2=np.array(np.mean(magn**2)**2)
        binder.append(mean_4/mean_2_2)
  np.savetxt(f'results_analysis/binder/beta_{beta}/binder_beta_{beta}.txt', binder)





