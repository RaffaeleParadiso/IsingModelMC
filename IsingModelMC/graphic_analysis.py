import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path

path='results_analysis'
path1='results_analysis/beta_riscalato'
path2='results_analysis/suscettività_riscalata'
path3='results_analysis/calore_specifico'
path4='results_analysis/magnetizzazione_riscalata'
path5='results_analysis/suscettività'


'''I seguenti for loops salvano ciascuno in un ndarray diverso tutti gli array delle varie grandezze indicate.
I valori di ogni file in ogni directory sono storati in modo da potervi accedere graficamente tramite for loops sul primo indice degli ndarray
'''


'''1. Sezione storage'''

####=====beta riscalati=====####
beta=np.ndarray((4, 281))
for root, dirs, files in os.walk(path1, topdown=False):
    ii=0
    for name in files:
        a=os.path.join(root, name)
        beta[ii,:]=np.array([[np.loadtxt(a)]])
        ii+=1

####======suscettività normale=====###
susc=np.ndarray((4, 281))
for root, dirs, files in os.walk(path2, topdown=False):
    ii=0
    for name in files:
        a=os.path.join(root, name)
        susc[ii,:]=np.array([[np.loadtxt(a)]])
        ii+=1

####======suscettività riscalata=====###
susc_resc=np.ndarray((4, 281))
for root, dirs, files in os.walk(path2, topdown=False):
    ii=0
    for name in files:
        a=os.path.join(root, name)
        susc_resc[ii,:]=np.array([[np.loadtxt(a)]])
        ii+=1

####=====calore specifico=====##
specific_heat=np.ndarray((4, 281))
for root, dirs, files in os.walk(path3, topdown=False):
    ii=0
    for name in files:
        a=os.path.join(root, name)
        specific_heat[ii,:]=np.array([[np.loadtxt(a)]])
        ii+=1

####=====magnetizzazione riscalata=====##
magn_resc=np.ndarray((4, 281))
for root, dirs, files in os.walk(path4, topdown=False):
    ii=0
    for name in files:
        a=os.path.join(root, name)
        magn_resc[ii,:]=np.array([[np.loadtxt(a)]])
        ii+=1
##################=================================#############################



'''2. Sezione grafici'''
#magnetizzazione
plt.plot()
plt.title(r'$M$ vs $\beta$')
for i in range(0,4):
  plt.scatter(beta[i,:], magn_resc[i,:], s=0.5)
plt.show()

plt.plot()
plt.title(r'$\chi$ rescaled vs $\beta$')
for i in range(0,4):
  plt.scatter(beta[i,:], susc_resc[i,:], s=0.5)
plt.show()

plt.plot()
plt.title(r'$\chi$ vs $\beta$')
for i in range(0,4):
  plt.scatter(beta[i,:], susc[i,:], s=0.5)
plt.show()

plt.plot()
plt.title(r'$C$ vs $\beta$')
for i in range(0,4):
    plt.scatter(beta[i,:], specific_heat[i,:], s=0.5)
plt.show()