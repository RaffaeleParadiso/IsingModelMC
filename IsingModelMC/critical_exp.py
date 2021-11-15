import os
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from scipy.optimize import curve_fit
import model.costants as c

path='results_analysis/suscettività'
beta=list(np.loadtxt('results_analysis/beta/beta_lattice_dim_10.txt'))
beta_c=c.BETA_CRITICO
beta_range=[]
chi_range=[]
chi_max=[]
#uso beta nel range 0.43, 0.47 e mi ricavo i corrispettivi per chi

index_start=beta.index(0.35)
index_end=beta.index(0.47)
chi_range=np.ndarray((5,index_end-index_start+1)) #contiene i valori di chi nel range index_start, index_end
index_chi_max=[]
beta_range=[ii for ii in beta if ii>=0.43 and ii<=0.47]

count=0
for files in os.listdir(path):
   if files.startswith('suscettività'):
      files=os.path.join(path, files)
      chi=np.array(np.loadtxt(files))
      chi_max.append(max(chi))
      chi_range[count]=[chi[ii] for ii in range(index_end-index_start+1)]
      index_chi_max.append(np.argmax(chi))
      count+=1

beta_pseudo_critici=np.array([beta[ii] for ii in index_chi_max])

def func_gamma_su_nu(x, a, b, c):
   return a+b*x**c

param_opt=curve_fit(func_gamma_su_nu, chi_max, np.arange(10,60,10))
coeff, _ =param_opt
print(coeff[2]**(-1))

def func_nu(x, a, b, c): #è uguale all'altra, la riporto per chiarezza
   return a + b*x**c     #a=beta_critico, b=x_segnato, c=-1/nu

y_teorico=func_nu(np.arange(10,60,10), beta_c, -0.49, -1.) #qui imposto i valori teorici
param_opt_2=curve_fit(func_nu, np.arange(10,60,10), beta_pseudo_critici, bounds=(0,3))
coeff, _ =param_opt_2
print(coeff[0])
#qui plotto l'andamento teorico vs quello ottenuto
plt.plot(y_teorico,np.arange(10,60,10), label='Teorico')
plt.plot(coeff[0]+coeff[1]*np.arange(10,60,10)**(coeff[2]), np.arange(10,60,10), label='Sperimentale')
plt.legend()
plt.show()

#non so, gli andamenti sono simili ma i coefficiendi sono shballati





        
