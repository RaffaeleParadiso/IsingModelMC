'''I seguenti for loops salvano ciascuno in un ndarray diverso tutti gli array delle varie grandezze indicate.
I valori di ogni file in ogni directory sono storati in modo da potervi accedere graficamente tramite for loops sul primo indice degli ndarray
'''
import os
import matplotlib.pyplot as plt
import numpy as np


path='results_analysis'
path1='results_analysis/beta_riscalato'
path2='results_analysis/suscettività_riscalata'
path3='results_analysis/calore_specifico'
path4='results_analysis/magnetizzazione_riscalata'
path5='results_analysis/suscettività'
path6='results_analysis/beta'

'''1. Sezione storage'''

###=====beta normali=====####
beta_normal=np.ndarray((5, 281))
for root, dirs, files in os.walk(path6, topdown=False):
    ii=0
    for name in files:
        a=os.path.join(root, name)
        beta_normal[ii,:]=np.array([[np.loadtxt(a)]])
        ii+=1

####======beta riscalati======####
beta=np.ndarray((5, 281))
for root, dirs, files in os.walk(path1, topdown=False):
    ii=0
    for name in files:
        a=os.path.join(root, name)
        beta[ii,:]=np.array([[np.loadtxt(a)]])
        ii+=1

####======suscettività normale======###
susc=np.ndarray((5, 281))
for root, dirs, files in os.walk(path5, topdown=False):
    ii=0
    for name in files:
        a=os.path.join(root, name)
        susc[ii,:]=np.array([[np.loadtxt(a)]])
        ii+=1

####======suscettività riscalata=====###
susc_resc=np.ndarray((5, 281))
for root, dirs, files in os.walk(path2, topdown=False):
    ii=0
    for name in files:
        a=os.path.join(root, name)
        susc_resc[ii,:]=np.array([[np.loadtxt(a)]])
        ii+=1

####=====calore specifico=====##
specific_heat=np.ndarray((5, 281))
for root, dirs, files in os.walk(path3, topdown=False):
    ii=0
    for name in files:
        a=os.path.join(root, name)
        specific_heat[ii,:]=np.array([[np.loadtxt(a)]])
        ii+=1

####=====magnetizzazione riscalata=====##
magn_resc=np.ndarray((5, 281))
for root, dirs, files in os.walk(path4, topdown=False):
    ii=0
    for name in files:
        a=os.path.join(root, name)
        magn_resc[ii,:]=np.array([[np.loadtxt(a)]])
        ii+=1
##################=================================#############################
'''2. Sezione grafici'''

plt.plot()
plt.title(r'$M$ vs $\beta$')
for i in range(0,5):
  plt.scatter(beta[i,:], magn_resc[i,:], s=0.5)
plt.show()

plt.plot()
plt.title(r'$\chi$ rescaled vs $\beta$')
for i in range(0,5):
  plt.scatter(beta[i,:], susc_resc[i,:], s=0.5)
plt.show()

plt.plot()
plt.title(r'$\chi$ vs $\beta$')
for i in range(0,5):
  plt.scatter(beta_normal[i,:], susc[i,:], s=0.5)
plt.show()

plt.plot()
plt.title(r'$C$ vs $\beta$')
for i in range(0,5):
  plt.scatter(beta[i,:], specific_heat[i,:], s=0.5)
plt.show()

#####========magnetizzazione in funzione di step montecarlo==========#####
mean_magn1=np.loadtxt('results_analysis/binder/beta_0.45/magnetization_latt_20_beta_0.45.txt')
mean_magn2=np.loadtxt('results/lattice_dim_20/magnetization/magnetization_beta_0.460.txt')
mean_magn3=np.loadtxt('results/lattice_dim_30/energies/energies_beta_0.450.txt')

plt.figure()
plt.scatter(range(0,len(mean_magn1)), mean_magn1, s=0.5)
plt.show()

########======cumulante di binder==========#######
binder=np.loadtxt('results_analysis/binder/beta_0.45/binder_beta_0.45.txt')

plt.figure()
plt.scatter(range(10, len(binder), 1), binder)
plt.show()