import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import model.costants as c

def func_gamma_su_nu(x, a, b, c):
   return a+b*x**c

def func_nu(x, a, b, c):
   return a+b*x**c

if __name__ == '__main__':
   beta_c=c.BETA_CRITICO
   path='results_analysis/suscettività/'
   beta=np.loadtxt('results_analysis/beta/beta_lattice_dim_10.txt')
   chi_max=[]
   index_chi_max=[]
   for files in os.listdir(path):
      if files.startswith('suscettività'):
         files=os.path.join(path, files)
         chi=np.loadtxt(files)
         chi_max.append(max(chi))
         index_chi_max.append(np.argmax(chi))
   beta_pseudo_critici=[beta[ii] for ii in index_chi_max]

   param_opt = curve_fit(func_gamma_su_nu, chi_max, np.arange(10,60,10))
   coeff, _ = param_opt
   print(coeff[2]**(-1))

   y_teorico = func_nu(np.arange(10,60,10), beta_c, -0.49, -1.)
   param_opt_2 = curve_fit(func_nu, np.arange(10,60,10), beta_pseudo_critici, bounds=(0,3))
   coeff, _ = param_opt_2
   print(coeff[0])
   plt.figure()
   plt.scatter(y_teorico,np.arange(10,60,10), label='Teorico')
   plt.scatter(coeff[0]+coeff[1]*np.arange(10,60,10)**(coeff[2]), np.arange(10,60,10), label='Sperimentale')
   plt.legend()
   
   plt.figure()
   plt.scatter(chi_max, np.arange(10,60,10))
   plt.show()
   def f(x, a, b, c):
      return a+b*x**c
   fa = curve_fit(f,np.arange(10,60,10), chi_max)
   par, _ = fa
   print(par)
